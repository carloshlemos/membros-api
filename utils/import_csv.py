import csv
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.mongo import get_mongodb

def import_csv_to_mongodb():
    """
    Imports data from a CSV file to a MongoDB collection.
    """
    # Load environment variables from variables.env
    env_path = os.path.join(os.path.dirname(__file__), '..', 'variables.env')
    load_dotenv(dotenv_path=env_path)

    # Get the MongoDB database
    try:
        db = get_mongodb()
        print("Successfully connected to MongoDB.")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return

    # Collection name
    collection_name = 'membros'
    collection = db[collection_name]

    # Path to the CSV file
    csv_file_path = os.path.join(os.path.dirname(__file__), 'membros.csv')

    try:
        # Read the CSV file and insert data into the collection
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            records_to_insert = [row for row in csv_reader]

            if records_to_insert:
                collection.insert_many(records_to_insert)
                print(f"Successfully imported {len(records_to_insert)} records into the '{collection_name}' collection.")
            else:
                print("No records found in the CSV file to import.")

    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    import_csv_to_mongodb()
