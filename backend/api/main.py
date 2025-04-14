import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from processor import process_and_save, load_cashflow_data
from mangum import Mangum

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(__file__)
DATA_FILE_PATH = os.path.join(BASE_DIR, "data", "Financial_Statements.csv")
PROCESSED_JSON_PATH = os.path.join(BASE_DIR, "data", "Processed_Financials.json")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Financial Data API!"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    with open(DATA_FILE_PATH, "wb") as f:
        f.write(contents)
    return {"filename": file.filename}


@app.get("/process")
def process_data():
    try:
        df = process_and_save(DATA_FILE_PATH, PROCESSED_JSON_PATH)
        return {"status": "success", "records": len(df)}
    except Exception as e:
        return {"error": str(e)}


@app.get("/data")
def get_data():
    try:
        if os.path.exists(PROCESSED_JSON_PATH):
            df = pd.read_json(PROCESSED_JSON_PATH)
            return df.to_dict(orient="records")
        else:
            return {"error": "Processed JSON not found. Run /process first."}
    except Exception as e:
        return {"error": str(e)}


@app.get("/cashflow")
def get_cashflow():
    try:
        data = load_cashflow_data(DATA_FILE_PATH)
        return data
    except Exception as e:
        return {"error": str(e)}


@app.get("/pnl")
def get_pnl_data():
    try:
        if os.path.exists(PROCESSED_JSON_PATH):
            df = pd.read_json(PROCESSED_JSON_PATH)

            # Select relevant columns only for P&L
            pnl_cols = [
                "Year", "Company", "Revenue", "Gross Profit", "Net Income",
                "Earning Per Share", "EBITDA"
            ]

            df = df[pnl_cols]

            # Group by company and return sorted yearly data
            grouped = (
                df.sort_values("Year")
                  .groupby("Company")
                  .apply(lambda x: x.to_dict(orient="index"))
                  .to_dict()
            )

            return grouped
        else:
            return {"error": "Processed data not found. Please run /process first."}
    except Exception as e:
        return {"error": str(e)}


@app.get("/company/{company_name}/data")
def get_company_data(company_name: str):
    try:
        if os.path.exists(PROCESSED_JSON_PATH):
            df = pd.read_json(PROCESSED_JSON_PATH)

            # Filter data based on company name
            company_data = df[df['Company'] == company_name]

            if company_data.empty:
                return {"error": f"No data found for company {company_name}"}

            return company_data.to_dict(orient="records")
        else:
            return {"error": "Processed data not found. Please run /process first."}
    except Exception as e:
        return {"error": str(e)}

# Required for AWS Lambda / Vercel compatibility
handler = Mangum(app)


