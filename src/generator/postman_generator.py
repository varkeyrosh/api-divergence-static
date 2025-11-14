# src/generator/postman_generator.py
import json
import os
from datetime import datetime
from uuid import uuid4

def _pm_meta():
    return {
        "name": "API Divergence Test Collection",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    }

def testcase_to_pm_item(testcase, base_url="http://127.0.0.1:8000"):
    endpoint = testcase.get("endpoint")
    method = testcase.get("method", "GET").upper()
    name = f"{method} {endpoint}"
    url = {
        "raw": f"{base_url}{endpoint}",
        "host": [base_url.replace("http://", "").replace("https://", "")],
        "path": endpoint.strip("/").split("/") if endpoint.strip("/") else []
    }

    # Basic body: for POST/PUT use placeholder JSON (empty), can be enriched later
    body = None
    if method in ("POST", "PUT", "PATCH"):
        body = {
            "mode": "raw",
            "raw": json.dumps(testcase.get("body", {})),
            "options": { "raw": { "language": "json" } }
        }

    # Add a test script in Postman to assert expected status code
    expected_status = 404 if any("404" in s for s in testcase.get("steps", [])) else None
    tests_script = ""
    if expected_status:
        tests_script = f"pm.test('Status is {expected_status}', function() {{ pm.response.to.have.status({expected_status}); }});"
    else:
        # default: assert not 404
        tests_script = "pm.test('Status is not 404', function() { pm.expect(pm.response.code).to.not.eql(404); });"

    item = {
        "name": name,
        "request": {
            "method": method,
            "header": [
                {"key": "Content-Type", "value": "application/json"}
            ],
            "body": body,
            "url": {
                "raw": f"{base_url}{endpoint}",
                "host": [base_url.replace("http://", "").replace("https://", "")],
                "path": endpoint.strip("/").split("/") if endpoint.strip("/") else []
            }
        },
        "response": [],
        "event": [
            {
                "listen": "test",
                "script": {
                    "exec": [tests_script],
                    "type": "text/javascript"
                }
            }
        ]
    }
    return item

def generate_collection_from_testcases(testcases_path, out_dir="reports/postman", base_url="http://127.0.0.1:8000"):
    os.makedirs(out_dir, exist_ok=True)
    with open(testcases_path, "r") as f:
        testcases = json.load(f)

    collection = {
        "info": {
            "name": f"API Divergence Collection {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "_postman_id": str(uuid4()),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }

    for t in testcases:
        collection["item"].append(testcase_to_pm_item(t, base_url=base_url))

    out_path = os.path.join(out_dir, f"collection_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json")
    with open(out_path, "w") as f:
        json.dump(collection, f, indent=2)
    print(f"✅ Postman collection generated at: {out_path}")
    return out_path


