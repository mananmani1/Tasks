# Data Extraction and Web Scraping Application

## Requirements

Before running the application, ensure that your system meets the following requirements:

1. Installed Python
2. Python interpreters (VS Code/Pycharm)
3. MySQL (preferably open-source cross-platform web server like XAMPP, etc.)
4. Installed Java setup (required for tabula)

## Environment Setup

1. Create a virtual environment using one of the following methods:
   - Virtualenv: `virtualenv name_of_env`
   - Python venv: `python -m venv name_of_env`

2. Activate the virtual environment in the command prompt of your current directory where the environment is created:
   - For Windows: `name_of_env\Scripts\Activate`

   You have now successfully activated your virtual environment.

## Installation of Required Libraries

Run the following command in the command prompt with the activated virtual environment to install all required libraries specified in the `requirements.txt` file:


pip install -r requirements.txt

This command will install all the necessary libraries for the application.

## Running the Application

Once the environment and libraries are set up, follow the steps below to run the application:

Run the following command in the command prompt:
uvicorn main:app --reload
This command will start the application and display a message along with a link:

INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
DEBUG: data_extraction: Extracted structured PDF and scraped Data has been stored in the Database with ID: 2 

1.  Click on the provided link in in terminal it will lead to your browser. This will open an HTML page with a download button and a text box for entering an ID.

2.  Enter the desired ID and click the download button. An Excel file containing both the extracted structured PDF data and scraped data from
   the website will be downloaded to your system.


## Fastapi and logging role

The entire application runs with a single command using FastAPI endpoints. 
The application fetches data from the database, runs scripts, and provides a user interface through an HTML page for interaction.  
## Additional Information
The application includes scripts for performing different tas holing all by FastAPI and there are database integration, exception handling, validations, logging, 
PDF structured data extraction using Tabula,and web scraping using BeautifulSoup. for all flow I passed comments so that one can undersatand easily.

For any questions or issues, please contact:
Abdul Manan
ML Engineer
Email: mananmani5577@gmail.com
