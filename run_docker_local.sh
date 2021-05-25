#!/bin/bash

docker run \
--net=host \
-v /mnt/output:/opt/output \
-v /opt/logs/:/opt/logs \
-v /opt/jira:/opt/jira \
-e JIRA_CONF=/opt/jira/jira_config.json \
-e FILE_LOGS=1 \
-e CLEAN_UP=0 \
-e JIRA_FILL=0 \
-e INGESTION_STACK_URL="http://ingestion-stack-3d-model-ingestion-service-route-3d.apps.v0h0bdx6.eastus.aroapp.io" \
-e INGESTION_CATALOG_URL="http://ingestion-stack-3d-ingestion-catalog-route-3d.apps.v0h0bdx6.eastus.aroapp.io" \
-e INGESTION_JOB_SERVICE_URL="http://ingestion-stack-discrete-ingestion-db-route-3d.apps.v0h0bdx6.eastus.aroapp.io" \
-e TMP_DIR="/tmp/auto_3rd" \
-e ENVIRONMENT_NAME=dev \
-e S3_EXPORT_STORAGE_MODE=True \
-e S3_ACCESS_KEY="raster" \
-e S3_SECRET_KEY="rasterPassword" \
-e S3_END_POINT="http://10.8.1.13:9000/" \
-e S3_BUCKET_NAME="ingestion-stack" \
-e S3_DOWNLOAD_DIR="/tmp" \
3rd-automation-test:latest


