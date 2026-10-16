{{- define "opensearch.bootstrap.validate" -}}
{{- if not .Values.server.enabled -}}
{{- $credential := required "External OpenSearch bootstrap requires bootstrap.credentialsSecret" .Values.bootstrap.credentialsSecret -}}
{{- if or (not (regexMatch "^https?://[^/?#@[:space:]]+/?$" .Values.bootstrap.url)) (contains "component-opensearch-node" .Values.bootstrap.url) -}}
{{- fail "External OpenSearch bootstrap requires a central HTTP/HTTPS origin" -}}
{{- end -}}
{{- end -}}
{{- if .Values.bootstrap.requireSecureConnection -}}
{{- if not (regexMatch "^https://[^/?#@[:space:]]+/?$" .Values.bootstrap.url) -}}
{{- fail "Secure OpenSearch bootstrap requires an HTTPS origin without credentials or path" -}}
{{- end -}}
{{- $credential := required "Secure OpenSearch bootstrap requires bootstrap.credentialsSecret" .Values.bootstrap.credentialsSecret -}}
{{- end -}}
{{- if lt (int .Values.bootstrap.activeDeadlineSeconds) 1 -}}
{{- fail "bootstrap.activeDeadlineSeconds must be positive" -}}
{{- end -}}
{{- if lt (int .Values.bootstrap.backoffLimit) 0 -}}
{{- fail "bootstrap.backoffLimit must be nonnegative" -}}
{{- end -}}
{{- end -}}
