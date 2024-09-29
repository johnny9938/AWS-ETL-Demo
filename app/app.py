import time
import re  # For regex to check dangerous SQL keywords

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import boto3

# Initialize the Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Initialize Boto3 Athena client
athena_client = boto3.client('athena', region_name='eu-north-1')  # Replace with your region

# Layout of the app
app.layout = dbc.Container(
    [
        html.Div(
            style={
                'background': 'linear-gradient(to right, #ff7e5f, #feb47b)',  # Gradient background
                'padding': '20px',
                'border-radius': '8px'
            },
            children=[
                html.H1("Log Analysis Dashboard", style={'text-align': 'center', 'color': 'white'}),

                dcc.Dropdown(
                    id='table-dropdown',
                    options=[],  # Options will be filled dynamically
                    placeholder="Select a table from Glue Data Catalog",
                ),
                dcc.Textarea(
                    id='sql-query-input',
                    placeholder='Enter your SQL query here...',
                    style={'width': '100%', 'height': '100px'},
                ),
                dbc.Button("Execute Query", id='execute-query-button', color='primary', className='mt-2'),

                html.Div(id='query-output', className='mt-3'),

                # Table for displaying query results
                html.Div(id='log-table-container', style={'margin-top': '20px'}),

                # Table for displaying executed queries
                html.H2("Executed Queries", className='mt-4', style={'color': 'white'}),
                dcc.Store(id='executed-queries-store', data=[]),  # Store for executed queries
                html.Div(id='executed-queries-table')
            ]
        )
    ],
    fluid=True
)


# Callback to populate the table dropdown from Glue Data Catalog
@app.callback(
    Output('table-dropdown', 'options'),
    Input('execute-query-button', 'n_clicks')
)
def populate_table_dropdown(n_clicks):
    # Fetch tables from Glue Data Catalog
    glue_client = boto3.client('glue', region_name='eu-north-1')  # Replace with your region
    response = glue_client.get_tables(DatabaseName='yonatan-n-glue-db')  # Replace with your database name
    tables = [{'label': table['Name'], 'value': table['Name']} for table in response['TableList']]
    return tables


# Callback to update the SQL query input based on the selected table
@app.callback(
    Output('sql-query-input', 'value'),
    Input('table-dropdown', 'value')
)
def update_sql_query(selected_table):
    if selected_table:
        # Provide a default query with the selected table
        return f"SELECT * FROM \"yonatan-n-glue-db\".\"{selected_table}\" LIMIT 10;"
    return ""

# Callback to execute the SQL query
@app.callback(
    Output('query-output', 'children'),
    Output('log-table-container', 'children'),
    Output('executed-queries-store', 'data'),
    Input('execute-query-button', 'n_clicks'),
    State('sql-query-input', 'value'),
    State('table-dropdown', 'value'),
    State('executed-queries-store', 'data'),
    prevent_initial_call=True
)
def execute_query(n_clicks, query, selected_table, executed_queries):
    if n_clicks and query and selected_table:
        # Check for forbidden queries (like DELETE)
        forbidden_keywords = ['DELETE', 'DROP', 'UPDATE', 'INSERT']
        if any(keyword in query.upper() for keyword in forbidden_keywords):
            return f"Error: Forbidden SQL query detected: {query}", "", executed_queries

        # Execute the query in Athena
        response = athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': 'yonatan-n-glue-db'  # Replace with your database name
            },
            ResultConfiguration={
                'OutputLocation': 's3://yonatan-s3-bucket/athena-results/'  # Replace with your output S3 bucket
            }
        )

        # Get the query execution ID and poll for query completion
        query_execution_id = response['QueryExecutionId']
        while True:
            query_status_response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
            status = query_status_response['QueryExecution']['Status']['State']
            if status == 'SUCCEEDED':
                break
            elif status in ['FAILED', 'CANCELLED']:
                return f"Query failed or was cancelled: {status}", "", executed_queries
            time.sleep(1)

        # Fetch the results
        results = athena_client.get_query_results(QueryExecutionId=query_execution_id)
        rows = results['ResultSet']['Rows']

        # Prepare DataFrame from results
        headers = [col['VarCharValue'] for col in rows[0]['Data']]
        data = [[col.get('VarCharValue', '') for col in row['Data']] for row in rows[1:]]  # Skip header

        # Create a DataFrame for display
        result_df = pd.DataFrame(data, columns=headers)

        # Create a table for displaying query results
        log_table = dbc.Table.from_dataframe(result_df, striped=True, bordered=True, hover=True)

        # Append executed query to the list, and ensure the store is a list
        if executed_queries is None:
            executed_queries = []
        executed_queries.append(query)

        return f"Executed Query: {query}", log_table, executed_queries

    return "", "", executed_queries



# Layout for displaying executed queries
@app.callback(
    Output('executed-queries-table', 'children'),
    Input('executed-queries-store', 'data')
)
def update_executed_queries_table(executed_queries):
    if executed_queries:
        return dbc.Table.from_dataframe(pd.DataFrame({'Executed Queries': executed_queries}), striped=True)
    return html.Div("No queries executed yet.")


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
