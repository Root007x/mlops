from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook 
import pendulum
import json


## Define the dag

with DAG(
    dag_id = "nasa_apod_postgres",
    start_date = pendulum.now().subtract(days=1),
    schedule= "@daily",
    catchup=False
) as dag:
    
    ## Step 1: Create the table if it doesn't exist
    
    @task
    def create_table():
        postgres_hook = PostgresHook(postgres_conn_id = "my_postgres_connection")

        ## SQL quary to create the table
        create_table_quary = """
        CREATE TABLE IF NOT EXISTS apod_data(
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            data DATE,
            media_type VARCHAR(50)
        )
        """
        ## Execute the table creation query
        postgres_hook.run(create_table_quary)

    ## Step 2: Extract the NASA API data
    ## https://api.nasa.gov/planetary/apod?api_key=Y4nqa6Khi8mQz3YyVAD15UGcGNecsbhGqqCNkpzt
    # API request
    extract_apod = HttpOperator(
        task_id = "extract_apod",
        http_conn_id = "nasa_api",
        endpoint = "planetary/apod",
        method = "GET",
        data = {"api_key": "{{ conn.nasa_api.extra_dejson.api_key }}"},
        response_filter = lambda response:response.json(),
    )


    ## Step 3: Transform the data
    @task
    def transform_apod_data(response):
        apod_data = {
            "title": response.get("title", ""),
            "explanation": response.get("explanation", ""),
            "url": response.get("url",""),
            "date": response.get("date", ""),
            "media_type": response.get("media_type", "")
        }

        return apod_data

    ## Step 4: Load the data into postgres SQL
    @task
    def load_data_to_postgres(apod_data):
        postgres_hook = PostgresHook(postgres_conn_id = "my_postgres_connection")


        ## Define the sql insert query
        insert_quary = """
            INSERT INTO apod_data (title,explanation, url, data, media_type)
            VALUES (%s, %s, %s, %s, %s)
        """

        postgres_hook.run(insert_quary, parameters = (
            apod_data["title"],
            apod_data["explanation"],
            apod_data["url"],
            apod_data["date"],
            apod_data["media_type"],
        ))

    ## step 5: verify the data DBViwer
    

    ## Step 6: Define the task dependencies
    ## Extract
    create_table() >> extract_apod ## Ensure the table is create before extraction
    api_response = extract_apod.output 
    # Transform
    transformed_data = transform_apod_data(api_response)
    # Load
    load_data_to_postgres(transformed_data)
