from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json

# Create the FastAPI app.
app = FastAPI()

# Enable CORS to allow GET requests from any origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Allow all origins.
    allow_methods=["GET", "OPTIONS"],  # Allow GET and OPTIONS.
    allow_headers=["*"],
)

# Load marks data on cold start.
with open("q-vercel-python.json", "r", encoding="utf-8") as f:
    marks_data = json.load(f)

# Define the route.
# Note: Since this file is in the "api" directory, Vercel will serve this
# function at https://your-app.vercel.app/api. So we use the path "/" here.
@app.get("/")
def get_marks(name: list[str] = Query(None)):
    """
    Expects one or more 'name' query parameters.
    For example: /api?name=Alice&name=Bob
    Returns the marks for the names in the same order.
    """
    if name is None:
        return {"marks": []}
    
    result_marks = [marks_data.get(n, None) for n in name]
    return {"marks": result_marks}
