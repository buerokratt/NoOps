{{- define "opensearch.bootstrap.validate" -}}
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
