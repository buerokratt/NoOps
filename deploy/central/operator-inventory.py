#!/usr/bin/env python3
"""Read-only, credential-free deployment inventory. Run on the operator's host."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kubectl', default='kubectl')
    parser.add_argument('--kubeconfig', required=True)
    parser.add_argument('--expected-server', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    config = Path(args.kubeconfig).expanduser().resolve(strict=True)
    if not config.is_file():
        raise ValueError('kubeconfig must be a file')
    output = Path(args.output).expanduser()
    if output.exists():
        raise ValueError('output already exists; retain previous inventory')
    base = [args.kubectl, '--kubeconfig', str(config), '--context', 'rit-byrokratt', '--request-timeout=20s']

    def read(*arguments, namespace):
        result = subprocess.run(base + ['--namespace', namespace] + list(arguments), capture_output=True, timeout=30)
        if result.returncode:
            # Do not expose auth-provider stderr or accidentally export credentials.
            raise RuntimeError('read-only inventory request failed: ' + arguments[0])
        return json.loads(result.stdout)

    view = read('config', 'view', '--minify', '-o', 'json', namespace='central')
    if len(view.get('clusters', [])) != 1 or len(view.get('contexts', [])) != 1:
        raise ValueError('ambiguous context binding')
    server = view['clusters'][0]['cluster']['server']
    if view['contexts'][0]['name'] != 'rit-byrokratt' or server != args.expected_server:
        raise ValueError('context/API-server identity mismatch')
    namespaces = read('get', 'namespaces', '-o', 'json', namespace='central')['items']
    namespace_ids = {x['metadata']['name']: x['metadata']['uid'] for x in namespaces}
    if 'central' not in namespace_ids or 'kube-system' not in namespace_ids:
        raise ValueError('required central/kube-system namespaces missing')
    report = {'context': 'rit-byrokratt', 'server': server, 'clusterNamespaceUID': namespace_ids['kube-system'],
              'namespaceUIDs': namespace_ids, 'readOnly': True, 'secretValuesCollected': False, 'namespaces': {}}
    kinds = 'pods,deployments,statefulsets,services,persistentvolumeclaims,configmaps,ingresses,networkpolicies,resourcequotas,limitranges'
    for namespace in ['central', 'central-opensearch-poc', 'central-byk-test', 'cl13-llm']:
        if namespace not in namespace_ids:
            report['namespaces'][namespace] = {'exists': False}
            continue
        rows = []
        for item in read('get', kinds, '-o', 'json', namespace=namespace)['items']:
            metadata = item['metadata']
            row = {'kind': item['kind'], 'name': metadata['name'], 'uid': metadata['uid'],
                   'resourceVersion': metadata['resourceVersion'], 'labels': metadata.get('labels', {}),
                   'owners': metadata.get('ownerReferences', []), 'finalizers': metadata.get('finalizers', [])}
            spec = item.get('spec', {})
            if item['kind'] in ['Deployment', 'StatefulSet', 'Pod']:
                pod = spec if item['kind'] == 'Pod' else spec.get('template', {}).get('spec', {})
                row['workload'] = {'replicas': spec.get('replicas'), 'serviceAccountName': pod.get('serviceAccountName'),
                                   'volumes': pod.get('volumes', []), 'nodeSelector': pod.get('nodeSelector', {}),
                                   'securityContext': pod.get('securityContext', {})}
                for group in ['containers', 'initContainers']:
                    row['workload'][group] = [{'name': c['name'], 'image': c['image'],
                        'mounts': c.get('volumeMounts', []), 'resources': c.get('resources', {}),
                        'envReferences': [{'name': e['name'], 'valueFrom': e.get('valueFrom')} for e in c.get('env', [])],
                        'envFrom': c.get('envFrom', [])} for c in pod.get(group, [])]
                if item['kind'] == 'StatefulSet': row['claimTemplates'] = spec.get('volumeClaimTemplates', [])
                if item['kind'] == 'Pod':
                    row['phase'] = item.get('status', {}).get('phase')
                    row['containerStatuses'] = [{key: c.get(key) for key in ['name', 'ready', 'containerID', 'imageID', 'restartCount']}
                        for c in item.get('status', {}).get('containerStatuses', [])]
            elif item['kind'] == 'ConfigMap':
                # Retain comparison evidence without exporting bootstrap scripts/inline secrets.
                row['contentKeys'] = sorted(set(item.get('data', {})) | set(item.get('binaryData', {})))
                row['contentSHA256'] = hashlib.sha256(json.dumps({k: item.get(k, {}) for k in ['data', 'binaryData']}, sort_keys=True).encode()).hexdigest()
            else:
                row['spec'] = spec
                if item['kind'] == 'PersistentVolumeClaim': row['phase'] = item.get('status', {}).get('phase')
            rows.append(row)
        report['namespaces'][namespace] = {'exists': True, 'resources': rows}
    report['storageClasses'] = [{key: x.get(key) for key in ['provisioner', 'reclaimPolicy', 'volumeBindingMode', 'allowVolumeExpansion']} |
                              {'name': x['metadata']['name']} for x in read('get', 'storageclasses', '-o', 'json', namespace='central')['items']]
    report['persistentVolumes'] = [{'name': x['metadata']['name'], 'uid': x['metadata']['uid'],
        'claimRef': x['spec'].get('claimRef'), 'reclaimPolicy': x['spec'].get('persistentVolumeReclaimPolicy'),
        'storageClassName': x['spec'].get('storageClassName'), 'capacity': x['spec'].get('capacity'),
        'accessModes': x['spec'].get('accessModes'), 'finalizers': x['metadata'].get('finalizers', [])}
        for x in read('get', 'persistentvolumes', '-o', 'json', namespace='central')['items']]
    report['ingressClasses'] = [{'name': x['metadata']['name'], 'uid': x['metadata']['uid'], 'controller': x['spec']['controller']} for x in read('get','ingressclasses','-o','json',namespace='central')['items']]
    report['nodes'] = [{'name': x['metadata']['name'], 'uid': x['metadata']['uid'], 'architecture': x.get('status',{}).get('nodeInfo',{}).get('architecture'), 'allocatable': x.get('status',{}).get('allocatable'), 'conditions': [{'type': c['type'], 'status': c['status']} for c in x.get('status',{}).get('conditions',[])]} for x in read('get','nodes','-o','json',namespace='central')['items']]
    service=read('get','service','kubernetes','-o','json',namespace='default');report['kubernetesAPIService']={'clusterIP':service['spec']['clusterIP'],'ports':service['spec']['ports']}
    endpoint=read('get','endpoints','kubernetes','-o','json',namespace='default');report['kubernetesAPIEndpoints']=endpoint.get('subsets',[])
    # Exclusive creation prevents accidentally overwriting prior evidence.
    with output.open('x') as file:
        json.dump(report, file, indent=2); file.write('\n')
    print('Read-only inventory saved. No deployment/Secret read/Helm values export performed.')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('Inventory stopped:', type(error).__name__)
        raise SystemExit(1)
