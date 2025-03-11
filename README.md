# aiKey - Medical Platform For Doctor Use

## Introduction
This platform allows doctors to access patient records across various systems. We assume that patient medical data comes from multiple platforms, with a large volume of records stored in cloud storage. To process and organize this data, we use Cloud Scheduler to trigger a data pipeline in DataFlow, which then stores the structured results in Cloud SQL.

The platform supports two user roles: "AIPHAS" and "DOCTOR." Role-based access control ensures that users with different roles can access distinct APIs. This setup allows AIPHAS employees to manage user accounts, while doctors can view patient data.

To improve data retrieval efficiency, we utilize Redis as a cache.

## Data Flow
![Architecture](https://github.com/lyoudr/aiKey/blob/main/diagram.png)
![Architecture]()

## Tools Used
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
- Cache
    - Redis
- CronJob
    - Cloud Scheduler
- WebSocket

## Start the project
Create virtual environment
```
python3.11 -m venv ai_venv
```
Activate virtual environment
```
source ai_venv/bin/activate
```
Install required pacakges
```
pip install -r requirements.txt
```
Start the application
```
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```
See API document in 
http://127.0.0.1:8000/docs

## DataBase Migration
```
alembic upgrade head
```

## DataBase Trigger for instant data display 
Create a Trigger Function
```
CREATE OR REPLACE FUNCTION notify_new_data() RETURNS TRIGGER AS $$
BEGIN
    PERFORM pg_notify('new_data_channel', row_to_json(NEW)::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql; 
```

Create Trigger for `patient_cost` Table
```
CREATE TRIGGER new_data_trigger
AFTER INSERT ON patient_cost
FOR EACH ROW
EXECUTE FUNCTION notify_new_data();
```

Listen to database event
```
async def listen_for_db_notification():
    """Listen for PostgreSQL notifications and push to WebSocket clients."""
    if os.getenv("ENV") == "local":
        dsn = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@localhost/{settings.DB_NAME}"
    else:
        dsn = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@/{settings.DB_NAME}?host=/cloudsql/{settings.DB_INSTANCE}"
    
    conn = psycopg2.connect(dsn)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    cursor.execute("LISTEN new_data_channel;")
    logger.info("Listening for new data...")

    while True:
        select.select([conn], [], [])
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            logger.info(f"New data received: {notify.payload}")
            # Send the notification to WebSocket clients
            await send_to_frontend(notify.payload)
```

## Seed Initial Data
```
python seed_data.py
```

## Build Service
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

- Add Push Subscription
```
gcloud pubsub subscriptions create medical-analysis-sub \
--topic=medical-analysis \
--push-endpoint=$CLOUD_RUN_URL/process/ \
--push-auth-service-account=$SERVICE_ACCOUNT
```

- Create Redis Instance
```
gcloud redis instances create my-redis \
--size=1 \
--region=us-central1 \
--network=default
```

- Set up Serverless VPC Access Connector
```
gcloud compute networks vpc-access connectors create my-connector \
--region=us-central1 \
--network=default \
--range=10.8.0.0/28
```

- Deploy to Cloud Run
```
gcloud run deploy aikey \
--image asia-east1-docker.pkg.dev/YOUR_PROJECT_ID/ann-repo/ai-key:latest \
--platform managed \
--region asia-east1 \
--allow-unauthenticated \
--set-env-vars DB_USER=$DB_USER,DB_PASS=$DB_PASS,DB_NAME=$DB_NAME,DB_INSTANCE=$DB_INSTANCE,DB_SOCKET_PATH=/cloudsql/<instance_connection_url> \
--add-cloudsql-instances=<instance_connection_url> \
--vpc-connector=ann-connector
```

- Create Cloud Scheduler to get medical record periodically
```
gcloud scheduler jobs create http your-job-name \
  --schedule "0 1 * * *" \
  --time-zone "Asia/Taipei" \
  --uri "https://your-cloud-run-url" \
  --http-method POST \
  --oidc-service-account-email "your-service-account@your-project.iam.gserviceaccount.com" \
  --oidc-token-audience "https://your-cloud-run-url" \
  --description "Daily job to trigger the Cloud Run service"
```