import sys
import re
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import to_json, struct

# Initialize Glue context
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
logger = glueContext.get_logger()

# Path to your input log files in S3
input_path = "s3://yonatan-s3-bucket/raw_logs/"
output_path = "s3://yonatan-s3-bucket/parsed_logs_json/"

# Read the log files into a DataFrame
log_df = spark.read.text(input_path)

# Define a regex pattern to match log entries
log_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}), (\w+): (.*?)(?:, \((\w+)\))?$'


# Function to parse a single log line
def parse_log_line(line):
    matches = re.match(log_pattern, line)
    if matches:
        return matches.groups()
    else:
        return (None, None, None, None)


# Parse the logs using the regex
parsed_logs = log_df.rdd.map(lambda row: parse_log_line(row[0]))

# Convert to a DataFrame
columns = ['timestamp', 'level', 'message', 'id']
parsed_df = spark.createDataFrame(parsed_logs, columns)

# Filter out any rows where parsing failed (i.e., all fields are None)
parsed_df = parsed_df.filter(parsed_df.timestamp.isNotNull())

# Convert each row to a JSON string
json_df = parsed_df.select(to_json(struct(*parsed_df.columns)).alias("json_data"))

# Write the JSON strings to a text file, one JSON object per line
json_df.write.text(output_path)

logger.info("Log parsing completed and saved in JSON format.")
