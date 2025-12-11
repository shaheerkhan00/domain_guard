# 🛡️ DomainGuard: The Phishing & Typosquatting Detector

![Project Status](https://img.shields.io/badge/Status-Complete-green?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/Stack-Llama3.2_|_Unsloth_|_FastAPI_|_Docker-blue?style=for-the-badge)
![Deployment](https://img.shields.io/badge/Deployment-Containerized-orange?style=for-the-badge)

**DomainGuard** is a specialized cybersecurity AI agent designed to detect malicious domains (phishing, typosquatting, and brand mimicry). Unlike generic LLMs which often hallucinate or refuse to answer security queries, DomainGuard was **fine-tuned** on a hybrid dataset of real-world threats (OpenPhish) and legitimate domains (Majestic Million). It acts as a strict security analyst, providing a clear `SAFE` or `SUSPICIOUS` verdict with reasoning.

---

## 🚀 Key Features

- **Vertical Slice Architecture:** Built from scratch—from data engineering to Docker deployment
- **Hybrid Data Strategy:** Trained on a mix of 1,200+ real malicious URLs and synthetically generated typosquatting examples
- **Fine-Tuned Intelligence:** Specialized Llama 3.2 model that detects patterns like `amazon-secure-login.xyz` vs `amazon.com`
- **Edge-Optimized:** Quantized to 4-bit GGUF format (1.5GB size) to run efficiently on standard CPUs
- **Production Ready:** Served via a Dockerized FastAPI endpoint with environment-injected networking

---

## 🏗️ Architecture

```mermaid
graph LR
    User[Client / Dashboard] -->|POST /analyze| API[FastAPI Container]
    API -->|Prompt| LLM[Ollama (Host Machine)]
    LLM -->|Verdict| API
    API -->|JSON Response| User
```

---

## 🛠️ Tech Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| **Model** | Llama 3.2 (3B) | Lightweight base model optimized for instruction following |
| **Training** | Unsloth (QLoRA) | Fine-tuned on T4 GPU (Google Colab) for specific security tasks |
| **Inference** | Ollama | Local LLM runtime used to serve the quantized GGUF model |
| **Backend** | FastAPI | Python API handling requests, parsing, and error management |
| **Deployment** | Docker | Containerized application with host-networking injection |

---

## 💻 How to Run

### Prerequisites

- **Docker Desktop** (Running)
- **Ollama** (Installed on Host) - [Download here](https://ollama.com/download)

### 1. Setup the AI Model

Pull the fine-tuned model and create the local instance:

```bash
# 1. Download the quantized model from Hugging Face
wget https://huggingface.co/Muhammad-Shaheer/FinetunedLAMAtoDomainGuard-002-3B/resolve/main/llama-3.2-3b-instruct.Q4_K_M.gguf -O domainguard.gguf

# 2. Create the Modelfile (Defines the AI's personality)
# Ensure Modelfile exists in current directory before running:
ollama create domainguard -f Modelfile
```

**Modelfile Example:**
```
FROM ./domainguard.gguf

SYSTEM """You are a cybersecurity expert analyzing domains for phishing and typosquatting threats. 
Respond with either SAFE or SUSPICIOUS followed by your reasoning."""
```

### 2. Configure Network (Windows Only)

By default, Ollama blocks external connections (including Docker). Allow Docker to access it:

```powershell
# Run in PowerShell as Administrator
setx OLLAMA_HOST "0.0.0.0"

# Restart the Ollama app after running this!
```

**For Linux/Mac:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export OLLAMA_HOST=0.0.0.0

# Restart terminal or run:
source ~/.bashrc
```

### 3. Build & Run Docker

We inject the host networking URL (`host.docker.internal`) so the container can talk to the local AI.

```bash
# Build the image
docker build -t domainguard-api .

# Run container (injecting the host URL)
docker run -p 8000:8000 -e OLLAMA_URL="http://host.docker.internal:11434" domainguard-api
```

**For Linux, use:**
```bash
docker run -p 8000:8000 -e OLLAMA_URL="http://172.17.0.1:11434" domainguard-api
```

---

## ⚡ Usage Example

Once the container is running, send a POST request to analyze a domain.

### Request (cURL):
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"domain": "netflix-verify-account.xyz"}'
```

### Request (PowerShell):
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/analyze" `
  -Body '{"domain": "netflix-verify-account.xyz"}' `
  -ContentType "application/json"
```

### Request (Python):
```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    json={"domain": "netflix-verify-account.xyz"}
)

print(response.json())
```

### Response:
```json
{
  "domain": "netflix-verify-account.xyz",
  "verdict": "SUSPICIOUS",
  "raw_analysis": "Verdict: SUSPICIOUS\nReasoning: Mimics brand 'netflix' with urgent keyword 'verify-account' on suspicious TLD (.xyz)."
}
```

---

## 🧠 Training Methodology

1. **Data Ingestion:** Scraped live threat feeds from OpenPhish and top domains from Majestic Million
2. **Data Augmentation:** Generated synthetic typosquatting examples (e.g., `g00gle.com`) to balance the dataset
3. **Fine-Tuning:** Used Unsloth for faster QLoRA fine-tuning on a Tesla T4 GPU
4. **Quantization:** Converted the 16-bit model to 4-bit GGUF to reduce VRAM usage from 6GB → 1.5GB

### Dataset Composition

- **Malicious Domains:** 1,200+ URLs from OpenPhish (phishing sites)
- **Legitimate Domains:** Top 1,000 domains from Majestic Million
- **Synthetic Examples:** 500+ generated typosquatting variants

---

## 📂 Project Structure

```
DomainGuard/
├── main.py              # Docker-aware FastAPI Application
├── Dockerfile           # Production container configuration
├── Modelfile            # Ollama configuration & System Prompt
├── requirements.txt     # Python dependencies
├── domainguard.gguf     # Quantized model file (download separately)
└── README.md            # Documentation
```

---

## 🔧 API Endpoints

### `POST /analyze`

Analyzes a domain for potential security threats.

**Request Body:**
```json
{
  "domain": "string"
}
```

**Response:**
```json
{
  "domain": "string",
  "verdict": "SAFE | SUSPICIOUS",
  "raw_analysis": "string"
}
```

### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

---

## 🐛 Troubleshooting

### Issue: "Connection refused to Ollama"
**Solution:** Ensure Ollama is running and `OLLAMA_HOST` is set to `0.0.0.0`

### Issue: "Model not found"
**Solution:** Run `ollama list` to verify the model was created successfully

### Issue: Docker can't reach host
**Solution:** 
- Windows/Mac: Use `host.docker.internal`
- Linux: Use `172.17.0.1` or `--network=host`

### Issue: Out of memory
**Solution:** The 4-bit quantized model requires ~2GB RAM. Close other applications or use a machine with more memory.

---

## 🚀 Future Enhancements

- [ ] Real-time threat feed integration
- [ ] Web dashboard for batch analysis
- [ ] Support for additional TLD risk scoring
- [ ] Multi-language phishing detection
- [ ] API rate limiting and authentication

---

## 📜 License

MIT License. OpenPhish data used for educational/research purposes.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ for a safer internet**