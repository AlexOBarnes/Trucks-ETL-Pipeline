source .env
export PGPASSWORD=$DB_PASSWORD
psql -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME -c "SET search_path TO $DB_SCHEMA;" -f schema.sql