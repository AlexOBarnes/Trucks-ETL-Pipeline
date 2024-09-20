# Truck Database

## Setup
1. Create a .env containing the following:
    - `DB_HOST`
    - `DB_PORT`
    - `DB_USER`
    - `DB_PASSWORD`
    - `DB_SCHEMA`
    - `DB_NAME`

## Usage
Once the redshift cluster has been setup run the following commands
```bash
psql -h [redshift-cluster-endpoint] -U [username] -p 5439
```
If you have schemas setup in this redshift cluster identify the schema you wish to use and set the .env variable accordingly.
```SQL
SET search_path TO [DB_schema]
CREATE DATABASE [DB_NAME]
```  
With the database setup run the following:
```bash
bash reload.sh
```
This will setup the tables with static data.  
 
### How it works

#### reset.sh
Included within this repository are shell scripts that make managing the redshift database more easy.  
`reset.sh` truncates the transaction table but leaves the other static tables intact.

#### connect.sh
This script is used to more speedily connect to the database. To use run the following:
```bash
bash connect.sh
```
#### reload.sh
This script reruns the schema.sql contained within this repository, which drops all of the tables and recreates them from scratch.  
Use the following to run this script:
```bash
bash reload.sh
```
