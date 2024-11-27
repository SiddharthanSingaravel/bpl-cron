import requests
import pandas as pd
import time
import random
import logging
logging.basicConfig(level=logging.INFO)

# API endpoint for the dataset
url = 'https://data.boston.gov/api/3/action/datastore_search'

# Define the parameters for your query
params = {
    'resource_id': 'c13199bf-49a1-488d-b8e9-55e49523ef81',  # Resource ID of the dataset
    'limit': 1000,  # Max number of records to fetch per request
}

# Function for retry logic with exponential backoff
def fetch_data_with_retry(url, params, retries=3, backoff_factor=1.5):
    for attempt in range(retries):
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        
        print(f'Error: {response.status_code}. Retrying in {backoff_factor ** attempt} seconds...')
        logging.error(f'Error: {response.status_code}. Retrying in {backoff_factor ** attempt} seconds...')
        time.sleep(backoff_factor ** attempt + random.uniform(0, 1))  # Exponential backoff
        
    print("Max retries reached. Exiting...")
    return None  # Return None if retries are exhausted

# Open a CSV file in write mode
with open(r'data/bpl_dataset.csv', 'w', newline='') as file:
    # Writing the header if it's an empty CSV
    header_written = False
    
    # Starting pagination
    start = 0
    
    while True:
        params['offset'] = start
        
        # Fetch data with retry logic
        data = fetch_data_with_retry(url, params)
        logging.info('Data fetched successfully.')
        
        if data:
            records = data['result']['records']
            
            if not records:
                break  # Exit loop if no more records
            
            # Convert records to DataFrame
            df = pd.DataFrame(records)
            
            # Write data incrementally to the file
            if not header_written:
                df.to_csv(file, header=True, index=False)
                logging.info('Header written to CSV.')
                header_written = True
            else:
                df.to_csv(file, header=False, index=False)
            
            # Update pagination start point for next batch
            start += 1000

            # Check if we've fetched all records
            if len(records) < 1000:
                break
        else:
            print('Failed to fetch data. Skipping batch.')
            break  # Exit if the retries are exhausted

        # Add a delay between requests to avoid overwhelming the API
        time.sleep(1)  # Delay of 1 second (can be adjusted based on rate limits)
