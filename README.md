# AI-GameSearch

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangGraph-ReAct-orange?style=for-the-badge)
![Model](https://img.shields.io/badge/Llama_3.3-70B-purple?style=for-the-badge)
![API](https://img.shields.io/badge/Steam_Store-API-black?style=for-the-badge)

**Steam Game Hunter** is an intelligent, autonomous AI agent designed to discover "hidden gem" games and track real-time prices on Steam.

Built on the **LangGraph** architecture using **ReAct (Reasoning + Acting)** logic, this agent doesn't just chat; it actively searches the web for game recommendations, filters them based on user criteria, and queries the Steam Store API for live pricing and discounts.

## 🚀 Key Features

* **🧠 ReAct Architecture:** The agent utilizes a cyclic graph workflow (Think → Act → Observe) to make decisions on which tools to use.
* **🔍 Smart Web Search (Tavily):** Scrapes the web for curated lists like "Best Indie Games 2025" or "Top Rated Metroidvanias" to find game names.
* **💰 Real-Time Price Checking:** Directly interacts with the Steam Store API to fetch current prices, discount percentages, and currency.
* **🛡️ Robust Error Handling:** Implements defensive programming in tool outputs to handle API timeouts and malformed data gracefully.
* **📉 Cost & Token Optimization:** Tools are engineered to return concise string summaries instead of raw JSON, reducing LLM token usage by **~80%**.
* **🇹🇷 Natural Language Support:** Fully optimized to process queries and generate responses in **Turkish**.

## 🛠️ Tech Stack & Architecture

This project leverages a modern AI engineering stack:

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Orchestration** | **LangGraph** | Manages the cyclic state and agent workflow. |
| **LLM** | **Llama 3.3 (via Groq)** | High-performance inference with large context window. |
| **Search Tool** | **Tavily API** | AI-optimized search engine for gathering game lists. |
| **Data Source** | **Steam Store API** | Custom Python wrapper for fetching game data. |
| **Backend** | **FastAPI / Uvicorn** | Serves the agent as a RESTful API. |

## 📂 Project Structure

```bash
├── src/
│   ├── api.py           # FastAPI entry point
│   ├── graph.py         # LangGraph workflow definition
│   ├── nodes.py         # Agent (LLM) and Tool execution nodes
│   ├── tools.py         # Tool configuration and Tavily setup
│   ├── steam_api.py     # Custom Steam API wrapper (Optimized)
│   ├── config.py        # Environment variable management
│   └── state.py         # TypedDict for Agent State
├── .env                 # API Keys (Not included in repo)
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
