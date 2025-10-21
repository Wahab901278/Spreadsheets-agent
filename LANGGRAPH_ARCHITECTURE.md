LANGGRAPH WORKFLOW ARCHITECTURE
================================================================================

WHERE LANGGRAPH IS USED: src/agent/graph.py

VISUAL WORKFLOW

              INPUT STATE
                  |
                  v
        START (LangGraph START)
                  |
                  v
        +-------------------+
        | node_read_data()  |  Reads Google Sheets
        |                   |  Uses: sheets.py
        |  Returns:         |  Returns: Command(update={"raw_data": [...]})
        +--------+----------+
                 |
                 v
        +-------------------+
        |node_analyze_data()| Analyzes with Pandas
        |                   | Uses: analysis.py
        |  Returns:         | Returns: Command(update={"analysis": {...}})
        +--------+----------+
                 |
                 v
    +---------------------+
    |node_generate_        | Generates Insights
    |insights()            | Uses: llm.py (ChatOllama)
    |                      | Returns: Command(update={"insights": "..."})
    +--------+-------------+
             |
             v
    +---------------------+
    |node_validate_        | Validates Output
    |output()              | Returns: Command(goto=END)
    +--------+-------------+
             |
             v
        END (LangGraph END)
             |
             v
        FINAL STATE
      (all fields updated)


STATE FLOW DIAGRAM

Initial State:
{
    spreadsheet_id: "abc...",
    read_range: "Sheet1!A1:Z1000",
    model: "llama2",
    raw_data: [],
    analysis: {},
    insights: "",
    error: ""
}
                    |
                    v
        Node 1: read_data() executes
                    |
    State updated: raw_data populated
                    |
                    v
        Node 2: analyze_data() executes
                    |
    State updated: analysis populated
                    |
                    v
        Node 3: generate_insights() executes
                    |
    State updated: insights populated
                    |
                    v
        Node 4: validate_output() executes
                    |
    State updated: error field checked
                    |
                    v
        Final State (all fields complete)


LANGGRAPH COMPONENTS IN CODE

1. IMPORTS
   from langgraph.graph import StateGraph, START, END
   from langgraph.types import Command

2. STATE DEFINITION
   class AgentState(TypedDict):
       spreadsheet_id: str
       read_range: str
       write_range: str
       service_account_json: str
       model: str
       base_url: str
       context: str
       raw_data: list
       analysis: dict
       insights: str
       error: str

3. NODE FUNCTIONS
   def node_read_data(state: AgentState) -> Command[AgentState]:
       ...logic...
       return Command(update={"raw_data": raw_data})

   def node_analyze_data(state: AgentState) -> Command[AgentState]:
       ...logic...
       return Command(update={"analysis": analysis})

   def node_generate_insights(state: AgentState) -> Command[AgentState]:
       ...logic...
       return Command(update={"insights": insights})

   def node_validate_output(state: AgentState) -> Command[AgentState]:
       ...logic...
       return Command(goto=END)

4. GRAPH CONSTRUCTION
   graph = StateGraph(AgentState)

5. NODE REGISTRATION
   graph.add_node("read_data", node_read_data)
   graph.add_node("analyze_data", node_analyze_data)
   graph.add_node("generate_insights", node_generate_insights)
   graph.add_node("validate_output", node_validate_output)

6. EDGE DEFINITION
   graph.add_edge(START, "read_data")
   graph.add_edge("read_data", "analyze_data")
   graph.add_edge("analyze_data", "generate_insights")
   graph.add_edge("generate_insights", "validate_output")

7. GRAPH COMPILATION
   compiled_graph = graph.compile()
   return compiled_graph

8. EXECUTION (in main.py)
   agent_graph = create_agent_graph()
   final_state = agent_graph.invoke(initial_state)


COMMAND PATTERN EXPLANATION

Each node returns a Command object that can:

1. Update State:
   Command(update={"field": value})
   
   This adds/updates fields in AgentState

2. Control Flow:
   Command(goto=END)
   Command(goto="node_name")
   
   This controls where the workflow goes next

3. Both:
   Command(update={"field": value}, goto="next_node")


ERROR HANDLING IN LANGGRAPH

Each node can set error field:
return Command(update={"error": "error message"})

Later nodes check for errors:
if state.get("error"):
    # Handle error
    return Command(update={"error": error})

Workflow completes gracefully even with errors.


DATA FLOW THROUGH NODES

START
  |
  v
Node 1: raw_data = []      --->  raw_data populated
  |
  v
Node 2: analysis = {}      --->  analysis populated
  |
  v
Node 3: insights = ""      --->  insights populated
  |
  v
Node 4: validates results  --->  Final state ready
  |
  v
END


INTEGRATION WITH OTHER MODULES

LangGraph (graph.py)
    |
    +---> Google Sheets (sheets.py)
    |     - read_sheet(config)
    |     - SheetsConfig class
    |
    +---> Data Analysis (analysis.py)
    |     - analyze_rows(rows)
    |     - Returns statistics
    |
    +---> LLM Integration (llm.py)
    |     - llm_generate_insights(analysis, model, base_url)
    |     - Uses ChatOllama
    |
    +---> Main Orchestration (main.py)
          - create_agent_graph()
          - agent_graph.invoke(state)
          - Display results


KEY LANGGRAPH FEATURES USED

1. StateGraph
   - Type-safe workflow definition
   - Automatic state threading

2. AgentState
   - Consistent state schema
   - TypedDict validation

3. Nodes
   - Modular functions
   - Isolated logic

4. Edges
   - Clear task ordering
   - Linear workflow path

5. Command
   - State updates
   - Flow control

6. START/END
   - Workflow boundaries
   - Entry and exit points

7. compile()
   - Graph preparation
   - Optimization

8. invoke()
   - Workflow execution
   - Returns final state


WHY LANGGRAPH FOR THIS PROJECT

1. State Management
   - Automatic state threading between nodes
   - No manual state passing

2. Modularity
   - Each step isolated in own node
   - Easy to test and extend

3. Error Resilience
   - Individual node failures handled
   - Workflow continues gracefully

4. Extensibility
   - Add nodes easily
   - Add conditional branches
   - Parallel execution possible

5. Type Safety
   - TypedDict ensures consistency
   - Type hints throughout

6. Observability
   - Clear execution flow
   - State transitions visible
   - Easy to debug

7. Production Ready
   - Error handling built-in
   - Logging integration
   - Robust execution


WORKFLOW EXECUTION SEQUENCE

1. main.py calls: agent_graph = create_agent_graph()
2. create_agent_graph() creates StateGraph(AgentState)
3. Adds 4 nodes: read_data, analyze_data, generate_insights, validate_output
4. Adds edges: START -> read_data -> analyze_data -> generate_insights -> validate_output
5. Compiles graph: graph.compile()
6. main.py creates initial_state with configuration
7. main.py invokes: final_state = agent_graph.invoke(initial_state)
8. LangGraph executes nodes in order:
   - Node 1: Reads data, updates state
   - Node 2: Analyzes data, updates state
   - Node 3: Generates insights, updates state
   - Node 4: Validates output, returns final state
9. main.py receives final_state with all results
10. Displays results and logs

COMPLETE LANGGRAPH USAGE: src/agent/graph.py (120 lines)
