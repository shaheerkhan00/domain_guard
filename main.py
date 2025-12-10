from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import os # <--- ADDED THIS

app = FastAPI(title="DomainGuard API")

class DomainRequest(BaseModel):
    domain: str

@app.post("/analyze")
def analyze_domain(request: DomainRequest):
    print(f"🔹 1. Received Request for: {request.domain}")

    # CONFIGURATION:
    # If running in Docker, we will pass "http://host.docker.internal:11434"
    # If running locally, it defaults to "http://127.0.0.1:11434"
    ollama_base = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
    url = f"{ollama_base}/api/generate"
    
    print(f"🔹 2. Connecting to Ollama at: {url}") # Debug print
    
    data = {
        "model": "domainguard",
        "prompt": request.domain,
        "stream": False,
        "temperature": 0.1
    }
    
    try:
        # Increased timeout to 120s for Docker networking latency
        response = requests.post(url, json=data, timeout=120)
        
        print("🔹 3. Response Received!")
        response_json = response.json()
        raw_output = response_json.get("response", "")
        
        verdict = "Unknown"
        if "SUSPICIOUS" in raw_output.upper():
            verdict = "SUSPICIOUS"
        elif "SAFE" in raw_output.upper():
            verdict = "SAFE"
            
        return {
            "domain": request.domain,
            "verdict": verdict,
            "raw_analysis": raw_output
        }

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Connection failed: {str(e)}")