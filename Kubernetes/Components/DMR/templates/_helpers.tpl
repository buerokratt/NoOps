{{- define "dmr.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "dmr.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name (include "dmr.name" .) | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- define "dmr.labels" -}}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" }}
app.kubernetes.io/name: {{ include "dmr.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "dmr.serverName" -}}
{{- printf "%s-server" (include "dmr.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "dmr.rabbitmqName" -}}
{{- default (printf "%s-rabbitmq" (include "dmr.fullname" .)) .Values.rabbitmq.name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "dmr.rabbitmqHost" -}}
{{- if .Values.rabbitmq.external.host }}{{ .Values.rabbitmq.external.host }}{{ else }}{{ include "dmr.rabbitmqName" . }}{{ end }}
{{- end }}

{{- define "dmr.rabbitmqManagementUri" -}}
{{- if .Values.rabbitmq.external.managementUri }}{{ .Values.rabbitmq.external.managementUri }}{{ else }}http://{{ include "dmr.rabbitmqHost" . }}:15672{{ end }}
{{- end }}

{{- define "dmr.rabbitmqSecret" -}}
{{- if .Values.rabbitmq.auth.existingSecret }}{{ .Values.rabbitmq.auth.existingSecret }}{{ else }}{{ include "dmr.rabbitmqName" . }}-default-user{{ end }}
{{- end }}

{{- define "dmr.agentName" -}}
{{- printf "%s-agent-%s" (include "dmr.fullname" .root) .agent.name | trunc 63 | trimSuffix "-" }}
{{- end }}

