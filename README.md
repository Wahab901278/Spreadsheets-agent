# Spreadsheet Analysis Agent with LangGraph

A sophisticated agentic workflow that reads data from Google Sheets, analyzes it, generates insights using an LLM, and validates the output. Built with LangGraph for workflow orchestration.

## Architecture Overview

This project implements a complete agentic workflow with the following components:

```
Start
  |
  v
Node 1: Read Data (sheets.py)
  |
  v
Node 2: Analyze Data (analysis.py)
  |
  v
Node 3: Generate Insights (llm.py)
  |
  v
Node 4: Validate Output (graph.py)
  |
  v
End
```

## Where LangGraph is Used

LangGraph is the core orchestration framework used in this project. Here's where it appears:

### 1. Main Graph Definition (src/agent/graph.py)
   - StateGraph: Creates the workflow graph with defined states
   - AgentState: TypedDict that defines the state structure passed between nodes
   - Nodes: Four workflow nodes are defined:
     - node_read_data(): Reads from Google Sheets
     - node_analyze_data(): Analyzes the data
     - node_generate_insights(): Generates LLM insights
     - node_validate_output(): Validates and finalizes output
   - Command Pattern: Uses Command to return updates and control flow
   - Graph Compilation: graph.compile() creates the executable graph
   - Graph Edges: add_edge() defines the workflow path: START -> read_data -> analyze_data -> generate_insights -> validate_output -> END

### 2. Workflow Execution (main.py)
   - Invokes the compiled LangGraph: agent_graph.invoke(initial_state)
   - Passes state through the entire pipeline

## Project Structure

```
lang-graph-agent/
  main.py                      Entry point - executes the workflow
  requirements.txt             Project dependencies
  .env.example                 Environment variables template
  .gitignore
  src/
    agent/
      __init__.py
      graph.py            LangGraph workflow definition
      llm.py              LLM integration (Ollama/LangChain)
      analysis.py         Data analysis logic (pandas)
      sheets.py           Google Sheets integration
```

## Component Details

### 1. sheets.py - Google Sheets Integration
- SheetsConfig: Configuration dataclass for sheet parameters
- get_sheets_service(): Authenticates with Google Sheets API
- read_sheet(): Fetches data from specified range

### 2. analysis.py - Data Analysis
- analyze_rows(): Converts raw data to DataFrame
- Generates summary statistics for numerical and categorical columns
- Uses pandas for data processing

### 3. llm.py - LLM Integration
- get_ollama(): Creates ChatOllama instance for local LLM inference
- craft_prompt(): Constructs system and user messages
- llm_generate_insights(): Generates business insights from analysis

### 4. graph.py - LangGraph Workflow
- AgentState: Manages workflow state
- Node 1 (read_data): Reads from Google Sheets via SheetsConfig
- Node 2 (analyze_data): Analyzes using pandas
- Node 3 (generate_insights): Calls LLM for insights
- Node 4 (validate_output): Validates and handles errors
- create_agent_graph(): Assembles the StateGraph with edges and compiles it

## Setup Instructions

### Prerequisites
- Python 3.8+
- Google Service Account with Sheets API enabled
- Ollama running locally (or accessible LLM endpoint)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a .env file:
```bash
SPREADSHEET_ID=your_spreadsheet_id
READ_RANGE=Sheet1!A1:Z1000
WRITE_RANGE=Sheet1!AB1
GOOGLE_SERVICE_ACCOUNT_JSON=crediantials/service_account.json
LLM_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434
ANALYSIS_CONTEXT="Your custom analysis context"
```

### 3. Add Google Service Account
Place your service account JSON file at crediantials/service_account.json

### 4. Start Ollama (if using locally)
```bash
ollama serve
```

In another terminal:
```bash
ollama pull llama2
```

## Running the Agent

```bash
python main.py
```

### Sample Output
```
================================================================================
STARTING SPREADSHEET ANALYSIS AGENT
================================================================================

Creating LangGraph workflow...

Invoking workflow with the following config:
  - Spreadsheet ID: 1a2b3c4d...
  - Read Range: Sheet1!A1:Z1000
  - LLM Model: llama2
  - Ollama Base URL: http://localhost:11434

================================================================================
Node 1: Reading data from Google Sheets...
Successfully read 100 rows from sheet

Node 2: Analyzing data...
Data analysis completed

Node 3: Generating insights with LLM...
Insights generated successfully

Node 4: Validating output...
Output validation passed

================================================================================

WORKFLOW EXECUTION COMPLETED

Workflow completed successfully!

INSIGHTS GENERATED:
================================================================================
Sales trend shows 15% growth in Q3
Highest performing region: North America
Recommended focus area: Southeast region needs attention
================================================================================

FINAL STATE:
  - Data rows read: 100
  - Analysis completed: Yes
  - Insights generated: Yes

================================================================================
Agent execution completed successfully!
================================================================================
```

