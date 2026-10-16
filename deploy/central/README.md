# Central operator delivery through GitHub

This directory builds an operator package; CI never contacts Kubernetes or Vault.
Application repositories publish commit-tagged Linux/amd64 images. `source-lock.json`
selects exact reviewed commits. The Central release workflow resolves those
images by digest, verifies their source/revision labels, builds the combined
frontend and DSL assets, mirrors fixed public runtime images to GHCR, and uploads
an operator archive with its SHA-256 sidecar. It contains 22 runtime image bindings.

Push the application branches first and wait for their Central images jobs. Push
NoOps last: changes to this delivery directory trigger validation and publication.
A manual rerun also requires publish selected (manual dispatch availability follows
GitHub's default-branch workflow rules). The source locks must exist on GitHub before materialization can succeed.
For private images, grant this repository Actions read access on each producer
package. The cluster image-pull identity needs read access to the NoOps packages
and every application runtime package. Existing GHCR access alone does not prove
access to newly created packages. Do not commit registry tokens or kubeconfig.

Download the resulting `central-operator-<commit>.tar.gz` and SHA-256 sidecar to the
Mac. Check `shasum -a 256 -c <archive>.sha256`, extract, and run
`python3 verify-package.py` inside the extracted directory. Use
`python3 deployment/operator-run.py --help` and the bindings template to prepare
operator-owned inputs. The renderer restricts the context to `rit-byrokratt`, the
application namespace to `central-byk-test`, and the dedicated engine to `central`.
It preserves existing Vault and rejects protected namespace/identity drift.
Never substitute `cl13-llm` as the application namespace.

If cluster credentials are already delivered through an image-pull Secret, set
`imagePullSecret` to its name and verify it exists in both `central-byk-test` and
`central`; Kubernetes Secrets are namespace scoped. Otherwise the operator can set
`imagePullConfigFile` to a mode-0600 Docker auth JSON containing only `ghcr.io`.
The renderer then creates dedicated `central-byk-test-registry-pull` Secrets in
both namespaces. Keep that auth file outside Git and out of the CI artifact.

Set `kubernetesAPICIDR` and `kubernetesAPIPort` to the API destination observed
by the cluster CNI after service translation. A Kubernetes Service on TCP443 can
forward to an API endpoint on TCP6443; for Calico workload policies, bind the
endpoint IP as a /32 (or /128 for IPv6) and its endpoint port. The template uses
6443; older bindings that omit the port retain 443. Only the scoped Vault delivery
Pods receive this API egress rule. See the [Calico policy reference](https://docs.tigera.io/calico/latest/reference/resources/globalnetworkpolicy)
for DNAT ordering. Verify connectivity in the target cluster; offline rendering
cannot prove CNI enforcement.

This is a fresh create-only deployment. Bind current cluster identities, storage,
DNS/TLS, ingress and Vault contracts using the template and review the rendered
plan before the operator applies it. Credentials, private keys and generated state
stay outside this repository. Do not use fresh initializers against an existing
installation. This new CI build still requires operator environment acceptance;
local source tests do not qualify remote ingress, admission, capacity or CNI.
Model generation remains disabled. The notification image is the retained legacy
integration; the isolated RabbitMQ replacement is excluded.

## Testing through kubectl port-forward

Set `frontendAccessMode` to `port-forward` and `frontendOrigin` to
`http://localhost:18080`. In this explicit mode, frontend TLS files, ingress class
and ingress namespace are unnecessary. The package creates no frontend Ingress
or TLS Secret and grants no ingress-controller access. The default `ingress`
mode continues to require verified HTTPS/TLS inputs. External HTTP origins are
rejected in port-forward mode.

Keep an operator-side Vault tunnel running in another terminal (use your actual
service name): `kubectl --kubeconfig rit-byrokratt.yaml --context rit-byrokratt
-n central port-forward --address 127.0.0.1 service/VAULT_SERVICE 18200:8200`.
For an existing HTTP Vault listener, use `vaultAddress=http://127.0.0.1:18200`,
its internal service HTTP URL as `workloadVaultAddress`, and `allowVaultHTTP=true`.
This preserves the existing listener; it does not change Vault configuration.

Run the installer normally. Port-forward mode reports
`INSTALLED_ORIGIN_ACCEPTANCE_PENDING` until the separate browser/health checks.
After installation, keep the frontend tunnel running in another terminal:

```sh
kubectl --kubeconfig rit-byrokratt.yaml --context rit-byrokratt \
  -n central-byk-test port-forward --address 127.0.0.1 \
  service/central-byk-test-frontend 18080:8080
```

Then run `deployment/health.py` with the same bindings, kubeconfig and state-dir,
and open `http://localhost:18080/chat/`. Use the exact configured origin consistently
for login, cookies and browser tabs. No DNS record, external ingress or inbound
firewall opening is required. Kubernetes API access and internal Pod networking
are still required. This mode has offline contract coverage; actual cluster CNI,
port-forward and browser acceptance are operator checks after deployment.

## Opt-in model generation

`llmGenerationEnabled` defaults to false. Enable it with boolean true and
`llmProviderCIDRs`: current public provider host addresses as /32 or /128 CIDRs.
Only the LLM Pod receives HTTPS egress to these destinations. Address changes need
binding/policy updates. Runtime model downloads stay offline; the producer image
bundles verified guardrails embeddings. Credentials remain in Resql/Vault. The
backend Service exposes Resql8082 for connection lookups. Bot activation stays
false; this change does not activate the external chatbot bot route.

For an existing installation, use the NEW package's `deployment/generation-upgrade.py`
with the ORIGINAL state, bindings and image overrides:

```sh
python3 deployment/generation-upgrade.py \
  --bindings "$BYK_PRIVATE/bindings.json" \
  --images "$BYK_PRIVATE/images-resql-fixed.json" \
  --kubeconfig "$BYK_KUBECONFIG" --state-dir "$BYK_PRIVATE/state" \
  --llm-image "IMMUTABLE_NEW_LLM_IMAGE_FROM_THIS_PACKAGE" \
  --provider-cidr "CURRENT_PROVIDER_IP/32"
# Repeat with --execute after GENERATION_UPGRADE_PLAN_PASS.
```

Plan checks identity, preservation and server admission without mutation. Execute
changes only task LLM/notification Deployments, backend Service and provider policy.
It accepts the exact temporary generation/port/policy repairs from testing, rejects
unrelated drift, backs up old binding/image/manifest/stages and synchronizes that
same private state. No schema/provisioning Jobs, DB/PVCs or Vault credentials change.
If a patch fails, rerun using the same state to finish. Do not initialize new state
or rerun the new create-only installer against the old manifest without this upgrade.

Then run this package's `deployment/health.py` with the updated original bindings
and state. It requires enabled generation, connected Redis and verified embedding
startup. Provider output still needs an LLM GUI test: use the existing testing
connection, verify completed output/SSE, then reload and check single storage.
Keep chatbot bot routing disabled pending separate routing correction/acceptance.

## Run-2 retrieval/GUI acceptance repair

The upgrade helper also accepts `--frontend-image` with this package's immutable
frontend reference. It changes only the frontend image alongside the scoped
LLM upgrade and saves a version-specific state backup. Existing frontend APIs,
credentials, data and backend Pod remain untouched. Reconnect the frontend
port-forward after its Pod changes.

The LLM image owns `/app/logs` as UID1000; real EmbeddingManager write smoke runs
without network access in CI. CKB account/auth requests use backoffice while
agency/data calls use CKB; Service GUI URLs no longer duplicate the private prefix.

For isolated RAG acceptance, `deployment/synthetic-knowledge.py --bindings ...
--kubeconfig ... --state-dir ...` plans a single fictional library reference.
Repeat with `--execute` to embed it through the existing testing connection and
index one fixed point in task Qdrant. It refuses foreign points/nonempty knowledge
or incompatible vector schema. Repeat runs reuse the exact fixture with no extra
provider call. It never imports real data or runs the unfinished CKB S3/pipeline.
Afterward ask: "According to the Central Test municipal library reference, what
three services does the library provide?" Verify a generated reply and real
inference_results storage, not the known fixture inference view endpoint.
The Test LLM screen has no history restoration feature; reload restoration there
is unsupported. Service/CKB browser checks still require operator acceptance.


## Run-3 widget repair and testing-only LLM adapter

After the successful RUN3 LLM GUI acceptance, upgrade the existing installation
with `generation-upgrade.py --frontend-image <this-release-frontend>
--widget-datamapper <this-release-datamapper> --enable-widget-llm` in addition to
its usual binding, images, kubeconfig, original state, LLM image and provider CIDR
arguments. Run the plan first, then repeat with `--execute`. Preserve original
private state and image overrides. Do not run the full installer or reseed the DSL
PVC. The helper permits only the existing scoped generation targets plus frontend,
backend Deployment, backend-config and one widget-runtime-fixes ConfigMap. It
replaces the backend Pod to activate interpreter caches, preserving its existing
DB/key PVCs, init-free runtime, credentials and all schema Jobs.

The six read-only file overrides fix greeting SQL's cross-database Service table
reference, greeting Service lookup, missing account-domain selections, bot request
timeout and TIM's null session duration. DataMapper grants no domains for missing
selections. Widget session duration defaults to 30 minutes before serialization.
The internal bot constant points to this task's LLM Service. The adapter is opt-in,
uses only the existing testing connection and consumes the guarded orchestration
stream through EOF so inference storage completes. It returns one final Rasa-format
reply through the existing widget/chat notification path; widget token streaming
is not implemented. Missing testing connection fails closed, without production
fallback. Existing generation-disabled bindings omit these new resources/env vars.

The upgrade does not enable `is_bot_active` in the application database. For the
controlled browser test, first retain its exact previous value and verify there
are no existing bot-assigned active chats that switching it off could transfer.
Temporarily enable the bot through the standard backoffice control, create one
new marked widget chat, ask the synthetic library question once, verify its final
reply and single inference/chat-message storage, then reload and reconnect. End
only that new test chat before restoring the previous bot setting. Preserve all
other chats, accounts, availability, schemas, engine Pods and Vault state. Do not
reindex the already accepted RUN3 fixture, call a production connection, broaden
provider egress or claim CKB ingestion acceptance.
