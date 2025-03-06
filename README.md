# aiKey - Medical Platform for doctor use

## Tools Used
---
- FrameWork
    - FastAPI
- DataBase 
    - PostgreSQL
- Storage
    - Cloud Storage
- Notification
    - Pub/Sub
- DataPipeline
    - Apache Beam
    - DataFlow

## Build Service
---
- Create a DataFlow Classic Template
    -  requirements.txt should be in the same folder as medical_analysis.py 
```
python -m src.services.medical_analysis \
--runner DataflowRunner \
--project YOUR_PROJECT_ID \
--staging_location gs://YOUR_BUCKET_NAME/staging \
--template_location gs://YOUR_BUCKET_NAME/templates/medical_service_template \
--region asia-east1 \
--dataflow_service_options=enable_preflight_validation=false
--requirements_file path/to/requirements.txt
```

- Run the Job on DataFlow
```
gcloud dataflow jobs run medical-service-job \
--gcs-location gs://YOUR_BUCKET_NAME/templates/medical_service_template \
--region asia-east1
```

- Create a Pub/Sub Topic 
```
gcloud pubsub topics create medical-analysis
```

- Configure Cloud Storage to Publish Events to Pub/Sub
    - Pub/Sub notifications sends information about changes to objects in your buckets to Pub/Sub, where the information is added to a Pub/Sub topic of your choice in the form of messages.
    - OBJECT_FINALIZE: Sent when a new object (or a new generation of an existing object) is successfully created in the bucket. This includes copying, rewriting, or restoring an existing object.
```
gcloud storage buckets notifications create gs://YOUR_BUCKET_NAME \
    --topic=medical-analysis \
    --event-types=OBJECT_FINALIZE
```

- List notification configurations for a bucket
```
gcloud storage buckets notifications list gs://YOUR_BUCKET_NAME
```

- Authenticate Cloud Run to Artifact Registry
```
gcloud auth configure-docker asia-east1-docker.pkg.dev
```

- Build and Push Docker Image to Artifact Registry
```
gcloud builds submit --tag asia-east1-docker.pkg.dev/YOUR_PROJECT_ID/ann-repo/ai-key:latest
```

- Deploy to Cloud Run
```
gcloud run deploy aikey \
--image asia-east1-docker.pkg.dev/YOUR_PROJECT_ID/ann-repo/ai-key:latest \
--platform managed \
--region asia-east1 \
--allow-unauthenticated \
--set-env-vars DB_USER=$DB_USER,DB_PASS=$DB_PASS,DB_NAME=$DB_NAME,DB_INSTANCE=$DB_INSTANCE,DB_SOCKET_PATH=/cloudsql/<instance_connection_url> \
--add-cloudsql-instances=<instance_connection_url>
```

- Add Push Subscription
```
gcloud pubsub subscriptions create medical-analysis-sub \
--topic=medical-analysis \
--push-endpoint=$CLOUD_RUN_URL/process/ \
--push-auth-service-account=$SERVICE_ACCOUNT
```