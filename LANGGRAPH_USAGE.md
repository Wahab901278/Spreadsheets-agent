# LangGraph Usage in This Project

## ��� Complete Guide: Where and How LangGraph is Used

### 1. **Core LangGraph Imports** (`src/agent/graph.py`)

```python
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
```

These imports are the foundation of the agentic workflow:
- **`StateGraph`**: Creates a directed graph for workflow orchestration
- **`START` & `END`**: Special nodes marking workflow entry and exit points
- **`Command`**: Returns state updates and control flow decisions from nodes

---

### 2. **State Definition** (`src/agent/graph.py`)

```python
class AgentState(TypedDict):
    """State for the agentic workflow"""
    spreadsheet_id: str
    read_range: str
    write_range: str
    service_account_json: str
    model: str
    base_url: str
    context: str
    raw_data: list          # �� Populated by node_read_data
    analysis: dict          # �� Populated by node_analyze_data
    insights: str           # �� Populated by node_generate_insights
    error: str              # �� Set if any node encounters an error
```

**Purpose**: Defines the shape of data that flows through the graph. LangGraph uses this TypedDict to:
- Validate state at each node
- Manage state transitions
- Ensure type safety across the workflow

---

### 3. **Node Definitions** (`src/agent/graph.py`)

Each node is a function that:
1. Receives the current state
2. Performs an action
3. Returns a `Command` with state updates

#### Node 1: Read Data from Google Sheets
```python
def node_read_data(state: AgentState) -> Command[AgentState]:
    """Node 1: Read data from Google Sheets"""
    config = SheetsConfig(...)
    raw_data = read_sheet(config)
    
    # Return Command to update state
    return Command(update={"raw_data": raw_data})
```
- **LangGraph Role**: Receives state, executes, returns updates
- **Data Flow**: `raw_data` added to state

#### Node 2: Analyze Data
```python
def node_analyze_data(state: AgentState) -> Command[AgentState]:
    """Node 2: Analyze the data"""
    raw_data = state.get("raw_data", [])
    analysis = analyze_rows(raw_data)
    
    return Command(update={"analysis": analysis})
```
- **LangGraph Role**: Consumes previous state, produces new state
- **Data Flow**: Uses `raw_data` -> produces `analysis`

#### Node 3: Generate Insights with LLM
```python
def node_generate_insights(state: AgentState) -> Command[AgentState]:
    """Node 3: Generate insights using LLM"""
    analysis = state.get("analysis", {})
    insights = llm_generate_insights(
        analysis=analysis,
        model=state.get("model"),
        base_url=state.get("base_url")
    )
    
    return Command(update={"insights": str(insights)})
```
- **LangGraph Role**: Orchestrates LLM calls through the pipeline
- **Data Flow**: Uses `analysis` -> produces `insights`

#### Node 4: Validate Output
```python
def node_validate_output(state: AgentState) -> Command[AgentState]:
    """Node 4: Validate and prepare output"""
    error = state.get("error")
    if error:
        return Command(goto=END)
    
    insights = state.get("insights", "")
    if not insights:
        return Command(update={"error": "No insights"}, goto=END)
    
    return Command(goto=END)
```
- **LangGraph Role**: Final validation before workflow completion
- **Flow Control**: Uses `goto=END` to terminate workflow
- **Error Handling**: Checks for errors and handles gracefully

---

### 4. **Graph Construction** (`src/agent/graph.py`)

```python
def create_agent_graph():
    """Create the LangGraph workflow"""
    
    # Step 1: Create StateGraph with AgentState
    graph = StateGraph(AgentState)
    
    # Step 2: Add all nodes
    graph.add_node("read_data", node_read_data)
    graph.add_node("analyze_data", node_analyze_data)
    graph.add_node("generate_insights", node_generate_insights)
    graph.add_node("validate_output", node_validate_output)
    
    # Step 3: Connect nodes with edges (workflow path)
    graph.add_edge(START, "read_data")
    graph.add_edge("read_data", "analyze_data")
    graph.add_edge("analyze_data", "generate_insights")
    graph.add_edge("generate_insights", "validate_output")
    
    # Step 4: Compile the graph for execution
    compiled_graph = graph.compile()
    
    return compiled_graph
```