## Workflow Flow

### State Management with LangGraph

1. Initial State Creation
   ```python
   initial_state: AgentState = {
       "spreadsheet_id": "...",
       "read_range": "Sheet1!A1:Z1000",
       ...
   }
   ```

2. Node Execution
   - Each node receives the current state
   - Processes data using specific tools
   - Returns Command with updates
   - LangGraph updates the state

3. State Progression
   ```
   {} -> {"raw_data": [...]} 
   -> {"raw_data": [...], "analysis": {...}}
   -> {"raw_data": [...], "analysis": {...}, "insights": "..."}
   -> {"raw_data": [...], "analysis": {...}, "insights": "...", "error": ""}
   ```

4. Error Handling
   - Each node can set an "error" field
   - Later nodes check for errors and handle gracefully
   - Workflow completes even with errors

## Extending the Workflow

### Adding a New Node
```python
def node_send_email(state: AgentState) -> Command[AgentState]:
    insights = state.get("insights", "")
    return Command(update={"email_sent": True})

graph.add_node("send_email", node_send_email)
graph.add_edge("validate_output", "send_email")
```

### Adding Conditional Flow
```python
def decide_next_step(state: AgentState):
    if len(state.get("raw_data", [])) > 1000:
        return "generate_insights"
    else:
        return "validate_output"

graph.add_conditional_edges(
    "analyze_data",
    decide_next_step,
    {
        "generate_insights": "generate_insights",
        "validate_output": "validate_output"
    }
)
```

## Dependencies

| Package | Purpose |
|---------|---------|
| langgraph | Workflow orchestration and state management |
| langchain | LLM framework and utilities |
| langchain-ollama | Local LLM integration |
| pandas | Data analysis |
| google-api-python-client | Google Sheets API |
| google-auth-oauthlib | Google authentication |
| python-dotenv | Environment variable management |

## Security Notes

- Never commit .env files or credentials
- Use Google Service Account for authentication
- Store credentials securely
- Run Ollama on a secure network or use authentication

## License

MIT License

## ��� Where LangGraph is Used

LangGraph is the core orchestration framework used in this project. Here's where it appears:

### 1. **Main Graph Definition** (`src/agent/graph.py`)
   - **`StateGraph`**: Creates the workflow graph with defined states
   - **`AgentState`**: TypedDict that defines the state structure passed between nodes
   - **Nodes**: Four workflow nodes are defined:
     - `node_read_data()`: Reads from Google Sheets
     - `node_analyze_data()`: Analyzes the data
     - `node_generate_insights()`: Generates LLM insights
     - `node_validate_output()`: Validates and finalizes output
   - **Command Pattern**: Uses `Command` to return updates and control flow
   - **Graph Compilation**: `graph.compile()` creates the executable graph
   - **Graph Edges**: `add_edge()` defines the workflow path: START �� read_data → analyze_data → generate_insights → validate_output → END

### 2. **Workflow Execution** (`main.py`)
   - Invokes the compiled LangGraph: `agent_graph.invoke(initial_state)`
   - Passes state through the entire pipeline

## ��� Project Structure

```
lang-graph-agent/
��── main.py                      # Entry point - executes the workflow
��── requirements.txt             # Project dependencies
��── .env.example                 # Environment variables template
��── .gitignore
��── src/
    ��── agent/
        ��── __init__.py
        ��── graph.py            # ⭐ LangGraph workflow definition
        ��── llm.py              # LLM integration (Ollama/LangChain)
        ��── analysis.py         # Data analysis logic (pandas)
        ��── sheets.py           # Google Sheets integration
```

## ��� Component Details

### 1. **sheets.py** - Google Sheets Integration
- `SheetsConfig`: Configuration dataclass for sheet parameters
- `get_sheets_service()`: Authenticates with Google Sheets API
- `read_sheet()`: Fetches data from specified range

### 2. **analysis.py** - Data Analysis
- `analyze_rows()`: Converts raw data to DataFrame
- Generates summary statistics for numerical and categorical columns
- Uses pandas for data processing

### 3. **llm.py** - LLM Integration
- `get_ollama()`: Creates ChatOllama instance for local LLM inference
- `craft_prompt()`: Constructs system and user messages
- `llm_generate_insights()`: Generates business insights from analysis

