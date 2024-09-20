# Truck Report Lambda

## Installation
1. Install the required Python packages:

```bash
pip install -r requirements.txt
```
Requirements.txt file includes all dependencies including: `redshift connector`, `jinja2`, and `python-dotenv`.

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

In this project the lambda function was dockerised and pushed to a prepared ECR repository. Then an AWS step function was setup through the UI that connected this lambda to AWS SES. The output of the lambda was used in the contents of the email and this step function was triggered using AWS eventbridge.

## Usage
Once dockerised and pushed to AWS ECR use the AWS UI to test the lambda function.
Alternative modify the handler function to take no inputs and run using the following:
```bash
python main.py
```

### How it works
#### `main.py`
- Uses `jinja2` to read in the template and fill it with data queried using `redshift-connector`
#### `template.html`
- Contains the HTML template that is filled by the lambda function