#!/usr/bin/env python3
"""Add only central-byk-test Vault resources; never install/restart/init Vault."""
import argparse
import base64
import json
from pathlib import Path
import re
import ssl
import subprocess
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, ProxyHandler, HTTPSHandler, HTTPRedirectHandler, build_opener

OWNER = 'central-byk-test'
PREFIX = OWNER + '/llm-module'
IDENTITIES = ('bootstrap', 'chatbot', 'common', 'service', 'knowledge', 'logging')


class Stop(Exception):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise Stop('redirect_refused')


def segment(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', value):
        raise Stop('invalid_mount')
    return value


def policies(mount):
    result = {}
    for kind in ('gui', 'cron', 'llm'):
        rules = []
        def add(path, capabilities):
            rules.append('path "' + path + '" { capabilities = ' + json.dumps(capabilities) + ' }')
        if kind in ('gui', 'cron'):
            add(mount + '/data/' + PREFIX + '/encryption/public_key', ['read'])
        add(mount + '/data/' + PREFIX + '/encryption/private_key', ['read'] if kind == 'cron' else ['deny'])
        for category in ('llm', 'embeddings'):
            add(mount + '/data/' + PREFIX + '/' + category + '/connections/*',
                ['create', 'read', 'update', 'delete'] if kind == 'cron' else ['read'] if kind == 'llm' else ['deny'])
            add(mount + '/metadata/' + PREFIX + '/' + category + '/connections/*',
                ['read', 'list', 'delete'] if kind == 'cron' else ['read', 'list'] if kind == 'llm' else ['deny'])
        if kind == 'llm':
            add(mount + '/data/' + PREFIX + '/langfuse/config', ['read'])
        for path, capabilities in [('auth/token/lookup-self', ['read']), ('auth/token/renew-self', ['update']), ('auth/token/revoke-self', ['update'])]:
            add(path, capabilities)
        result[OWNER + '-llm-' + kind] = '\n'.join(rules) + '\n'
    for kind in IDENTITIES:
        result[OWNER + '-os-' + kind + '-delivery'] = (
            'path "' + mount + '/data/opensearch/' + OWNER + '/' + kind + '" { capabilities = ["read"] }\n'
            'path "auth/token/revoke-self" { capabilities = ["update"] }\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bindings', required=True)
    parser.add_argument('--kubeconfig', required=True)
    parser.add_argument('--token-file')
    parser.add_argument('--opensearch-credentials-file')
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    binding = json.loads(Path(args.bindings).read_text())
    if binding.get('context') != 'rit-byrokratt' or binding.get('applicationNamespace') != OWNER:
        raise Stop('target_scope_mismatch')
    for field in ('expectedAPIServer', 'expectedKubeSystemUID', 'expectedVaultClusterID', 'vaultAddress'):
        if not isinstance(binding.get(field), str) or not binding[field]:
            raise Stop('unbound_' + field)
    mount = segment(binding.get('vaultKVMount', 'secret'))
    auth_mount = segment(binding.get('vaultAppRoleMount', 'approle'))
    url = urlsplit(binding['vaultAddress'])
    if url.scheme not in ('http', 'https') or not url.hostname or url.username or url.password or url.path not in ('', '/') or url.query or url.fragment:
        raise Stop('invalid_vault_origin')
    if url.scheme == 'http' and binding.get('allowVaultHTTP') is not True:
        raise Stop('http_requires_explicit_binding')
    planned = policies(mount)
    if not args.execute:
        print(json.dumps({'mode': 'plan', 'context': 'rit-byrokratt', 'namespace': OWNER, 'prefix': PREFIX,
                          'newRoles': list(planned), 'sharedVaultRestart': False, 'initialization': False,
                          'existingPolicyRoleOverwrite': False, 'keys': 'create-only or verify/reuse matching pair'}, indent=2))
        return
    if not args.token_file or not args.opensearch_credentials_file:
        raise Stop('private_material_files_required')
    token_path = Path(args.token_file)
    if token_path.stat().st_mode & 0o077:
        raise Stop('token_file_must_be_private')
    token = token_path.read_text().strip()
    if not token:
        raise Stop('empty_token_file')
    credentials_path = Path(args.opensearch_credentials_file)
    if credentials_path.stat().st_mode & 0o077:
        raise Stop('credential_file_must_be_private')
    credentials = json.loads(credentials_path.read_text())
    if credentials.get('installation') != OWNER or set(credentials.get('accounts', {})) != set(IDENTITIES):
        raise Stop('new_installation_account_contract_required')
    for account in credentials['accounts'].values():
        if set(account) != {'username', 'password'} or any(not isinstance(x, str) or not x or any(ord(c) < 32 for c in x) for x in account.values()) or ':' in account['username']:
            raise Stop('invalid_dedicated_account_material')
    if len({account['username'] for account in credentials['accounts'].values()}) != len(IDENTITIES):
        raise Stop('dedicated_account_names_must_be_unique')
    kube = ['kubectl', '--kubeconfig', str(Path(args.kubeconfig).resolve(strict=True)), '--context', 'rit-byrokratt', '--namespace', OWNER, '--request-timeout=20s']

    def kj(*arguments, payload=None, missing=False):
        command = kube + list(arguments)
        if missing:
            command += ['--ignore-not-found']
        r = subprocess.run(command, input=None if payload is None else json.dumps(payload).encode(), capture_output=True, timeout=30)
        if r.returncode:
            raise Stop('kubernetes_operation_failed')
        return json.loads(r.stdout) if r.stdout.strip() else None

    view = kj('config', 'view', '--minify', '-o', 'json')
    if len(view.get('clusters', [])) != 1 or view['clusters'][0]['cluster']['server'] != binding['expectedAPIServer']:
        raise Stop('api_server_identity_mismatch')
    system = kj('get', 'namespace', 'kube-system', '-o', 'json')
    if system['metadata']['uid'] != binding['expectedKubeSystemUID']:
        raise Stop('cluster_uid_mismatch')
    namespace = kj('get', 'namespace', OWNER, '-o', 'json')
    if namespace['metadata'].get('labels', {}).get('buerokratt.ee/deployment') != OWNER:
        raise Stop('namespace_not_task_owned')
    opener = build_opener(ProxyHandler({}), NoRedirect(), HTTPSHandler(context=ssl.create_default_context(cafile=binding.get('vaultCAFile') or None)))
    origin = binding['vaultAddress'].rstrip('/')

    def api(method, path, body=None, missing=False, bearer=token):
        headers = {'Content-Type': 'application/json'}
        if bearer:
            headers['X-Vault-Token'] = bearer
        req = Request(origin + '/v1/' + path, method=method, headers=headers,
                      data=None if body is None else json.dumps(body).encode())
        try:
            with opener.open(req, timeout=15) as response:
                raw = response.read(1048577)
                if len(raw) > 1048576:
                    raise Stop('vault_response_too_large')
                return json.loads(raw or '{}')
        except HTTPError as error:
            code = error.code; error.close()
            if missing and code == 404:
                return None
            raise Stop('vault_operation_http_' + str(code)) from None

    health = api('GET', 'sys/health', bearer=None)
    if health.get('initialized') is not True or health.get('sealed') is not False or health.get('cluster_id') != binding['expectedVaultClusterID']:
        raise Stop('vault_identity_or_health_mismatch')
    mounts = api('GET', 'sys/mounts')['data']
    auth = api('GET', 'sys/auth')['data']
    if mounts.get(mount + '/', {}).get('type') != 'kv' or str(mounts[mount + '/'].get('options', {}).get('version')) != '2':
        raise Stop('existing_kv_v2_mount_required')
    if auth.get(auth_mount + '/', {}).get('type') != 'approle':
        raise Stop('existing_approle_mount_required')
    for name, policy in planned.items():
        path = 'sys/policies/acl/' + name
        existing = api('GET', path, missing=True)
        if existing is None:
            api('PUT', path, {'policy': policy})
        elif existing.get('data', {}).get('policy', '').strip() != policy.strip():
            raise Stop('existing_test_policy_conflict')
        role_path = 'auth/' + auth_mount + '/role/' + name
        desired = {'token_policies': [name], 'token_period': 1200, 'bind_secret_id': True, 'secret_id_num_uses': 0, 'secret_id_ttl': 0, 'token_no_default_policy': True}
        existing = api('GET', role_path, missing=True)
        if existing is None:
            api('POST', role_path, desired)
        elif any(existing.get('data', {}).get(k) != v for k, v in desired.items()):
            raise Stop('existing_test_role_conflict')
        role_id = api('GET', role_path + '/role-id')['data']['role_id']
        secret_name = name + '-approle'
        existing = kj('get', 'secret', secret_name, '-o', 'json', missing=True)
        if existing is not None:
            if existing['metadata'].get('labels', {}).get('buerokratt.ee/deployment') != OWNER:
                raise Stop('credential_secret_owner_conflict')
            stored_role = base64.b64decode(existing['data']['role_id']).decode()
            secret_id = base64.b64decode(existing['data']['secret_id']).decode()
            if stored_role != role_id:
                raise Stop('existing_role_id_conflict')
        else:
            created = api('POST', role_path + '/secret-id', {})['data']
            secret_id = created['secret_id']
            resource = {'apiVersion': 'v1', 'kind': 'Secret', 'metadata': {'name': secret_name, 'namespace': OWNER,
                        'labels': {'buerokratt.ee/deployment': OWNER}}, 'type': 'Opaque',
                        'data': {k: base64.b64encode(v.encode()).decode() for k, v in {'role_id': role_id, 'secret_id': secret_id}.items()}}
            try:
                kj('create', '-f', '-', '-o', 'json', payload=resource)
            except Exception:
                api('POST', role_path + '/secret-id-accessor/destroy', {'secret_id_accessor': created['secret_id_accessor']})
                raise
        login = api('POST', 'auth/' + auth_mount + '/login', {'role_id': role_id, 'secret_id': secret_id}, bearer=None)
        check_token = login.get('auth', {}).get('client_token')
        if not check_token or set(login['auth'].get('policies', [])) != {name}:
            raise Stop('credential_login_or_scope_validation_failed')
        api('POST', 'auth/token/revoke-self', {}, bearer=check_token)

    def kv_read(path):
        response = api('GET', mount + '/data/' + path, missing=True)
        if response is None:
            return None
        data = response.get('data', {}).get('data')
        if not isinstance(data, dict):
            raise Stop('invalid_kv_read')
        return data

    def create_value(path, data):
        api('POST', mount + '/data/' + path, {'options': {'cas': 0}, 'data': data})

    private_path = PREFIX + '/encryption/private_key'
    public_path = PREFIX + '/encryption/public_key'
    private = kv_read(private_path); public = kv_read(public_path)
    if private is None:
        if public is not None:
            raise Stop('public_without_private_key')
        private = {'key': subprocess.run(['openssl', 'genpkey', '-algorithm', 'RSA', '-pkeyopt', 'rsa_keygen_bits:2048'], check=True, capture_output=True).stdout.decode(), 'algorithm': 'RSA-OAEP', 'key_size': 2048}
        create_value(private_path, private)
    derived = subprocess.run(['openssl', 'pkey', '-pubout'], input=private['key'].encode(), check=True, capture_output=True).stdout.decode()
    if public is None:
        create_value(public_path, {**private, 'key': derived})
    else:
        normalized = subprocess.run(['openssl', 'pkey', '-pubin', '-pubout'], input=public['key'].encode(), check=True, capture_output=True).stdout.decode()
        if derived != normalized:
            raise Stop('existing_rsa_pair_mismatch')
    for name, values in credentials['accounts'].items():
        path = 'opensearch/' + OWNER + '/' + name
        existing = kv_read(path)
        if existing is None:
            create_value(path, values)
        elif any(existing.get(k) != v for k, v in values.items()):
            raise Stop('existing_opensearch_credential_conflict')
    print(json.dumps({'status': 'PASS', 'testRolesValidated': list(planned), 'RSA': 'matching pair verified/reused or create-only',
                      'existingUnrelatedResourcesChanged': False, 'vaultRestartedOrReinitialized': False, 'credentialsExported': False}))


if __name__ == '__main__':
    try:
        main()
    except Stop as error:
        print('Stopped:', str(error)); raise SystemExit(1)
    except Exception as error:
        print('Stopped:', type(error).__name__); raise SystemExit(1)
