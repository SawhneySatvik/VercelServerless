import os
import json
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS to allow GET requests from any origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# Determine the absolute path to the JSON file.
# current_dir = os.path.dirname(__file__)
# json_file_path = os.path.join(current_dir, "..", "q-vercel-python.json")

# Load the JSON data.
with open(json_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert the list of objects to a dictionary.
marks_data = {entry["name"]: entry["marks"] for entry in data if "name" in entry and "marks" in entry}

@app.get("/api")
def get_marks(name: list[str] = Query(None)):
    """
    Expects one or more 'name' query parameters, e.g.:
    /api?name=Alice&name=Bob
    Returns the marks for the provided names in order.
    """
    if name is None:
        return {"marks": []}
    
    result_marks = [marks_data.get(n, None) for n in name]
    return {"marks": result_marks}


