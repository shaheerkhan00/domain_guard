from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import os 
app = FastAPI(title="DomainGuard API")

class DomainRequest(BaseModel):
    domain: str

@app.post("/analyze")
def analyze_domain(request: DomainRequest):
    print(f"Received Request for: {request.domain}")

    
    # If running in Docker, we will pass "http://host.docker.internal:11434"
    # If running locally, it defaults to "http://127.0.0.1:11434"
    ollama_base = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
    url = f"{ollama_base}/api/generate"
    
    print(f"Connecting to Ollama at: {url}") # Debug print
    
    data = {
        "model": "domainguard",
        "prompt": request.domain,
        "stream": False,
        "temperature": 0.1
    }
    
    try:
        # Increased timeout to 120s for Docker networking latency
        response = requests.post(url, json=data, timeout=120)
        
        print("Response Received")
        response_json = response.json()
        raw_output = response_json.get("response", "")
        clean_output = raw_output.upper()
        verdict = "UNKNOWN"
        if "VERDICT: SUSPICIOUS" in clean_output:
            verdict = "SUSPICIOUS"
        elif "VERDICT: SAFE" in clean_output:
            verdict = "SAFE"
            
        # 3. Fallback: If model forgot "Verdict:", looks for keywords but strictly
        else:
            # If it says "Safe" but NOT "Suspicious", it's Safe
            if "SAFE" in clean_output and "SUSPICIOUS" not in clean_output:
                verdict = "SAFE"
            # If it says "Suspicious", it's Suspicious
            elif "SUSPICIOUS" in clean_output:
                verdict = "SUSPICIOUS"
            else:
                verdict = "Unknown"
        return {
            "domain": request.domain,
            "analysis": raw_output
        }

    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Connection failed: {str(e)}")