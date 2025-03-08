from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import secretmanager
from datetime import datetime
import apache_beam as beam
import csv 
import argparse

# Function to access secret from Google Secret Manager
def access_secret_version(secret_id):
    """
    Access the payload for the given secret version from Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/ann-project-390401/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=secret_name)
    # Return the decoded secret payload
    return response.payload.data.decode('UTF-8')


SERVICE_ACCOUNT = access_secret_version("SERVICE_ACCOUNT")
GCS_BUCKET = access_secret_version("GCS_BUCKET")
REGION = access_secret_version("REGION")

# Step 1: Parse the CSV file to create a list of dictionaries
def parse_csv(line):
    reader = csv.reader([line])
    fields = next(reader)
    
    # Return the record as a dictionary
    return {
        "id": int(fields[0]),
        "patient_id": int(fields[1]),
        "record_date": fields[2],
        "diagnosis": fields[3],
        "treatment": fields[4],
        "prescription": fields[5],
        "cost": float(fields[6]),
        "notes": fields[7],
        "created_time": fields[8],
        "updated_time": fields[9]
    }


# Step 2: Extract the month from the 'record_date'
def extract_month(record):
    try:
        record_date = datetime.strptime(record['record_date'], '%Y-%m-%d')
        month = record_date.strftime('%Y-%m')
        return (record['patient_id'], month), record['cost']
    except ValueError:
        # Handle the case where the date is not in the expected format
        print(f"Skipping record with invalid date format: {record['record_date']}")
        return None  # Skip this record


# Step 3: Sum the costs for each patient per month
def sum_costs(patient_month, cost_iter):
    total_cost = sum(cost_iter)
    return {
        'patient_id': patient_month[0],
        'month': patient_month[1],
        'total_cost': total_cost
    }

def run_pipeline(gcs_path: str, save_main_session=True):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        default=f'gs://{GCS_BUCKET}/medical/*.csv',
        help='Input file to process.'
    )
    pipeline_options = PipelineOptions(
        runner='DataflowRunner',
        project='ann-project-390401',
        job_name='medical-service',
        region=REGION,
        service_account_email=SERVICE_ACCOUNT,
        save_main_session=True,
        temp_location=f'gs://{GCS_BUCKET}/temp/',
        staging_location=f'gs://{GCS_BUCKET}/staging/',
        template_location=f'gs://{GCS_BUCKET}/templates/medical_service_template',
        enable_preflight_validation=False,
    )
    # pipeline_options_local = PipelineOptions(
    #     runner='DirectRunner'  # Runs locally
    # )
    with beam.Pipeline(options=pipeline_options) as p:
        (p
         | 'Read CSV File' >> beam.io.ReadFromText(gcs_path, skip_header_lines=1)
         | 'Parse CSV' >> beam.Map(parse_csv)
         | 'Extract Month and Patient ID' >> beam.Map(extract_month)
         | 'Group by Patient and Month' >> beam.GroupByKey()
         | 'Sum Costs' >> beam.MapTuple(sum_costs)
         | 'Write to GCS' >> beam.io.WriteToText(
            f'gs://{GCS_BUCKET}/output/medical_service_results',  # The output path in GCS
            file_name_suffix='.csv',  # Ensure the file has a .csv extension
            shard_name_template='',  # Disable sharding
            num_shards=1  # Force a single output file
         )
        )


if __name__ == "__main__":
    run_pipeline(
        f'gs://{GCS_BUCKET}/medical/*.csv'
    )