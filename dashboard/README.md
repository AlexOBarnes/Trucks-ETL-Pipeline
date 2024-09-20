# Truck Dashboard

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
    - `DB_NAME`

The *.py files use environment variables and the names of these can be changed easily to match your .env format.
## Usage
To run the dashboard locally:
```bash
steamlit run homepage.py
```
To run the dockerised dashbaord:
```bash
docker run -p 8501:8501  --env-file .env  [image_name]
```

### How it works
#### `homepage.py`
- Runs `streamlit` dashboard
- Imports vega-altair graphs from `graphs.py`
- Links to `pages/` folder and runs additional navigable pages
#### `graphs.py`
- Uses `pandas` and `vega-altair` to transform and visualise the data from the redshift cluster
#### `pages/`
- Contains additional pages which import graphs from `graphs.py`