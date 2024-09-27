# ETL Pipeline and Interactive Log Analysis Dashboard Using AWS Services and Dash

## Project Overview

This project builds an ETL pipeline using AWS services to process raw log data, store it in a structured format, and create an interactive dashboard with **Python Dash** to visualize and analyze the data.

The pipeline includes:
- Extracting data using **AWS Glue Crawlers**.
- Transforming and cleaning log data with **AWS Glue Jobs**.
- Storing the cleaned data back into **S3**.
- Querying the transformed data with **AWS Athena**.
- Visualizing and interacting with the data through a **Python Dash** dashboard.

---

## Architecture Overview

1. **Raw Data Source (S3)**:
   - Store raw log files (e.g., web server/application logs) in **AWS S3**.

2. **ETL Process**:
   - **Extract**: Use **AWS Glue Crawlers** to scan the raw logs and automatically catalog the data into structured formats (e.g., JSON/CSV) stored in the **Glue Data Catalog**.
   - **Transform**: Use **AWS Glue Jobs** to clean and filter the logs (e.g., remove `INFO` level logs, extract useful columns like `timestamp` and `log_level`).
   - **Load**: Save the cleaned, structured data back to **S3** in a format like **CSV** or **Parquet**.

3. **Data Querying**:
   - Use **AWS Athena** to run SQL queries on the transformed log data stored in S3.

4. **Data Visualization**:
   - Use **Python Dash** to create an interactive dashboard that lets users filter and visualize the log data based on parameters such as log levels and date ranges.

---

## Steps to Reproduce the Project

### 1. Set Up Raw Log Data on S3

1. Upload raw log files (e.g., web server logs) to an S3 bucket.
   - Example folder structure:  
     ```
     s3://your-bucket/logs/raw/
     ```

### 2. Extract Data with AWS Glue Crawlers

1. Create an **AWS Glue Crawler** to scan the S3 location of the raw logs.
2. The crawler will create a table in the **Glue Data Catalog** that describes the schema and location of the log data.

### 3. Transform Data with AWS Glue Jobs

1. Write an **AWS Glue Job** in Python to clean and transform the log data:
   - Parse the raw logs.
   - Filter out irrelevant log levels (e.g., `INFO`).
   - Save the transformed data back to **S3** in a structured format (e.g., **CSV** or **Parquet**).

2. Example output folder:
   ```
   s3://your-bucket/logs/cleaned/
   ```

### 4. Query Data with AWS Athena

1. Use **AWS Athena** to query the transformed data stored in S3.
2. Write SQL queries to perform analysis on the logs, such as:
   - Counting the number of `ERROR` logs per day.
   - Filtering logs by log level and date range.

### 5. Build the Interactive Dashboard with Python Dash

1. Create a **Python Dash** app that provides interactive data visualizations based on the log data.
   - Use **Boto3** to run **Athena queries** in the background and fetch results based on user input.
   - Add filters (e.g., log level, date range) and display the queried data in tables or charts.

2. Example Dashboard Features:
   - A dropdown to select log levels (`ERROR`, `WARNING`, `INFO`).
   - A date picker to select a date range.
   - A time-series chart showing the frequency of log events over time.

---

## Project Structure

```
|-- etl_pipeline/
    |-- glue_jobs/
        |-- transform_log_data.py   # Glue Job Python script for data transformation
    |-- dash_app/
        |-- app.py                  # Dash app script for visualization
        |-- assets/
            |-- style.css           # CSS styling for the dashboard (optional)
```

---

## Technology Stack

- **AWS S3**: For storing raw and cleaned log data.
- **AWS Glue Crawlers**: For automatically cataloging raw log data into structured metadata tables.
- **AWS Glue Jobs**: For cleaning and transforming the log data.
- **AWS Athena**: For querying the transformed data stored in S3.
- **Python Dash**: For building an interactive dashboard to visualize and analyze the log data.

---

## Setup and Deployment

### 1. AWS Setup

1. Set up **AWS S3**, **AWS Glue Crawlers**, **Glue Jobs**, and **AWS Athena** services in your AWS environment.
2. Ensure appropriate **IAM roles and permissions** are configured to allow Glue Jobs and Crawlers to access S3, and for Athena to query S3.

### 2. Python Dash App Setup

1. Clone the repository.
   ```bash
   git clone https://github.com/your-repo/etl-log-analysis-dashboard.git
   cd etl-log-analysis-dashboard
   ```

2. Install required Python libraries:
   ```bash
   pip install dash boto3 pandas
   ```

3. Run the Dash app:
   ```bash
   python app.py
   ```

---

## Example Use Case

- **Goal**: Process web server logs to identify error trends.
  - **Step 1**: Store raw log files on S3.
  - **Step 2**: Use AWS Glue Crawlers to catalog log data.
  - **Step 3**: Use AWS Glue Jobs to filter out `INFO` logs and store cleaned logs back in S3.
  - **Step 4**: Query the cleaned data with Athena.
  - **Step 5**: Use the Dash app to visualize and interact with the log data (e.g., filtering errors by date and log level).

---

## Optional Enhancements

- **Add caching**: Implement caching in Dash to store frequently queried Athena results and improve performance.
- **Authentication**: Add user authentication to restrict access to sensitive log data.
- **Real-time log processing**: Use AWS Kinesis or Kafka for real-time log ingestion and processing.