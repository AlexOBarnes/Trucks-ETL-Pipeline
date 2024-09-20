# Truck Pipeline

## Installation
1. Install the required Python packages:

```bash
pip install -r requirements.txt
```
Requirements.txt file includes all dependencies including: `redshift connector`, `pandas`, and `python-dotenv`.

2. Make sure the pipeline runs locally and can connect to the prepared S3 bucket and redshift database.

3. If you wish to deploy this project to the cloud run the following commands:
```bash
docker build -t [example_name] . --platform "linux/amd64"
```
Create an ECR repository on AWS, this can be done through terraform or through the UI, then authenticate using AWS cli.
```bash
brew install awscli
aws ecr get-login-password --region [region-of-choice]| docker login --username AWS --password-stdin [ECR-URI]
```
Then tag your docker image and push to the ECR repository.
```bash
docker tag [example_name]:[ECR-URI]
docker push [ECR-URI]
```

## Setup
In order to run the script users must create a .env file containing the following things.
- `redshift connector` requirements:
    - `DB_HOST`
    - `DB_PORT`
    - `DB_USER`
    - `DB_PASSWORD`
    - `DB_SCHEMA`  
- `boto3` requirements:
    - `AWS_ACCESS_KEY`
    - `AWS_SECRET_ACCESS_KEY`
    - `BUCKET` 

The *.py files use environment variables and the names of these can be changed easily to match your .env format.

## Usage
To run the pipeline:
```bash
python pipeline.py
```
Additional `-l` argument can be added to log to file.

## How it works

#### `pipeline.py`
- Calls all other functions in the ETL pipeline.
- Takes command line arguments in order to configure the logging of the pipeline.
#### `extract.py`
- Uses the `io` and `boto3` libraries to extract data from the S3 bucket, currently it checks the time of creation (which is stored in the file name) and only extracts files created in the last 3 hours.
- Returns a `pandas` dataframe containing all the truck data.
#### `transform.py`
- Uses `pandas` to removes erroneous, extreme or missing data 
- Returns a list of the cleaned data ready for upload.
#### `load.py`
- Uses `redshift-connector` to upload data to a redshift database