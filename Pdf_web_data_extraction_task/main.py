from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import SessionLocal, engine
from database import models
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from data_extraction import extract_and_store  # Import the extract_and_store function
import extraction_routes
import json
import pandas as pd
from fastapi import Query


app = FastAPI()
origins = ['*']

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Endpoint to serve the home page with a button to download Excel based on ID
@app.get("/", response_class=HTMLResponse)
async def home():
    return FileResponse("static/home.html")

#endpoint for download excel file
@app.get("/download_excel")
def download_excel(data_id: int = Query(..., title="Data ID"), self: str = Query(..., title="Self"), db: Session = Depends(extraction_routes.ConversationRoutes.get_db)):
    data = db.query(models.DataSet).filter(models.DataSet.id == data_id).first()

    if data:
        extracted_data = json.loads(data.extracted_data)

        # Creating a Pandas DataFrame from the extracted data
        df = pd.DataFrame(extracted_data)

        # Excel file path
        excel_file_path = f"Data_Id_{data_id}.xlsx"

        # Save the DataFrame to an Excel file
        df.to_excel(excel_file_path, index=False)

        # Return the Excel file as a response to download
        return FileResponse(excel_file_path, filename=f"Data_Id_{data_id}.xlsx")
    else:
        raise HTTPException(status_code=404, detail="Data not found")

# Endpoint to run the extraction process
@app.get("/run_extraction")
def run_extraction(db: Session = Depends(extraction_routes.ConversationRoutes.get_db)):
    try:
        # Call the extract_and_store function to perform the extraction, cleaning, and storing into the database
        extract_and_store()

        return {"message": "Extraction process completed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")




#for the use of fastapi ui (swagger) 
@app.get("/get_extracted_data/{data_id}")
def get_extracted_data(data_id: int, db: Session = Depends(extraction_routes.ConversationRoutes.get_db)):
    data = db.query(models.DataSet).filter(models.DataSet.id == data_id).first()

    if data:
        return {"id": data.id, "extracted_data": data.extracted_data}
    else:
        raise HTTPException(status_code=404, detail="Data not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
