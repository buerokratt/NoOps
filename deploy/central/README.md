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

This is a fresh create-only deployment. Bind current cluster identities, storage,
DNS/TLS, ingress and Vault contracts using the template and review the rendered
plan before the operator applies it. Credentials, private keys and generated state
stay outside this repository. Do not use fresh initializers against an existing
installation. This new CI build still requires operator environment acceptance;
local source tests do not qualify remote ingress, admission, capacity or CNI.
Model generation remains disabled. The notification image is the retained legacy
integration; the isolated RabbitMQ replacement is excluded.
