
* Create a DataFlow Classic Template
```
python -m src.services.medical_analysis \
--runner DataflowRunner \
--project ann-project-390401 \
--staging_location gs://medical_ann/staging \
--template_location gs://medical_ann/templates/medical_service_template \
--region asia-east1 \
--dataflow_service_options=enable_preflight_validation=false
--requirements_file path/to/requirements.txt
```

* Run the Job on DataFlow
```
gcloud dataflow jobs run medical-service-job \
--gcs-location gs://medical_ann/templates/medical_service_template \
--region asia-east1
```

* add `src` as system path
```
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
```

* install apache beam
```
pip install 'apache-beam[gcp]'
```