**LangGraph Responsibilities**:
- `StateGraph(AgentState)`: Creates graph with state type
- `add_node()`: Registers workflow nodes
- `add_edge()`: Defines node connections (workflow path)
- `compile()`: Converts graph definition to executable form

---

### 5. **Graph Execution** (`main.py`)

```python
# Create the graph
agent_graph = create_agent_graph()

# Execute with initial state
final_state = agent_graph.invoke(initial_state)
```

**LangGraph Execution Flow**:
1. **Entry**: Start at `START` node
2. **Node 1**: Execute `node_read_data()` with initial state
3. **State Update**: Merge returned `Command` updates into state
4. **Node 2**: Execute `node_analyze_data()` with updated state
5. **State Update**: Merge new updates into state
6. **Node 3**: Execute `node_generate_insights()` with updated state
7. **State Update**: Merge insights into state
8. **Node 4**: Execute `node_validate_output()` with updated state
9. **Exit**: Reach `END` node
10. **Return**: Return final state with all accumulated data

---

### 6. **State Flow Diagram**

```
Initial State:
{
  spreadsheet_id: "...",
  read_range: "...",
  model: "llama2",
  raw_data: [],        �� Empty
  analysis: {},        �� Empty
  insights: "",        �� Empty
  error: ""
}
    ��
[node_read_data]
    ��
After Node 1:
{
  ...,
  raw_data: [[col1, col2, ...], [val1, val2, ...], ...],  �� Populated
  analysis: {},
  insights: "",
  error: ""
}
    ��
[node_analyze_data]
    ��
After Node 2:
{
  ...,
  raw_data: [...],
  analysis: {                                              �� Populated
    summary_of_numerical_columns: {...},
    summary_of_categorical_columns: {...}
  },
  insights: "",
  error: ""
}
    ��
[node_generate_insights]
    ��
After Node 3:
{
  ...,
  raw_data: [...],
  analysis: {...},
  insights: "�� Sales trend shows 15% growth...",          ← Populated
  error: ""
}
    ��
[node_validate_output]
    ��
Final State:
{
  ...,
  raw_data: [...],
  analysis: {...},
  insights: "...",
  error: "" (or error message if failed)
}
```

---

### 7. **Error Handling with LangGraph**

Each node has `try-except` to catch errors:

```python
try:
    # Do work
    result = read_sheet(config)
    return Command(update={"raw_data": result})
except Exception as e:
    # Return error in state
    return Command(update={"error": f"Data reading failed: {str(e)}"})
```

**LangGraph Benefit**: 
- Errors don't crash the workflow
- Error state persists through the graph
- Later nodes can check `state.get("error")` and handle gracefully

---

### 8. **Command Return Types**

Three main Command patterns used:

#### Pattern 1: Update State
```python
return Command(update={"raw_data": data})
```
- Updates state field and continues to next edge

#### Pattern 2: Conditional Flow
```python
if error:
    return Command(goto=END)
else:
    return Command(goto="next_node")
```
- Jumps to specific node or END

#### Pattern 3: Combined
```python
return Command(
    update={"error": "Something failed"},
    goto=END
)
```
- Updates state and jumps

---

## ��� Summary: Key LangGraph Concepts Used

| Concept | Location | Purpose |
|---------|----------|---------|
| **StateGraph** | `graph.py:create_agent_graph()` | Creates the workflow graph |
| **AgentState TypedDict** | `graph.py` | Defines state schema |
| **Nodes** | `graph.py:node_*()` functions | Workflow tasks |
| **Edges** | `graph.py:add_edge()` | Connections between nodes |
| **START/END** | `graph.py:add_edge()` | Entry/exit points |
| **Command** | All node functions | Return updates and flow control |
| **compile()** | `graph.py:create_agent_graph()` | Makes graph executable |
| **invoke()** | `main.py` | Executes the workflow |

---

##  Why LangGraph for This Project?

1. **Orchestration**: Manages complex multi-step workflows easily
2. **State Management**: Automatically threads state through nodes
3. **Error Resilience**: Continues execution even with errors
4. **Scalability**: Easy to add more nodes or conditional branches
5. **Observability**: Clear execution flow and state transitions
6. **Type Safety**: TypedDict ensures state structure consistency

---

## ��� Further Reading

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [StateGraph API](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.StateGraph)
- [Command Return Pattern](https://langchain-ai.github.io/langgraph/how-tos/return-values-as-output/)