### 4. **graph.py** - �� LangGraph Workflow
- **AgentState**: Manages workflow state
- **Node 1 (read_data)**: Reads from Google Sheets via SheetsConfig
- **Node 2 (analyze_data)**: Analyzes using pandas
- **Node 3 (generate_insights)**: Calls LLM for insights
- **Node 4 (validate_output)**: Validates and handles errors
- **create_agent_graph()**: Assembles the StateGraph with edges and compiles it

## ��� Setup Instructions

### Prerequisites
- Python 3.8+
- Google Service Account with Sheets API enabled
- Ollama running locally (or accessible LLM endpoint)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file:
```bash
SPREADSHEET_ID=your_spreadsheet_id
READ_RANGE=Sheet1!A1:Z1000
WRITE_RANGE=Sheet1!AB1
GOOGLE_SERVICE_ACCOUNT_JSON=crediantials/service_account.json
LLM_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434
ANALYSIS_CONTEXT="Your custom analysis context"
```

### 3. Add Google Service Account
Place your service account JSON file at `crediantials/service_account.json`

### 4. Start Ollama (if using locally)
```bash
ollama serve
# In another terminal:
ollama pull llama2
```

## ��️ Running the Agent

```bash
python main.py
```

### Sample Output
```
================================================================================
��� STARTING SPREADSHEET ANALYSIS AGENT
================================================================================

��� Creating LangGraph workflow...

��� Invoking workflow with the following config:
  - Spreadsheet ID: 1a2b3c4d...
  - Read Range: Sheet1!A1:Z1000
  - LLM Model: llama2
  - Ollama Base URL: http://localhost:11434

================================================================================
��� Node 1: Reading data from Google Sheets...
�� Successfully read 100 rows from sheet

��� Node 2: Analyzing data...
�� Data analysis completed

��� Node 3: Generating insights with LLM...
�� Insights generated successfully

��️ Node 4: Validating output...
�� Output validation passed

================================================================================

��� WORKFLOW EXECUTION COMPLETED

�� Workflow completed successfully!

��� INSIGHTS GENERATED:
��───────────────────────────────────────────────────────────────────────────────
�� Sales trend shows 15% growth in Q3
�� Highest performing region: North America
�� Recommended focus area: Southeast region needs attention
��───────────────────────────────────────────────────────────────────────────────

��� FINAL STATE:
  - Data rows read: 100
  - Analysis completed: Yes
  - Insights generated: Yes

================================================================================
�� Agent execution completed successfully!
================================================================================
```

## ��� Workflow Flow

### State Management with LangGraph

1. **Initial State Creation**
   ```python
   initial_state: AgentState = {
       "spreadsheet_id": "...",
       "read_range": "Sheet1!A1:Z1000",
       ...
   }
   ```

2. **Node Execution**
   - Each node receives the current state
   - Processes data using specific tools
   - Returns `Command` with updates
   - LangGraph updates the state

3. **State Progression**
   ```
   {} �� {"raw_data": [...]} 
   �� {"raw_data": [...], "analysis": {...}}
   �� {"raw_data": [...], "analysis": {...}, "insights": "..."}
   �� {"raw_data": [...], "analysis": {...}, "insights": "...", "error": ""}
   ```

4. **Error Handling**
   - Each node can set an "error" field
   - Later nodes check for errors and handle gracefully
   - Workflow completes even with errors

## ���️ Extending the Workflow

### Adding a New Node
```python
def node_send_email(state: AgentState) -> Command[AgentState]:
    """New node to send insights via email"""
    insights = state.get("insights", "")
    # Send email logic
    return Command(update={"email_sent": True})

# In create_agent_graph():
graph.add_node("send_email", node_send_email)
graph.add_edge("validate_output", "send_email")
```

### Adding Conditional Flow
```python
def decide_next_step(state: AgentState):
    if len(state.get("raw_data", [])) > 1000:
        return "generate_insights"
    else:
        return "validate_output"

graph.add_conditional_edges(
    "analyze_data",
    decide_next_step,
    {
        "generate_insights": "generate_insights",
        "validate_output": "validate_output"
    }
)
```

## ��� Dependencies

| Package | Purpose |
|---------|---------|
| **langgraph** | Workflow orchestration and state management |
| **langchain** | LLM framework and utilities |
| **langchain-ollama** | Local LLM integration |
| **pandas** | Data analysis |
| **google-api-python-client** | Google Sheets API |
| **google-auth-oauthlib** | Google authentication |
| **python-dotenv** | Environment variable management |

## ��� Security Notes

- Never commit `.env` files or credentials
- Use Google Service Account for authentication
- Store credentials securely
- Run Ollama on a secure network or use authentication

## ��� License

MIT License - Feel free to use and modify!

## ��� Contributing

Feel free to submit issues and enhancement requests!
