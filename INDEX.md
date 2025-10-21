# ��� Complete Project Index

## ��� Project Overview

**Spreadsheet Analysis Agent with LangGraph** - A complete agentic workflow that:
1. Reads data from Google Sheets
2. Analyzes it with pandas
3. Generates business insights using an LLM
4. Validates and returns results

All orchestrated by **LangGraph**, a graph-based workflow framework.

---

## ��� Project Structure

### Root Level Files

| File | Purpose |
|------|---------|
| **main.py** |  Entry point - runs the complete workflow |
| **requirements.txt** | ��� All Python dependencies |
| **.env.example** | ��️ Configuration template |
| **.gitignore** | ��� Git ignore file |
| **README.md** | ��� Complete project documentation |

### Documentation Files

| File | Content |
|------|---------|
| **WORKFLOW_SUMMARY.md** | Complete workflow overview with state flow |
| **LANGGRAPH_USAGE.md** | Detailed LangGraph implementation guide |
| **QUICK_REFERENCE.md** | Quick one-page reference guide |
| **INDEX.md** | This file |

### Source Code (`src/agent/`)

| File | Functionality |
|------|---------------|
| **graph.py** |  LangGraph workflow definition (4 nodes + edges) |
| **llm.py** | LLM integration (ChatOllama, prompt crafting) |
| **analysis.py** | Data analysis (pandas describe, statistics) |
| **sheets.py** | Google Sheets API integration |
| **__init__.py** | Package initialization |

---

## ��� Quick Navigation

### ��� For Getting Started
-> Start with **README.md**

### ���️ For Understanding Architecture
-> Read **WORKFLOW_SUMMARY.md**

### ��� For Understanding LangGraph
-> Read **LANGGRAPH_USAGE.md**

### �� For Quick Reference
-> Check **QUICK_REFERENCE.md**

### ��� For Running the Code
-> Execute `python main.py`

---

## ��� Where LangGraph is Used

### Main Implementation
**File: `src/agent/graph.py`**

```python
# LangGraph Imports
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

# LangGraph Components:
1. AgentState TypedDict      - Defines state schema
2. 4 Node Functions          - Workflow tasks
3. StateGraph Creation       - Graph assembly
4. Edge Definitions          - Workflow connections
5. Graph Compilation         - Execution preparation
```

### Execution
**File: `main.py`**
```python
agent_graph = create_agent_graph()  # From graph.py
final_state = agent_graph.invoke(initial_state)  # Execute workflow
```

---

## ��� The 4-Node Workflow

```
Node 1: Read Data
��── Input: spreadsheet_id, read_range
��── Process: Fetch from Google Sheets
��── Output: raw_data (list of lists)

Node 2: Analyze Data
��── Input: raw_data
��── Process: Pandas describe() for statistics
��── Output: analysis (numerical + categorical summaries)

Node 3: Generate Insights
��── Input: analysis, model, base_url
��── Process: Send to LLM for interpretation
��── Output: insights (business-friendly summary)

Node 4: Validate Output
��── Input: insights, error
��── Process: Check for errors and completeness
��── Output: -> END (workflow completion)
```

---

## ��� State Flow Diagram

```
Initial State
��
Node 1: Read Data
��─ Output: {"raw_data": [...]}
��
Node 2: Analyze Data
��─ Output: {"analysis": {...}}
��
Node 3: Generate Insights
��─ Output: {"insights": "..."}
��
Node 4: Validate
��─ Output: Final state with all fields
��
Final State
```

---

##  Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Configuration
```bash
cp .env.example .env
# Edit .env with your settings:
# - SPREADSHEET_ID
# - GOOGLE_SERVICE_ACCOUNT_JSON path
# - LLM_MODEL and OLLAMA_BASE_URL
```

### 3. Run
```bash
python main.py
```

---

## ��� Key Concepts

### LangGraph Core
- **StateGraph**: Container for workflow nodes and edges
- **AgentState**: TypedDict defining state structure
- **Command**: Node return type (state updates + flow control)
- **START/END**: Special nodes for workflow entry/exit
- **Edges**: Connections between nodes

### Workflow Patterns Used
1. **Linear Flow**: Sequential node execution
2. **Error Handling**: Each node has try-except
3. **State Threading**: Automatic state passing
4. **Type Safety**: TypedDict validation

---

## ��� Dependencies

```
langgraph              - Workflow orchestration 
langchain             - LLM framework
langchain-ollama      - Local LLM integration
pandas                - Data analysis
google-auth           - Google authentication
google-api-python-client - Google Sheets API
python-dotenv         - Environment variables
```

---

## ��� Learning Path

### Beginner
1. Read **README.md** for overview
2. Check **QUICK_REFERENCE.md** for quick understanding
3. Run `python main.py` to see it work

### Intermediate
1. Read **WORKFLOW_SUMMARY.md** for architecture
2. Review `src/agent/graph.py` for implementation
3. Understand each node's function

### Advanced
1. Study **LANGGRAPH_USAGE.md** for deep dive
2. Analyze state flow and Command patterns
3. Plan extensions (conditional logic, parallel nodes, etc.)

---

## ��� Extension Ideas

### Easy Additions
- [ ] Add logging to each node
- [ ] Cache analysis results
- [ ] Add retry logic for LLM

### Medium Complexity
- [ ] Conditional branching (sample large datasets)
- [ ] Parallel analysis (numerical + categorical simultaneously)
- [ ] Write results back to Google Sheets

### Advanced
- [ ] Multi-threaded execution
- [ ] Streaming LLM responses
- [ ] Human-in-the-loop validation
- [ ] Graph visualization

---

## ��� File Relationships

```
main.py
��── imports from src/agent/graph.py
��   ├── imports from src/agent/sheets.py
��   ├── imports from src/agent/analysis.py
��   └── imports from src/agent/llm.py
��
��── .env (configuration)
```

---

##  Completion Checklist

-  Complete agentic workflow implemented
-  4-node LangGraph system created
-  Google Sheets integration working
-  Data analysis with pandas functional
-  LLM integration with Ollama ready
-  Error handling at each node
-  State management throughout
-  Main entry point created
-  All documentation complete
-  Quick reference guides provided

---

## ��� One-Liner Summary

**A LangGraph-orchestrated workflow in `graph.py` reads data from Google Sheets (Node 1), analyzes it with pandas (Node 2), generates LLM insights (Node 3), and validates output (Node 4), all invoked from `main.py` with automatic state threading.**

---

## ��� Quick Links to Key Files

- **Start Here**: [README.md](README.md)
- **Understand LangGraph**: [LANGGRAPH_USAGE.md](LANGGRAPH_USAGE.md)
- **Full Workflow**: [WORKFLOW_SUMMARY.md](WORKFLOW_SUMMARY.md)
- **Quick Reference**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Implementation**: [src/agent/graph.py](src/agent/graph.py)
- **Main Entry**: [main.py](main.py)

---

## ��� Project Highlights

1. **Production-Ready**: Error handling, logging, configuration management
2. **Well-Documented**: 4 comprehensive documentation files
3. **Modular Design**: Each component is independent and testable
4. **LangGraph Power**: Leverages graph-based orchestration
5. **Extensible**: Easy to add new nodes or conditional logic
6. **Type-Safe**: TypedDict ensures state consistency

---

**Happy analyzing! **
