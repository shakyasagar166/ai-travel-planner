# ✈️ ShopAgent AI — Autonomous Travel Planner Agent

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent%20Mesh-blue?style=for-the-badge&logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq%20Cloud-Llama%203.3%2070B-F55036?style=for-the-badge&logo=fastly&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20RAG-orange?style=for-the-badge)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![React](https://img.shields.io/badge/React-18%20%2B%20Vite%20%2B%20Tailwind-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<p align="center">
  <b>An autonomous, multi-agent AI travel concierge engineered with LangGraph, Groq Llama 3.3, ChromaDB vector RAG, MySQL catalog, FastAPI REST gateway, and a modern React.js frontend.</b>
</p>

[Key Features](#-key-features) • [System Architecture](#-system-architecture) • [Multi-Agent Mesh](#-multi-agent-mesh-langgraph) • [Project Structure](#-project-directory-structure) • [Quickstart Guide](#-quickstart-guide) • [API Reference](#-api-reference) • [Automated Tests](#-automated-test-suite)

---

</div>

## 📖 Overview

Standard travel chatbots merely generate generic, text-heavy bullet lists that disregard hard budget constraints, hallucinate attraction pricing, and fail to optimize daily geographic pacing.

**ShopAgent AI (Travel Edition)** is built upon **Agentic AI principles** using **LangGraph**. It coordinates a specialized team of autonomous agents that work together to:
* Parse natural language vacation wishes into structured requirement specifications (destination, days, budget bounds, party size, travel style, and dietary needs).
* Filter and rank attractions and accommodations from a structured database.
* Calculate trip costs deterministically in Python (stay, dining, activities, and local transit) to strictly enforce budget guardrails.
* Retrieve localized cultural advice, weather warnings, and scams to avoid using **ChromaDB dense vector RAG**.
* Deliver an interactive day-by-day itinerary timeline with morning, afternoon, and evening schedules.

---

## 🌟 Key Features

* **🧠 Multi-Agent Orchestration**: 9 decoupled agents collaborating via a compiled LangGraph `StateGraph(TravelState)` workflow.
* **🛠️ Native Tool Calling**: LangChain `@tool` functions for catalog search, interest ranking, hotel filtering, deterministic budget calculation, and RAG retrieval.
* **🛡️ Zero-Hallucination Guardrails**: Cost breakdowns and pacing constraints are calculated mathematically in Python, preventing invented expenses.
* **🔍 Dense Vector RAG**: Indexed travel guides, local etiquette, packing checklists, and safety advisories in **ChromaDB** using `sentence-transformers/all-MiniLM-L6-v2`.
* **⚡ High-Speed Inference**: Powered by **Groq Cloud Llama 3.3 70B Versatile** for near instantaneous reasoning and plan generation.
* **🔐 Secure Authentication**: Industry-standard Bcrypt password hashing (12 rounds) and cryptographically signed JWT access tokens.
* **🎨 Modern Travel Dashboard**: Built with React 18, Vite, Tailwind CSS, and Lucide icons. Features live multi-agent execution step indicator, interactive day-by-day timeline tabs, visual budget breakdown bars, and destination explorer catalog.
* **🧪 Comprehensive Test Suite**: 6 standalone automated test scripts verifying database models, authentication, tools, RAG retriever, multi-agent graph, and FastAPI REST endpoints.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    User([👤 Traveler / Browser]) <--> ReactApp[⚛️ React 18 + Tailwind UI\nLive Agent Steps | Day Timeline | Budget Bars | Catalog]
    ReactApp <-->|REST API + JWT Bearer| FastAPI[⚡ FastAPI Backend Gateway]

    subgraph LangGraph_Mesh [LangGraph Multi-Agent Orchestrator]
        FastAPI --> Supervisor[🎯 Supervisor / Planner Agent]
        Supervisor -->|Step 1: Extract Specs| ReqAgent[📝 Requirement Understanding Agent]
        Supervisor -->|Step 2: Match Destination| DestAgent[🌍 Destination Selection Agent]
        Supervisor -->|Step 3: Rank Spots| AttrAgent[🏛️ Attraction Curation Agent]
        Supervisor -->|Step 4: Pick Stay| StayAgent[🏨 Accommodation Agent]
        Supervisor -->|Step 5: Schedule Slots| SchedAgent[📅 Itinerary Scheduler Agent]
        Supervisor -->|Step 6: Math Verification| BudgetAgent[💰 Budget Estimator Agent]
        Supervisor -->|Step 7: Vector Knowledge| RAGAgent[📚 Travel Knowledge RAG Agent]
        Supervisor -->|Step 8: Synthesize Plan| FinalAgent[💬 Final Response Agent]
    end

    subgraph Data_Layer [Data & Persistence Tier]
        DestAgent & AttrAgent & StayAgent <-->|SQLAlchemy ORM| MySQL[(🐬 MySQL 8.0 Catalog)]
        RAGAgent <-->|SentenceTransformers| ChromaDB[(🔮 ChromaDB Vector Store)]
    end

    subgraph LLM_Cloud [High-Performance Inference]
        ReqAgent & FinalAgent <-->|Ultra-Low Latency| Groq[🚀 Groq Cloud: Llama 3.3 70B]
    end
```

---

## 🤖 Multi-Agent Mesh (LangGraph)

| Agent | Responsibility | Core Logic & Tools Used |
| :--- | :--- | :--- |
| **1. Requirement Understanding Agent** | Analyzes natural language input to extract destination, days, budget, travelers count, travel style, interests, and pacing. | Groq Llama 3.3 with structured JSON extraction and deterministic regex fallback. |
| **2. Supervisor / Planner Agent** | Validates state and routes execution flow sequentially through the planning pipeline. | LangGraph state transitions and workflow management. |
| **3. Destination Selection Agent** | Resolves destination from catalog or suggests best match based on climate and traveler tags. | Tool: `search_destinations(query, continent)` via MySQL. |
| **4. Attraction Curation Agent** | Ranks and selects attractions matching traveler's interests and available trip duration. | Tool: `search_attractions()`, `filter_attractions_by_interests()`. |
| **5. Accommodation Agent** | Selects optimal hotel, hostel, or resort matching budget and comfort tier. | Tool: `search_accommodations(destination, tier)`. |
| **6. Itinerary Scheduler Agent** | Organizes curated attractions into Morning, Afternoon, and Evening slots with realistic timing and tips. | Day-by-day timeline builder. |
| **7. Budget Estimator Agent** | Deterministically calculates stay, food, activities, and transit expenses against user budget bounds. | Tool: `calculate_trip_budget()`. Eliminates hallucinated pricing. |
| **8. Travel Knowledge RAG Agent** | Retrieves dense semantic chunks regarding weather warnings, local tips, and scams to avoid. | Tool: `search_travel_knowledge(query, destination)` via ChromaDB. |
| **9. Final Response Agent** | Compiles engaging markdown narrative along with typed JSON itinerary payload for frontend components. | Combines LLM narrative synthesis with typed UI payload. |

---

## 📁 Project Directory Structure

```
ai-travel-planner-agent/
│
├── 📁 backend/                 # FastAPI server, LangGraph multi-agent mesh, tools & models
│   ├── app/
│   │   ├── agents/             # The 9 autonomous LangGraph agents & state definition
│   │   ├── api/                # REST API routers (auth, chat, destinations, trips, users)
│   │   ├── core/               # Security, Bcrypt password hashing, JWT dependencies
│   │   ├── database/           # SQLAlchemy models, Pydantic schemas, catalog seed data
│   │   ├── graph/              # LangGraph StateGraph assembly and workflow compilation
│   │   ├── rag/                # ChromaDB vector store, MiniLM embeddings, semantic retriever
│   │   ├── services/           # Authentication and business logic services
│   │   ├── tools/              # LangChain @tool definitions for search, filter, RAG, budget
│   │   ├── config.py           # Centralized Pydantic BaseSettings environment loader
│   │   └── main.py             # FastAPI entrypoint with CORS, lifespan startup hooks
│   ├── tests / scripts:
│   │   ├── test_db.py          # Database ORM and schema verification test
│   │   ├── test_auth.py        # Bcrypt & JWT token verification test
│   │   ├── test_rag.py         # ChromaDB ingestion & semantic search test
│   │   ├── test_tools.py       # LangChain tool execution test
│   │   ├── test_graph.py       # LangGraph multi-agent full pipeline test
│   │   └── test_api.py         # FastAPI REST endpoints integration test
│   ├── Dockerfile              # Backend containerization spec
│   ├── requirements.txt        # Pinned Python package dependencies
│   └── .env.example            # Backend environment variable template
│
├── 📁 frontend/                # Modern React 18 + Vite + Tailwind CSS Single Page App
│   ├── src/
│   │   ├── api/                # Axios API client & typed REST endpoint helpers
│   │   ├── components/         # Navbar, ChatMessage, ItineraryTimeline, BudgetBreakdownCard, DestinationCard, AuthModal, PreferencesModal
│   │   ├── context/            # AuthContext for persistent JWT session state
│   │   ├── pages/              # DashboardPage with live agent pipeline tracker and itinerary workspace
│   │   ├── App.jsx             # Main application component & modal coordinators
│   │   └── main.jsx            # React DOM root entrypoint
│   ├── Dockerfile              # Frontend multi-stage Nginx build spec
│   ├── package.json            # Node.js dependencies (Tailwind, Lucide, Axios, Vite)
│   └── tailwind.config.js      # Custom theme styling & colors
│
├── 📁 data/                    # Raw catalog dataset and database schemas
│   ├── destinations.json       # Seed data for 8 global destinations, attractions & stays
│   ├── schema.sql              # MySQL DDL schema definition
│   └── README.md
│
├── 📁 vectorstore/             # ChromaDB persistent vector collection storage
│   ├── .gitkeep
│   └── README.md
│
├── 🐳 docker-compose.yml       # Multi-service container orchestration (Backend, Frontend, MySQL)
├── 📄 .gitignore               # Comprehensive Git secret & build artifact ignore rules
├── 📄 .env.example             # Project-wide environment template
├── 📄 README.md                # Project documentation
└── 📄 LICENSE                  # MIT License
```

---

## 🚀 Quickstart Guide

### Prerequisites
* **Python**: 3.11, 3.12, or 3.13
* **Node.js**: 18+ and npm
* **MySQL Server**: 8.0+ running locally (or via Docker)
* **Groq API Key**: Free tier available at [console.groq.com](https://console.groq.com/keys)

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/shakyasagar166/ShopAgent-AI.git
cd ShopAgent-AI
```

---

### Step 2: Configure Environment Variables

Copy `.env.example` to `backend/.env`:

```bash
cp .env.example backend/.env
```

Edit `backend/.env` with your settings:

```env
# Security & JWT
SECRET_KEY=generate_a_random_32_byte_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=travel_ai

# Groq LLM Provider
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Chroma Vector Store
CHROMA_PERSIST_DIRECTORY=./vectorstore

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

> [!NOTE]
> If MySQL is not running on your machine, the backend will automatically fall back to an embedded SQLite database (`travel_local.db`) so you can develop and test immediately without friction!

---

### Step 3: Run the Backend (FastAPI)

```bash
cd backend

# Create and activate Python virtual environment
python -m venv .venv

# Windows:
.\.venv\Scripts\activate
# Linux / macOS:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI development server
uvicorn app.main:app --reload --port 8000
```

* 🚀 **Interactive Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
* 🩺 **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

### Step 4: Run the Frontend (React.js + Vite)

Open a new terminal window:

```bash
cd frontend

# Install npm dependencies
npm install

# Start Vite dev server
npm run dev
```

* 🌐 **Frontend Application**: [http://localhost:5173](http://localhost:5173)

---

## 🐳 Optional: Run with Docker Compose

To spin up the entire stack (FastAPI Backend + React Frontend + MySQL Database) using Docker:

```bash
docker-compose up --build
```

Services will be accessible at:
* Frontend: `http://localhost:3000`
* Backend: `http://localhost:8000`
* MySQL: `localhost:3306`

---

## 🧪 Automated Test Suite

The repository includes 6 standalone automated test suites in `backend/`:

```bash
cd backend
.\.venv\Scripts\activate

# 1. Verify Database ORM Models & Seeding
python test_db.py

# 2. Verify Bcrypt Hashing & JWT Token Generation
python test_auth.py

# 3. Verify ChromaDB Ingestion & Semantic Retrieval
python test_rag.py

# 4. Verify LangChain Tool Calling Layer
python test_tools.py

# 5. Verify LangGraph Multi-Agent StateGraph Workflow
python test_graph.py

# 6. Verify FastAPI REST Endpoints & Chat API
python test_api.py
```

---

## 🔌 API Reference

### Authentication Endpoints
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/v1/auth/register` | Register a new traveler account | No |
| `POST` | `/api/v1/auth/login` | Login and receive a JWT Bearer token | No |
| `GET` | `/api/v1/auth/me` | Fetch authenticated user profile | **Yes** |

### Chat & Agentic Workflow
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/v1/chat` | Send a natural language travel request; triggers LangGraph | Optional |

#### Example Request:
```json
POST /api/v1/chat
Content-Type: application/json

{
  "message": "Plan a 4-day budget trip to Goa for 2 people with Rs. 35,000 budget. We love beaches and nightlife.",
  "conversation_id": null
}
```

#### Example Response:
```json
{
  "conversation_id": "4d78832a-5a81-42db-8d96-c65ee1a3b8e7",
  "response": "### ✈️ Your Custom 4-Day Itinerary for Goa!...",
  "itinerary": {
    "destination": "Goa",
    "days": 4,
    "travelers_count": 2,
    "travel_style": "Nightlife & Leisure",
    "pace": "Moderate",
    "accommodation": {
      "name": "Santana Beach Resort",
      "tier": "Moderate",
      "price_per_night_inr": 4200.0,
      "rating": 4.4
    },
    "cost_breakdown": {
      "stay_cost_inr": 12600.0,
      "food_cost_inr": 11200.0,
      "transit_cost_inr": 5600.0,
      "activities_cost_inr": 4200.0,
      "total_estimated_cost_inr": 33600.0,
      "budget_limit_inr": 35000.0,
      "is_within_budget": true,
      "savings_or_excess_inr": 1400.0
    },
    "days_plan": [
      {
        "day": 1,
        "title": "Day 1: Highlights of Goa",
        "morning": { "time": "09:00 AM - 12:30 PM", "activity": "Visit Baga Beach & Water Sports", "category": "Beach & Adventure", "estimated_cost_inr": 0.0 },
        "afternoon": { "time": "01:30 PM - 04:30 PM", "activity": "Experience Fort Aguada & Lighthouse", "category": "Heritage & Scenic", "estimated_cost_inr": 50.0 },
        "evening": { "time": "05:30 PM - 08:30 PM", "activity": "Sunset & evening at Anjuna Flea Market", "category": "Shopping & Nightlife", "estimated_cost_inr": 0.0 },
        "day_total_cost_inr": 50.0
      }
    ],
    "insider_tips": [
      "Rent a scooter (₹350-₹500/day) for maximum mobility and coastal flexibility.",
      "Try local Goan fish curry thali away from crowded tourist strips."
    ],
    "packing_checklist": [
      "Swimwear & quick-dry towels",
      "Sunglasses & Sunscreen SPF 50+",
      "Light cotton clothes"
    ]
  },
  "agent_steps": [
    { "agent": "requirement_understanding", "status": "completed", "output": "Parsed destination: Goa, Duration: 4 days, Budget: ₹35,000" },
    { "agent": "destination_selection", "status": "completed", "output": "Selected destination: Goa (India)" },
    { "agent": "attraction_curation", "status": "completed", "output": "Curated 5 top-rated attractions" },
    { "agent": "accommodation_matcher", "status": "completed", "output": "Selected stay: Santana Beach Resort" },
    { "agent": "itinerary_scheduler", "status": "completed", "output": "Constructed cohesive 4-day timeline" },
    { "agent": "budget_cost_estimator", "status": "completed", "output": "Estimated total: ₹33,600 (Within Budget)" },
    { "agent": "travel_knowledge_rag", "status": "completed", "output": "Retrieved 3 verified insider guides" }
  ]
}
```

### Destination Endpoints
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/destinations` | Retrieve catalog with optional search & continent filters | No |
| `GET` | `/api/v1/destinations/{id}` | Retrieve comprehensive destination details, attractions, and stays | No |
| `GET` | `/api/v1/destinations/{id}/attractions` | Retrieve attractions for a destination | No |
| `GET` | `/api/v1/destinations/{id}/accommodations` | Retrieve accommodations for a destination | No |

---

## 🔒 Security Best Practices

* **No Hardcoded Secrets**: All configuration is derived dynamically from `.env` via Pydantic `BaseSettings`.
* **Strict .gitignore**: Protects `.env`, local vector stores, and private keys from Git commits.
* **Bcrypt Password Encryption**: Industry-standard adaptive salt hashing protects user credentials.
* **Deterministic Guardrails**: Hardware and financial spec checking are strictly executed via Python logic, eliminating hallucinations.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — see the LICENSE file for details.

---

<div align="center">
  <b>Built with ❤️ using LangGraph, Groq, ChromaDB, FastAPI, and React</b>
</div>
