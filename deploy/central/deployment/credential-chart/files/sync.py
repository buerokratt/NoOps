"""Copy a scoped Vault KV-v2 credential into an explicitly opted-in Secret."""
import base64
import json
import os
from pathlib import Path
import re
import ssl
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import (
    HTTPRedirectHandler, HTTPSHandler, ProxyHandler, Request, build_opener,
)


class SyncError(Exception):
    """Safe error text; never include response bodies or credentials."""


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise SyncError("HTTP redirects are forbidden")


def request(opener, method, url, headers, payload=None, content_type="application/json"):
    body = None if payload is None else json.dumps(payload).encode()
    req = Request(url, data=body, headers={**headers, "Content-Type": content_type}, method=method)
    try:
        with opener.open(req, timeout=10) as response:
            raw = response.read(1048577)
            if len(raw) > 1048576:
                raise SyncError("HTTP response exceeds size limit")
            if not raw:
                return {}
            return json.loads(raw)
    except HTTPError as error:
        error.close()
        raise SyncError(f"{method} request failed with HTTP {error.code}") from None
    except (URLError, OSError, ValueError):
        raise SyncError(f"{method} request failed (transport or invalid JSON)") from None


def safe_path(value):
    if not isinstance(value, str) or not value or any(
        not re.fullmatch(r"[A-Za-z0-9_.-]+", segment) or segment in (".", "..")
        for segment in value.split("/")
    ):
        raise SyncError("Invalid Vault mount or secret path")
    return value


def vault_origin(value, allow_http=False):
    parsed = urlsplit(value)
    if (
        parsed.scheme not in (("https", "http") if allow_http else ("https",))
        or not parsed.hostname or parsed.username is not None or parsed.password is not None
        or parsed.path not in ("", "/") or parsed.query or parsed.fragment
        or any(ord(char) < 33 for char in value)
    ):
        raise SyncError("Vault address must be an HTTPS origin without credentials or path")
    return value.rstrip("/")


def encode_credentials(data):
    if not isinstance(data, dict):
        raise SyncError("Vault credential data must be an object")
    username, password = data.get("username"), data.get("password")
    if (
        not isinstance(username, str) or not isinstance(password, str)
        or not username or not password or ":" in username
        or any(ord(char) < 32 or ord(char) == 127 for char in username + password)
    ):
        raise SyncError("Vault credential requires valid username and password strings")
    return {
        key: base64.b64encode(value.encode()).decode()
        for key, value in {"username": username, "password": password, "auth": username + ":" + password}.items()
    }


def sync(vault_request, kube_request, config, role_id, secret_id):
    """GET/patch an existing Secret; a resourceVersion test prevents lost updates."""
    target = f'/api/v1/namespaces/{config["namespace"]}/secrets/{config["target"]}'
    current = kube_request("GET", target)
    metadata = current.get("metadata", {})
    if (
        current.get("type", "Opaque") != "Opaque" or current.get("immutable", False)
        or metadata.get("annotations", {}).get("opensearch.buerokratt.ee/vault-path")
        != config["kv_mount"] + "/" + config["secret_path"]
        or not metadata.get("resourceVersion")
    ):
        raise SyncError("Target must be a mutable, opted-in Opaque Secret with resourceVersion")
    token = None
    try:
        login = vault_request("POST", f'/v1/auth/{config["approle_mount"]}/login', {},
                              {"role_id": role_id, "secret_id": secret_id})
        token = login.get("auth", {}).get("client_token")
        if not isinstance(token, str) or not token:
            raise SyncError("Vault login did not return a token")
        result = vault_request("GET", f'/v1/{config["kv_mount"]}/data/{config["secret_path"]}',
                               {"X-Vault-Token": token})
        encoded = encode_credentials(result.get("data", {}).get("data"))
        existing = current.get("data") or {}
        merged = {**existing, **encoded}
        if merged == existing:
            return False
        kube_request("PATCH", target, [
            {"op": "test", "path": "/metadata/resourceVersion", "value": metadata["resourceVersion"]},
            {"op": "add", "path": "/data", "value": merged},
        ])
        return True
    finally:
        if token:
            vault_request("POST", "/v1/auth/token/revoke-self", {"X-Vault-Token": token}, {})


def main():
    origin = vault_origin(os.environ["VAULT_ADDR"], os.environ.get("VAULT_ALLOW_INSECURE_HTTP") == "true")
    config = {
        "approle_mount": safe_path(os.environ["VAULT_APPROLE_MOUNT"]),
        "kv_mount": safe_path(os.environ["VAULT_KV_MOUNT"]),
        "secret_path": safe_path(os.environ["VAULT_SECRET_PATH"]),
        "namespace": os.environ["TARGET_NAMESPACE"],
        "target": os.environ["TARGET_SECRET"],
    }
    for key in ("namespace", "target"):
        if not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", config[key]):
            raise SyncError("Invalid Kubernetes namespace or Secret name")
    vault_opener = build_opener(ProxyHandler({}), NoRedirect(), HTTPSHandler(
        context=ssl.create_default_context(cafile=os.environ.get("VAULT_CACERT"))))
    account = Path("/var/run/secrets/kubernetes.io/serviceaccount")
    kube_opener = build_opener(ProxyHandler({}), NoRedirect(), HTTPSHandler(
        context=ssl.create_default_context(cafile=str(account / "ca.crt"))))
    kube_headers = {"Authorization": "Bearer " + (account / "token").read_text().strip()}

    def vault_request(method, path, headers, payload=None):
        return request(vault_opener, method, origin + path, headers, payload)

    def kube_request(method, path, payload=None):
        return request(kube_opener, method, "https://kubernetes.default.svc" + path,
                       kube_headers, payload, "application/json-patch+json" if method == "PATCH" else "application/json")

    role_id = Path("/approle/role_id").read_text().strip()
    secret_id = Path("/approle/secret_id").read_text().strip()
    if not role_id or not secret_id:
        raise SyncError("AppRole credential files must be nonempty")
    changed = sync(vault_request, kube_request, config, role_id, secret_id)
    print("OpenSearch credential Secret updated" if changed else "OpenSearch credential Secret already matches")


if __name__ == "__main__":
    try:
        main()
    except SyncError as error:
        print(f"Credential sync failed: {error}", file=sys.stderr)
        sys.exit(1)
    except Exception:
        # A traceback could include a server-provided secret or token.
        print("Credential sync failed: configuration or unexpected response error", file=sys.stderr)
        sys.exit(1)
