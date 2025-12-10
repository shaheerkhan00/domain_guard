# 🛡️ DomainGuard: The Phishing & Typosquatting Detector

![Project Status](https://img.shields.io/badge/Status-Complete-green?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/Stack-Llama3.2_|_Unsloth_|_FastAPI_|_Docker-blue?style=for-the-badge)
![Deployment](https://img.shields.io/badge/Deployment-Containerized-orange?style=for-the-badge)

**DomainGuard** is a specialized cybersecurity AI agent designed to detect malicious domains (phishing, typosquatting, and brand mimicry).

Unlike generic LLMs which often hallucinate or refuse to answer security queries, DomainGuard was **fine-tuned** on a hybrid dataset of real-world threats (OpenPhish) and legitimate domains (Majestic Million). It acts as a strict security analyst, providing a clear `SAFE` or `SUSPICIOUS` verdict with reasoning.

---

## 🚀 Key Features
- **Vertical Slice Architecture:** Built from scratch—from data engineering to Docker deployment.
- **Hybrid Data Strategy:** Trained on a mix of 1,200+ real malicious URLs and synthetically generated typosquatting examples.
- **Fine-Tuned Intelligence:** Specialized Llama 3.2 model that detects patterns like `amazon-secure-login.xyz` vs `amazon.com`.
- **Edge-Optimized:** Quantized to 4-bit GGUF format (1.5GB size) to run efficiently on standard CPUs.
- **Production Ready:** Served via a Dockerized FastAPI endpoint with environment-injected networking.

---

## 🏗️ Architecture

graph LR
    User[Client / Dashboard] -->|POST /analyze| API[FastAPI Container]
    API -->|Prompt| LLM[Ollama (Host Machine)]
    LLM -->|Verdict| API
    API -->|JSON Response| User


## 🛠️ Tech Stack

| Component    | Technology        | Description                                                   |
|--------------|-------------------|---------------------------------------------------------------|
| **Model**    | Llama 3.2 (3B)    | Lightweight base model optimized for instruction following    |
| **Training** | Unsloth (QLoRA)   | Fine-tuned on T4 GPU (Google Colab) for specific security tasks|
| **Inference**| Ollama            | Local LLM runtime used to serve the quantized GGUF model       |
| **Backend**  | FastAPI           | Python API handling requests, parsing, and error management    |
| **Deployment**| Docker           | Containerized application with host-networking injection       |

## 💻 How to Run

### Prerequisites
- Docker Desktop (running)
- Ollama (installed on host)

