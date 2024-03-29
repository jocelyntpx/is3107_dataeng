# IS3107 - Data Engineering Project

In this project, we want to build a data warehouse which stores information of stocks on SGX, to provide business and personal traders with comprehensive data and insights to make better investment decisions. y creating an End-to-End Extract, Transform, Load (ETL) pipeline to automate data flow from the different sources to our data warehouse, we can facilitate avid and amateur investors to have a better decision-making process and make smarter data-driven investment decisions. Ultimately, it aims to value-add investors who are interested in the Singapore stock market and its surrounding players in a streamlined process. 

## User Guide to setting up our group's project code
Step 1:
- Install VirtualBox and import MyLinuxServer.ova
- Access VM through visual studio code via SSH
- Create virtual environment and install airflow using tutorial 3 slides

Step 2:
- Install mongodb using tutorial 7 slides
- In the venv command line, run "pip install -r requirements.txt"
- Set up postgres connection in airflow

step 3:
- Connect to postgresql `sudo -u postgres psql`
- Create a stock_db table `CREATE DATABASE stock_db;`

Step 3:
- Under the airflow folder, import the 4 folders ("DAG", "scripts", "sql", "keys") under it
- Note: The "DAG" folder contains all our DAG files, "scripts" folder stores the functions we are calling in our DAG files, "sql" folder helps to create the yfinance tables and "keys" folder contain our google cloud connection key.

Step 4:
- Configure your environment to allow parallel processing 
- Configure a postgresql backend database : https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html
```console 
CREATE DATABASE airflow_db;
CREATE USER airflow_user WITH PASSWORD 'airflow_pass';
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;
ALTER USER airflow_user WITH SUPERUSER;
```
- Edit your airlfow.cfg file 
```console 
executor = LocalExecutor
sql_alchemy_conn = postgresql+psycopg2://airflow_user:airflow_pass@localhost/airflow_db
```
Step 5:
- In the venv command line, run `airflow webserver --port 8080`
- In another terminal, run `airflow scheduler`
- Go to localhost:8080 

## To run twitter, reddit, stock news DAG
- In a new terminal, run `sudo systemctl start mongod`
- In another terminal, go into the scirpts directory and run "python tweetpy_call.py" to get some data into your local machine. This mocks the starting of the data stream on an external server.
- In your airflow homepage, run the 'retrieve_daily_textual_data' dag

## To run yfinance DAG
- Create a google cloud connection in airflow with your respecitve key.json and name it "bq_conn"
- run 'stocks_esg_dag' dag and it will trigger 'stock_esg_google_cloud_dag' dag at the end
- run 'stocks_info_dag' dag and it will trigger 'stock_info_google_cloud' dag at the end
- run 'stocks_price_analysis' and it will 'stock_price_google_cloud' dag at the end
