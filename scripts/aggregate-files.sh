#!/bin/bash

# This is a refacto of Buerokratt-DSL files transportation

# Set CENTRAL_PATH to the repo root (parent of .github/)
CENTRAL_PATH="$(dirname "$(dirname "$0")")"
CHANGELOG="$CENTRAL_PATH/CHANGELOG.md"

# Hardcoded source repos
SOURCE_REPOS=(
  "buerokratt/Buerokratt-Chatbot:test"
  "buerokratt/Training-Module:test"
  "buerokratt/Analytics-Module:test"
  "buerokratt/Service-Module:test"
)

# Hardcoded version
VERSION="v2"

# Chatbot-specific mappings (e.g., backoffice-related)
CHATBOT_MAPPINGS=(
  "DSL/Ruuter.public/backoffice:Ruuter/public/v2/backoffice"
  "DSL/Ruuter.private/backoffice:Ruuter/private/v2/backoffice"
  "DSL/Resql/backoffice:Resql/backoffice"
#  "DSL/Resql:Resql/backoffice"  # Consolidates training into backoffice
  "DSL/DMapper/backoffice/hbs:dmapper/backoffice/hbs"
  "DSL/CronManager:cronmanager/backoffice"
  "DSL/Liquibase:liquibase/backoffice"
  "DSL/OpenSearch:opensearch/backoffice"
)

# Training-Module-specific mappings (training-related)
TRAINING_MAPPINGS=(
  "DSL/Ruuter.private/training:Ruuter/private/v2/training"
  "DSL/Resql/training:Resql/training"
  "DSL/DMapper/training/hbs:dmapper/training/hbs"
  "DSL/DMapper/training/locations:dmapper/training/locations"
  "DSL/CronManager:cronmanager/training"
  "DSL/Liquibase:liquibase/training"
  "DSL/Pipelines:pipelines/training"
  "DSL/OpenSearch:opensearch/training"
)

# Analytics-Module-specific mappings (analytics-related)
ANALYTICS_MAPPINGS=(
  "DSL/Ruuter/analytics:Ruuter/private/v2/analytics"
  "DSL/Resql/analytics:Resql/analytics"
  "DSL/DMapper/analytics/hbs:dmapper/analytics/hbs"
  "DSL/CronManager:cronmanager/analytics"
  "DSL/Liquibase:liquibase/analytics"
)

# Service-Module-specific mappings (services-related)
SERVICE_MAPPINGS=(
  "DSL/Ruuter/services:Ruuter/private/v2/services"
  "DSL/Resql/services:Resql/services"
  "DSL/DMapper/services/hbs:dmapper/services/hbs"
  "DSL/CronManager/services:cronmanager/services"
  "DSL/Liquibase:liquibase/services"
  "DSL/Pipelines:pipelines/services"
  "DSL/OpenSearch:opensearch/services"
)

TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

declare -A CHATBOT_CHANGES TRAINING_CHANGES ANALYTICS_CHANGES SERVICE_CHANGES

