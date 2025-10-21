# ��� Quick Reference: LangGraph Usage in This Project

## One-Liner Summary
**LangGraph orchestrates a 4-node agentic workflow in `src/agent/graph.py` that reads data from Google Sheets, analyzes it, generates LLM insights, and validates the output.**

---

## ��� LangGraph Locations

### Primary File: `src/agent/graph.py`

```python
# 1. IMPORTS
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

# 2. STATE DEFINITION
class AgentState(TypedDict):
    raw_data: list
    analysis: dict
    insights: str
    error: str

# 3. NODES (4 functions)
def node_read_data(state) -> Command
def node_analyze_data(state) -> Command
def node_generate_insights(state) -> Command
def node_validate_output(state) -> Command

# 4. GRAPH ASSEMBLY
graph = StateGraph(AgentState)
graph.add_node(name, function)      # 4 nodes
graph.add_edge(source, target)      # 5 edges
compiled_graph = graph.compile()

# 5. EXECUTION (in main.py)
result = compiled_graph.invoke(initial_state)
```

---

## ��� The Workflow

```
START
  ��
node_read_data        -> Reads from Google Sheets
  ��
node_analyze_data     -> Analyzes with pandas
  ��
node_generate_insights -> Calls LLM for insights
  ��
node_validate_output  -> Validates & returns
  ��
END
```

---

## ��� State Flow

```
Input:  { spreadsheet_id, model, base_url, ... }
         
Step 1: + raw_data = [[...], [...], ...]
        
Step 2: + analysis = {numerical: {...}, categorical: {...}}
        
Step 3: + insights = "Key findings: ..."
        
Step 4: + error = "" (or error message)

Output: { All of the above }
```

---

## ��� Each Node's Job

| Node | Input | Process | Output |
|------|-------|---------|--------|
| **read_data** | `spreadsheet_id`, `read_range` | Use Google Sheets API | `raw_data: list` |
| **analyze_data** | `raw_data` | Pandas describe() | `analysis: dict` |
| **generate_insights** | `analysis`, `model` | Call LLM | `insights: str` |
| **validate_output** | `insights`, `error` | Check completion | -> END |

---

##  Execution Sequence

```python
# 1. Create graph
graph = create_agent_graph()  # From graph.py

# 2. Prepare state
state = {
    "spreadsheet_id": "...",
    "read_range": "Sheet1!A1:Z",
    "model": "llama2",
    "base_url": "http://localhost:11434",
    "raw_data": [],
    "analysis": {},
    "insights": "",
    "error": ""
}

# 3. Run workflow
result = graph.invoke(state)

# 4. Get results
print(result["insights"])    # �� The generated insights
print(result["error"])       # �� Error if any
```

---

## ��� LangGraph Components Used

### StateGraph
```python
graph = StateGraph(AgentState)
```
- Container for the workflow
- Holds nodes and edges
- Type-checked with AgentState

### Nodes
```python
graph.add_node("read_data", node_read_data)
```
- 4 nodes total
- Each receives state, returns Command
- Execute in sequence

### Edges
```python
graph.add_edge(START, "read_data")
graph.add_edge("read_data", "analyze_data")
# etc.
```
- Define workflow path
- Linear sequence: START -> Node1 -> Node2 -> Node3 -> Node4 -> END

### Command
```python
return Command(update={"raw_data": data})
return Command(goto=END)
```
- Node return type
- Carries state updates
- Controls flow direction

### Compilation
```python
compiled_graph = graph.compile()
```
- Makes graph executable
- Validates structure
- Returns runnable graph

### Invocation
```python
final_state = compiled_graph.invoke(initial_state)
```
- Starts workflow
- Returns final state
- Blocks until complete

---

## ��� Key Features Used

1. **Type Safety**: `AgentState` TypedDict
2. **State Threading**: Auto state passing between nodes
3. **Error Handling**: Try-except in each node
4. **Flow Control**: `Command(goto=END)`
5. **Linear Workflow**: 5 edges connecting 4 nodes

---

## ��️ How to Extend

### Add a new node
```python
def node_new_task(state: AgentState) -> Command[AgentState]:
    # Do work
    return Command(update={"new_field": result})

graph.add_node("new_task", node_new_task)
graph.add_edge("validate_output", "new_task")
```

### Add conditional logic
```python
def node_decide(state: AgentState):
    if state["analysis"]["summary"]:
        return "generate_insights"
    else:
        return "validate_output"

graph.add_conditional_edges(
    "analyze_data",
    node_decide,
    {...}
)
```

### Run with graph visualization
```python
# LangGraph has built-in visualization
graph.get_graph().draw_mermaid_png("workflow.png")
```

---

## ��� Files in Project

```
lang-graph-agent/
��── main.py                    ← Entry point (runs graph)
��── src/agent/
��   ├── graph.py              ←  LangGraph definition
��   ├── sheets.py             ← Google Sheets
��   ├── analysis.py           ← Data analysis
��   └── llm.py                ← LLM integration
��── requirements.txt          ← Dependencies (includes langgraph)
��── .env.example              ← Config template
��── README.md                 ← Full docs
��── LANGGRAPH_USAGE.md        ← Detailed guide
��── WORKFLOW_SUMMARY.md       ← This summary

```

---

##  Run It

```bash
# 1. Setup
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your settings

# 3. Run
python main.py
```

---

## ��� Remember

- **StateGraph**: The graph container
- **AgentState**: The state schema (what flows through)
- **Nodes**: The work units (4 of them)
- **Edges**: The connections (START -> N1 -> N2 -> N3 -> N4 -> END)
- **Command**: Node return value (updates state, controls flow)
- **compile()**: Prepares graph for execution
- **invoke()**: Runs the workflow

**All managed by LangGraph! ���**
