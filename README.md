# 🧭 Trip Planner — Multi-Agent System with LangGraph

This repo contains the code from **AI Playground Video 2**.  
In the previous video we built a single **Hotel Agent** — here we expand that into a **multi-agent trip planner** using [LangGraph](https://github.com/langchain-ai/langgraph).

## 🔹 What this project shows

We build a system of **AI Agents** that work together:

1. **Orchestrator Agent** → parses a free-text request into structured fields  
2. **Flights Agent** → proposes a flight (mocked, no API)  
3. **Hotels Agent** → suggests 3 realistic hotels as structured JSON  
4. **Calendar Agent** → computes travel dates and adds a note  
5. **Integrator Agent** → stitches everything into a final itinerary  

The flow looks like this:


```

User Request
      |
 Orchestrator
      |
 ┌───────────────┬───────────────┬───────────────┐
 Flights Agent   Hotels Agent    Calendar Agent
 └───────────────┴───────────────┴───────────────┘
      |
  Integrator
      |
  Final Itinerary
  ```


## 🔹 Why LangGraph?

LangGraph lets us model agent workflows as **graphs of nodes and edges**.  

- **Nodes** → Python functions that take state in and return updated state  
- **Edges** → the order of execution between nodes  
- **State** → shared memory that flows through the graph  

In this demo:  
- We **fan out** from the Orchestrator to three specialists  
- Then **fan in** to the Integrator to combine results  

## 🔹 Tech stack

- **LangGraph** → orchestration (state, nodes, edges)  
- **LangChain OpenAI** → easy OpenAI model calls  
- **Pydantic** → strict structured outputs  
- **dotenv** → load `OPENAI_API_KEY` safely from `.env`  

## 🔹 Repo structure

trip-planner-multiagent/
├─ schemas.py      
├─ state.py        
├─ agents.py       
├─ graph.py        
├─ demo.py         
├─ requirements.txt
└─ .env.example    

## 🔹 Setup & Run Locally

1. Clone this repo and install dependencies:

```bash
git clone https://github.com/learnwithme114-gif/simple-trip-planner-multiagent-langgraph-demo.git
cd simple-trip-planner-multiagent-langgraph-demo
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2. Add your OpenAI API key:

```bash
cp .env.example .env
# open .env and paste your key
```

3. Run the demo:

```bash
python demo.py
```

## 🔹 Related Repos

- [Hotel Agent Demo (Github Rep)](https://github.com/learnwithme114-gif/simple-hotel-agent-langraph)  
- **This repo (Video 2):** Trip Planner Multi-Agent  
- (Coming soon) [Trip Planner API (Video 3)]()

## 📺 Watch the Video

👉 [YouTube: Single Agent  (LangGraph)](https://youtu.be/PulES62ScoA)
👉 [YouTube: Multi-Agent Trip Planner (LangGraph)](https://youtu.be/SMYlq8nCcKU)