for repo in "${SOURCE_REPOS[@]}"; do
  REPO_NAME="${repo%%:*}"
  REPO_BRANCH="${repo##*:}"
  REPO_DIR="$TEMP_DIR/$(basename "$REPO_NAME")"
  
  echo "Cloning $REPO_NAME into $REPO_DIR"
  git clone --depth 1 --branch "$REPO_BRANCH" "https://github.com/$REPO_NAME.git" "$REPO_DIR"
  
  if [ "$REPO_NAME" = "buerokratt/Buerokratt-Chatbot" ]; then
    MAPPINGS=("${CHATBOT_MAPPINGS[@]}")
    CHANGES_ARRAY="CHATBOT_CHANGES"
  elif [ "$REPO_NAME" = "buerokratt/Training-Module" ]; then
    MAPPINGS=("${TRAINING_MAPPINGS[@]}")
    CHANGES_ARRAY="TRAINING_CHANGES"
  elif [ "$REPO_NAME" = "buerokratt/Analytics-Module" ]; then
    MAPPINGS=("${ANALYTICS_MAPPINGS[@]}")
    CHANGES_ARRAY="ANALYTICS_CHANGES"
  elif [ "$REPO_NAME" = "buerokratt/Service-Module" ]; then
    MAPPINGS=("${SERVICE_MAPPINGS[@]}")
    CHANGES_ARRAY="SERVICE_CHANGES"
  else
    echo "Unknown repo $REPO_NAME - skipping"
    continue
  fi
  
  for mapping in "${MAPPINGS[@]}"; do
    SOURCE_FOLDER="${mapping%%:*}"
    DEST_FOLDER="${mapping##*:}"
    FULL_SOURCE="$REPO_DIR/$SOURCE_FOLDER/"
    FULL_DEST="$CENTRAL_PATH/$DEST_FOLDER/"
    
    if [ -d "$FULL_SOURCE" ]; then
      mkdir -p "$FULL_DEST"
      BEFORE_FILE=$(mktemp)
      AFTER_FILE=$(mktemp)
      find "$FULL_DEST" -type f -exec sha256sum {} + 2>/dev/null | sort -k 3 > "$BEFORE_FILE"
      RSYNC_OUTPUT=$(rsync -av --delete "$FULL_SOURCE" "$FULL_DEST" 2>&1)
      echo "Synced $FULL_SOURCE to $FULL_DEST"
      find "$FULL_DEST" -type f -exec sha256sum {} + 2>/dev/null | sort -k 3 > "$AFTER_FILE"
      
      CHANGES=""
      if echo "$RSYNC_OUTPUT" | grep -qE "^deleting "; then
        CHANGES+="Deleted: $(echo "$RSYNC_OUTPUT" | grep "^deleting " | sed 's/^deleting //')"
      fi
      ADDED_MODIFIED=$(comm -13 "$BEFORE_FILE" "$AFTER_FILE" | cut -c 67-)
      if [ -n "$ADDED_MODIFIED" ]; then
        CHANGES+=" Added/Modified: $ADDED_MODIFIED"
      fi
      
      rm "$BEFORE_FILE" "$AFTER_FILE"
      
      if [ -n "$CHANGES" ]; then
        eval "$CHANGES_ARRAY['$DEST_FOLDER']='$CHANGES'"
      fi
    else
      echo "No $FULL_SOURCE found in $REPO_NAME"
    fi
  done
done

# Generate summary
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
SUMMARY="# Sync Run - $TIMESTAMP\n\n"
ANY_CHANGES=0

for block in "Chatbot" "Training" "Analytics" "Service"; do
  SUMMARY+="## $block Changes\n"
  case "$block" in
    "Chatbot") CHANGES_ARRAY="CHATBOT_CHANGES" ;;
    "Training") CHANGES_ARRAY="TRAINING_CHANGES" ;;
    "Analytics") CHANGES_ARRAY="ANALYTICS_CHANGES" ;;
    "Service") CHANGES_ARRAY="SERVICE_CHANGES" ;;
  esac
  
  eval "changes_count=\${#$CHANGES_ARRAY[@]}"
  if [ "$changes_count" -eq 0 ]; then
    SUMMARY+="No changes detected.\n\n"
  else
    ANY_CHANGES=1
    eval "for dest in \"\${!$CHANGES_ARRAY[@]}\"; do
      SUMMARY+=\"### \$dest\n\"
      SUMMARY+=\"\${$CHANGES_ARRAY[\$dest]}\n\n\"
    done"
  fi
done

# Print to console
echo -e "\n=== Sync Confirmation Summary ==="
echo -e "$SUMMARY"

# Update changelog with newest first
TEMP_CHANGELOG=$(mktemp)
echo -e "$SUMMARY" > "$TEMP_CHANGELOG"

if [ -f "$CHANGELOG" ]; then
  # Extract existing content after header
  tail -n +4 "$CHANGELOG" >> "$TEMP_CHANGELOG"  # Skip "# Changelog\n\nAll changes...\n"
fi

# Write back with header
{
  echo -e "# Changelog\n"
  echo -e "All changes to Buerokratt-DSL from source repos.\n"
  cat "$TEMP_CHANGELOG"
} > "$CHANGELOG"

rm "$TEMP_CHANGELOG"
