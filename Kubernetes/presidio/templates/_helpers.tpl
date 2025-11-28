{{- define "anonymizer.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" | lower -}}
{{- end }}

{{- define "anonymizer.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" | lower -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name (include "anonymizer.name" .) | trunc 63 | trimSuffix "-" | lower -}}
{{- end -}}
{{- end }}
