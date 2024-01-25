import os
import tabula
import pandas as pd
from database.connection import SessionLocal, engine
from database import models
import logging
import json
from web_scraping import scrape_and_get_data

models.Base.metadata.create_all(bind=engine)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

#data cleaning
def clean_table(table_data):
    # Fill NaN values in numeric columns with mean if nan ratio is less than 80%
    numeric_columns = table_data.select_dtypes(include='number').columns
    for column in numeric_columns:
        nan_ratio = table_data[column].isna().sum() / len(table_data)
        if nan_ratio < 0.8:
            table_data[column] = table_data[column].fillna(table_data[column].mean())

        else:
            # Drop the entire column if NaN ratio is 80% or more
            table_data = table_data.drop(column, axis=1)

    # Reset the index after cleaning
    cleaned_data = table_data.reset_index(drop=True)

    return cleaned_data

#data storing
def store_combined_data(data):
    db = SessionLocal()

    try:
        combined_data_list = []  # List to accumulate all rows from all tables

        for i, combined_data in enumerate(data):
            # Convert each combined data to a DataFrame
            combined_df = pd.DataFrame(combined_data)

            # Convert the DataFrame to a list of dictionaries (rows)
            combined_data_list.extend(combined_df.to_dict(orient='records'))

            # instance of  model for the combined data
            db_data = models.DataSet(
                extracted_data=json.dumps(combined_data_list)  # Convert the combined data to JSON and store it
            )

            db.add(db_data)
            db.commit()

            # message in the terminal
            logger.debug(f"\nExtracted structued Pdf and scraped Data has been stored in the Database with ID: {db_data.id}")


    except Exception as e:
        logger.error(f"Error while storing data in the database: {e}")
        db.rollback()
    finally:
        db.close()

#cancatination of both structured pdf extracted data and web scraped data
def concatenate_dataframes(table_data_list, df2_list):
    # Concatenate 
    combined_data = pd.concat([pd.DataFrame(table_data_list), pd.DataFrame(df2_list)], axis=1)

    return combined_data

#function to extract and store data
def extract_and_store(pdf_file_path):
    try:
        # Use tabula to extract tables from the PDF
        # extract_tables = tabula.read_pdf(pdf_file_path, pages='all', multiple_tables=True)
        extract_tables = tabula.read_pdf(pdf_file_path, pages='all', multiple_tables=True, java_options=["-Djava.awt.headless=true"])
        all_tables_data = []  # List to accumulate all tables

        # Calling scrape_and_save_data function to get the scraped data in DataFrame
        scraped_data = scrape_and_get_data()

        # Clean the DataFrame obtained from scrape_and_save_data fuction from webscraping script
        scraped_data_df = clean_table(scraped_data)

        df2_list = scraped_data_df.to_dict(orient='records')


        if extract_tables:

            all_tables_data = []  # List to accumulate data for each table separately
            combined_df2_list = []  # List to accumulate df2_list once

            for i, table_data in enumerate(extract_tables):
                cleaned_data = clean_table(table_data)
                dataframe = pd.DataFrame(cleaned_data)
                table_data_list = dataframe.to_dict(orient='records')

                all_tables_data.extend(table_data_list)
                

                # Accumulate df2_list only once
                if i == 0:
                    combined_df2_list.extend(df2_list)

            # getting df2_list dataframe only once
            combined_df2 = pd.DataFrame(combined_df2_list)

            # Concatenate all tables together
            combined_data = concatenate_dataframes(all_tables_data, combined_df2)

            # Store the accumulated data as a single record
            store_combined_data([combined_data])  
        else:
            logger.debug("No tables found in the PDF.")

    except Exception as e:
        logger.error(f"Error during extraction and storage: {e}")
        raise  # Re-raise the exception for proper handling in the main script



# PDF files folder path
pdf_folder = "pdf_files"

# iterate for PDF files in the folder
pdf_files = [file for file in os.listdir(pdf_folder) if file.lower().endswith('.pdf')]

# Check if the folder is empty or contains only non-PDF files
if not pdf_files:
    logger.warning(f"No PDF files found in the folder: {pdf_folder}")
else:
    for pdf_file in pdf_files:
        pdf_file_path = os.path.join(pdf_folder, pdf_file)
        extract_and_store(pdf_file_path)
