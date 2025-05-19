
# AI Billing Assistant Project

## Introduction

Welcome to the AI Billing Assistant — an intelligent chat-based solution designed to help users effortlessly manage and inquire about their mobile billing. Powered by advanced language models, this assistant interprets user queries, interacts with backend billing APIs, and provides clear, human-like responses in real-time.

---

## Why This Project?

Modern billing systems can be complex and hard to navigate. By integrating Large Language Models (LLMs) such as OPENAI or Mistral or Ollama, we bring natural language understanding directly to your fingertips. This project demonstrates how AI can streamline customer interactions, combining conversational AI with real-time data access.

---

 ## Project Architecture Overview

- **Frontend:** Built using Expo and React Native Web, providing a seamless chat interface accessible from any device.
- **Backend:** A FastAPI WebSocket server that processes user messages, invokes LLMs to extract intents, queries billing APIs, formats responses, and logs conversations.
- **Data Persistence:** Firebase Firestore stores chat history and synchronizes messages for a consistent user experience.
- **Deployment:** Backend is containerized via Docker and deployed on Azure App Service; frontend is hosted on Expo’s web platform with EAS deploy.

---
## Example Scenario to Run in the App

You can test the application using the following natural language commands. Each message includes a clear intent and subscriber number, ensuring the system can understand and process the request using the LLM and API Gateway.

---

### 1. Add Usage (Phone)
> **“Add 5000 minutes of phone usage for July 2027. My Subscriber number is 1.”**

This command adds phone usage for the subscriber.

---

### 2. Bill Summary
> **“What is my bill for July 2027? My Subscriber number is 1.”**

This returns a summary of the bill (total amount and payment status).

---

### 3. Detailed Bill (First Request)
> **“Show my detailed bill for July 2027. My Subscriber number is 1.”**

This fetches usage breakdown (minutes, MBs, amount, payment status).

---

### 4. Make Payment
> **“Pay my bill for July 2027. My Subscriber number is 1.”**

This triggers the payment API for the corresponding month.

---

### 5. Detailed Bill (After Payment)
> **“Show it again for July 2027. My Subscriber number is 1.”**

This reconfirms the updated bill with status changed to "Paid ✅".

---

These messages simulate a full user flow: usage entry → bill inquiry → detailed check → payment → re-verification.



## Setup & Installation

### Prerequisites

- Node.js (v16+)
- Python 3.10+
- Docker (for backend)
- Azure CLI (for deployment)
- Firebase account with Firestore enabled
- Expo CLI for frontend development
- Git and GitHub account

### Backend Setup

1. Clone the repo and create a Python virtual environment:

   ```
   git clone https://github.com/yourusername/your-repo.git
   cd your-project-folder
   python -m venv .venv
   source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
    ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Configure environment variables in a `.env` file:

   ```env
   OPENAI_API_KEY=your-api-key
   FIREBASE_KEY_PATH=path/to/firebase_key.json
   API_USERNAME=your_api_username
   API_PASSWORD=your_api_password
   API_BASE_URL=https://your-billing-api.com/api/v1
   ```

4. Place your Firebase service account JSON as specified and update your config accordingly.

---

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd MobileBillingApp
   ```

2. Install Node.js dependencies:

   ```bash
   npm install
   ```

3. Update Firebase config with your project’s details (make sure to exclude sensitive files from Git).

4. Modify WebSocket URL in `ChatScreen.tsx` to point to your deployed backend:

   ```ts
   const socket = new WebSocket("wss://your-backend-url/ws");
   ```

---

## Running the Project Locally

* **Backend:**

  ```bash
  source .venv/bin/activate  # Activate venv
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```

* **Frontend:**

  ```bash
  cd MobileBillingApp
  npm run web  # or expo start --web
  ```

Open the Expo web URL and test your chat interface with the backend.

---

## Challenges & Tips

* **LLM Output Validation:** Ensuring the AI returns strict JSON was tricky; prompt engineering was key to reliable parsing.
* **Environment Configuration:** Managing secrets securely across local, Docker, and cloud deployments required `.env` best practices.
* **WebSocket Reliability:** Handling connection drops gracefully improves user experience.
* **Build & Deploy:** Expo Router’s web build nuances required adapting to newer Expo CLI and EAS workflows.

---

## Deployment

### Backend

* Build and push Docker image to Docker Hub.
* Deploy on Azure App Service using Azure CLI.
* Enable WebSocket support and configure ports.
* Update frontend WebSocket URL accordingly.

### Frontend

* Use Expo’s `eas build` and `eas deploy` commands for seamless web deployment.
* Alternatively, connect your GitHub repo to Vercel for automatic deployments on push.

---

## Conclusion

This project illustrates how modern AI, cloud services, and frontend technologies can harmonize to create intuitive, scalable user-facing applications. Beyond functionality, the journey involved problem-solving around AI prompt design, deployment strategies, and real-time communication.

We hope this repository serves both as a practical tool and a learning resource for integrating conversational AI in real-world scenarios.

---

## Quick Commands Summary

```bash
# Backend setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend setup
cd MobileBillingApp
npm install
npm run web

# Docker build & push
docker build -t yourusername/ai-agent-backend .
docker push yourusername/ai-agent-backend

# Azure deployment (example)
az login
az group create --name my-resource-group --location francecentral

az appservice plan create --name my-appservice-plan --resource-group my-resource-group --is-linux --sku B1

az webapp create --resource-group my-resource-group --plan my-appservice-plan --name my-unique-webapp-name --deployment-container-image-name yourdockerhubusername/ai-agent-backend:latest

az webapp config set --resource-group my-resource-group --name my-unique-webapp-name --web-sockets-enabled true

az webapp config appsettings set --resource-group my-resource-group --name my-unique-webapp-name --settings WEBSITES_PORT=8000


# Expo web deploy
npx expo export --platform web
eas deploy
```

---


