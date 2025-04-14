from pydantic import BaseModel

class FinancialData(BaseModel):
    year: int
    company: str
    revenue: float
