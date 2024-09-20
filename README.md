# Truck Pipeline

### Overview
This project implements an ETL data pipeline that connects an S3 bucket to a redshift database.  
The `pandas` library is used to read and clean the data whilst `redshift connector` is used for loading.
This project also contains the files necessary to terraform an ECS task, AWS lambda function and AWS eventbridge.
The pipeline is modular and is contained across the `pipeline.py`, `extract.py`, `transform.py` and `load.py` files within the `pipeline/` folder.
A dashboard that analyses the truck data is stored in the `dashboard/` folder, this uses `streamlit` and has a Dockerfile associated so that it can be run as an ECS task on AWS.
A lambda function that composes a daily report using the `jinja2` library is contained within the `lambda/` folder. This was used with AWS step-function, AWS eventbridge and AWS SES to email the daily report. This was not terraformed and requires setup through AWS UI.

### Installation
1. Clone the repository:
```bash
git clone https://github.com/AlexOBarnes/Trucks-ETL-Pipeline.git
```

2. This project requires a prepared S3 bucket and redshift cluster on AWS. This can be provisioned through the AWS UI

3. Move into each folder and follow the instructions within each in the following order:
    - Database
    - Pipeline
    - Lambda
    - Dashboard
    - Terraform

