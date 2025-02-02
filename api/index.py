import json
import urllib.parse

# Load the marks data from marks.json on cold start.
with open("marks.json", "r", encoding="utf-8") as f:
    marks_data = json.load(f)

def handler(request, context):
    # Enable CORS by setting the proper headers.
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    # Handle preflight (OPTIONS) requests.
    if request.method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": ""
        }

    # Parse the query string manually to support multiple "name" parameters.
    # (Example URL: /api?name=Alice&name=Bob)
    qs = {}
    if "?" in request.url:
        query_string = request.url.split("?", 1)[1]
        qs = urllib.parse.parse_qs(query_string)
    names = qs.get("name", [])

    # Retrieve marks for each provided name (preserving the order).
    result_marks = [marks_data.get(name, None) for name in names]

    body = json.dumps({"marks": result_marks})
    return {
        "statusCode": 200,
        "headers": headers,
        "body": body
    }
