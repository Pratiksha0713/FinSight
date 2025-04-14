import pandas as pd

def process_and_save(input_path: str, output_path: str):
    df = pd.read_csv(input_path)

    # ✅ Clean/structure logic here:
    df.columns = df.columns.str.strip()  # Trim column names
    df = df.dropna(how='all')            # Remove completely empty rows
    df = df.fillna(0)                    # Replace NaNs with 0
    numeric_cols = df.select_dtypes(include='number').columns
    df[numeric_cols] = df[numeric_cols].round(2)  # Round numeric fields

    # ✅ Write to JSON
    df.to_json(output_path, orient="records", indent=2)
    return df



import pandas as pd

def load_cashflow_data(file_path: str):
    df = pd.read_csv(file_path)
    # ✅ Clean/structure logic here:
    df.columns = df.columns.str.strip()  # Trim column names
    df = df.dropna(how='all')            # Remove completely empty rows
    df = df.fillna(0)                    # Replace NaNs with 0
    numeric_cols = df.select_dtypes(include='number').columns
    df[numeric_cols] = df[numeric_cols].round(2)  # Round numeric fields

    # Select only necessary columns
    df_cashflow = df[[
        'Year', 'Company', 
        'Cash Flow from Operating', 
        'Cash Flow from Investing', 
        'Cash Flow from Financial Activities'
    ]]

    # Prepare chart-friendly structure
    result = {}

    for _, row in df_cashflow.iterrows():
        company = row['Company']
        year = str(row['Year'])

        if company not in result:
            result[company] = {}

        result[company][year] = {
            "Operating": row['Cash Flow from Operating'],
            "Investing": row['Cash Flow from Investing'],
            "Financing": row['Cash Flow from Financial Activities']
        }

    return result

    try:
        # Load CSV
        df = pd.read_csv(input_path)

        # Clean column names
        df.columns = df.columns.str.strip()

        # Remove fully empty rows
        df = df.dropna(how='all')

        # Replace NaNs with 0
        df = df.fillna(0)

        # Ensure Year is numeric and sorted
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        df = df.dropna(subset=["Year"])
        df["Year"] = df["Year"].astype(int)
        df = df.sort_values(by="Year")

        # Round all numeric values
        numeric_cols = df.select_dtypes(include="number").columns
        df[numeric_cols] = df[numeric_cols].round(2)

        # Save to JSON
        df.to_json(output_path, orient="records", indent=2)

        return df
    except Exception as e:
        print("🔥 Data processing error:", e)
        raise
