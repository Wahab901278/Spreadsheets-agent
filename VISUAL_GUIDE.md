# ��� Visual Guide: LangGraph in Action

## The Complete Workflow Visualization

```
��━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
��                         MAIN ENTRY POINT                        ┃
��                         main.py                                 ┃
��  • Load environment variables                                  ┃
��  • Initialize configuration                                    ┃
��  • Create initial state                                        ┃
��━━━━━━━━━━━━━━━━━┬━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                  ��
                  �� agent_graph = create_agent_graph()
                  ��
                  ��
��━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
��                  LANGGRAPH CONSTRUCTION                          ┃
��                   graph.py:create_agent_graph()                ┃
��                                                                 ┃
��  graph = StateGraph(AgentState)                               ┃
��  ├─ graph.add_node("read_data", node_read_data)              ┃
��  ├─ graph.add_node("analyze_data", node_analyze_data)        ┃
��  ├─ graph.add_node("generate_insights", node_generate_insights)
��  ├─ graph.add_node("validate_output", node_validate_output)  ┃
��  ├─ graph.add_edge(START, "read_data")                       ┃
��  ├─ graph.add_edge("read_data", "analyze_data")              ┃
��  ├─ graph.add_edge("analyze_data", "generate_insights")      ┃
��  └─ graph.add_edge("generate_insights", "validate_output")   ┃
��  compiled_graph = graph.compile()                            ┃
��━━━━━━━━━━━━━━━━━┬━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                  ��
                  �� final_state = agent_graph.invoke(initial_state)
                  ��
                  ��
��━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
��                    WORKFLOW EXECUTION                            ┃
��                  Managed by LangGraph.invoke()                 ┃
��━━━━━━━━━━━━━━━━━┬━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                  ��
        ��========─┴============┬============──┬============──┐
        ��                      │              │              │
        ��                      ▼              ▼              ▼
    ��========┐           ┌========──┐   ┌========──┐   ┌========──┐
    �� START  │           │          │   │          │   │          │
    ��====┬───┘           │          │   │          │   │          │
         ��               │          │   │          │   │          │
         ��               │          │   │          │   │          │
         ��========──┐    │          │   │          │   │          │
                    ��    │          │   │          │   │          │
                    ��    │          │   │          │   │          │
             ��========──┐│          │   │          │   │          │
             �� Node 1   ││          │   │          │   │          │
             ��Read Data ││          │   │          │   │          │
             ��====┬====─┘│          │   │          │   │          │
                  ��      │          │   │          │   │          │
      State: {raw_data}  ��          │   │          │   │          │
                  ��      │          │   │          │   │          │
                  ��====──┼====┐     │   │          │   │          │
                         ��    │     │   │          │   │          │
                         ��    │     │   │          │   │          │
                  ��========──┐ │     │   │          │   │          │
                  �� Node 2   │ │     │   │          │   │          │
                  ��Analyze   │ │     │   │          │   │          │
                  ��  Data    │ │     │   │          │   │          │
                  ��====┬====─┘ │     │   │          │   │          │
                       ��       │     │   │          │   │          │
           State: +{analysis}  ��     │   │          │   │          │
                       ��       │     │   │          │   │          │
                       ��====───┼====─┼───┐         │   │          │
                               ��     │   │         │   │          │
                               ��     │   │         │   │          │
                        ��========──┐ │   │         │   │          │
                        �� Node 3   │ │   │         │   │          │
                        ��Generate  │ │   │         │   │          │
                        ��Insights  │ │   │         │   │          │
                        ��====┬====─┘ │   │         │   │          │
                             ��       │   │         │   │          │
                  State: +{insights} ��   │         │   │          │
                             ��       │   │         │   │          │
                             ��====───┼───┼========─┼───┐          │
                                     ��   │         │   │          │
                                     ��   │         │   │          │
                              ��========──┐         │   │          │
                              �� Node 4   │         │   │          │
                              ��Validate  │         │   │          │
                              �� Output   │         │   │          │
                              ��====┬====─┘         │   │          │
                                   ��               │   │          │
                    State: check error/insights    ��   │          │
                                   ��               │   │          │
                                   ��========───┬───┘   │          │
                                               ��       │          │
                                               ��       │          │
                                            ��====──┐   │          │
                                            �� END  │   │          │
                                            ��====──┘   │          │
                                                       ��          │
                                                       ��========──┘
                                                     (All nodes
                                                      eventually
                                                      reach END)
        ��
        ��========================─┐
                                  ��
                                  ��
��━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
��                      FINAL STATE RETURNED                        ┃
��                   {all state fields populated}                  ┃
��                      Back to main.py                            ┃
��━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                  ��
                                  �� Display results
                                  �� Return exit code
                                  ��
                        ��================──┐
                        ��   Workflow Done  │
                        ��================──┘
```

---

## State Transformation Through Nodes

```
��====================================─┐
��       INITIAL STATE (Input)         │
��====================================─┤
�� {                                   │
��   spreadsheet_id: "123abc",         │
��   read_range: "Sheet1!A1:Z100",    │
��   model: "llama2",                  │
��   base_url: "http://localhost:...", │
��   raw_data: [],          ← EMPTY   │
��   analysis: {},          ← EMPTY   │
��   insights: "",          ← EMPTY   │
��   error: ""                         │
�� }                                   │
��============┬========================┘
             ��
             �� Node 1: node_read_data()
             �� Reads from Google Sheets via sheets.py
             �� Returns: Command(update={"raw_data": [...]})
             ��
��====================================─┐
��     AFTER NODE 1 (raw_data added)   │
��====================================─┤
�� {                                   │
��   spreadsheet_id: "123abc",         │
��   read_range: "Sheet1!A1:Z100",    │
��   model: "llama2",                  │
��   base_url: "http://localhost:...", │
��   raw_data: [              ← FILLED │
��     ["Name", "Sales", "Region"],   │
��     ["Alice", 1000, "North"],      │
��     ["Bob", 1500, "South"],        │
��     ...                             │
��   ],                                │
��   analysis: {},          ← Still empty
��   insights: "",          ← Still empty
��   error: ""                         │
�� }                                   │
��============┬========================┘
             ��
             �� Node 2: node_analyze_data()
             �� Analyzes with pandas via analysis.py
             �� Returns: Command(update={"analysis": {...}})
             ��
��====================================─┐
��   AFTER NODE 2 (analysis added)     │
��====================================─┤
�� {                                   │
��   spreadsheet_id: "123abc",         │
��   read_range: "Sheet1!A1:Z100",    │
��   model: "llama2",                  │
��   base_url: "http://localhost:...", │
��   raw_data: [...],                  │
��   analysis: {            ← FILLED  │
��     "summary_of_numerical_columns": {
��       "summary": "Sales        │
��        count    1000.0          │
��        mean      1250.0         │
��        std        250.0         │
��        ..."                      │
��     },                            │
��     "summary_of_categorical...": {
��       "summary": "Region      │
��        North    500            │
��        South    500            │
��        ..."                     │
��     }                            │
��   },                             │
��   insights: "",        ← Still empty
��   error: ""                      │
�� }                                │
��============┬====================─┘
             ��
             �� Node 3: node_generate_insights()
             �� Calls LLM via llm.py
             �� Returns: Command(update={"insights": "..."})
             ��
��====================================─┐
��  AFTER NODE 3 (insights added)      │
��====================================─┤
�� {                                   │
��   spreadsheet_id: "123abc",         │
��   read_range: "Sheet1!A1:Z100",    │
��   model: "llama2",                  │
��   base_url: "http://localhost:...", │
��   raw_data: [...],                  │
��   analysis: {...},                  │
��   insights: "              ← FILLED │
��     • Sales demonstrate solid       │
��       performance averaging 1250    │
��                                     │
��     • Region distribution shows     │
��       balanced split between North  │
��       and South                     │
��                                     │
��     • Recommendation: Expand        │
��       marketing efforts in South    │
��       region",                      │
��   error: ""                         │
�� }                                   │
��============┬========================─┘
             ��
             �� Node 4: node_validate_output()
             �� Validates and prepares to END
             �� Returns: Command(goto=END)
             ��
��====================================─┐
��     FINAL STATE (Complete)          │
��====================================─┤
�� {                                   │
��   spreadsheet_id: "123abc",         │
��   read_range: "Sheet1!A1:Z100",    │
��   model: "llama2",                  │
��   base_url: "http://localhost:...", │
��   raw_data: [...],                  │
��   analysis: {...},                  │
��   insights: "...",                  │
��   error: ""                         │
�� }                                   │
��  Ready to display/process         │
��====================================─┘
```

---

## Node Function Pattern

```
��====================================================─┐
��         Generic Node Function Pattern               │
��====================================================─┘

def node_task_name(state: AgentState) -> Command[AgentState]:
    """
    Step 1: Receive current state from LangGraph
    Step 2: Extract needed data from state
    Step 3: Perform the actual work
    Step 4: Handle errors gracefully
    Step 5: Return Command with updates
    """
    
    try:
        # Step 2: Extract from state
        input_data = state.get("field_name", default_value)
        
        # Step 3: Do work using other modules
        result = external_function(input_data)
        
        # Step 5a: Success - return with update
        return Command(update={"output_field": result})
        
    except Exception as e:
        # Step 4: Error handling
        logger.error(f"Task failed: {str(e)}")
        
        # Step 5b: Error - set error field
        return Command(update={"error": str(e)})


��====================================================─┐
��         Actual Implementation Example               │
��          node_generate_insights()                  │
��====================================================─┘

def node_generate_insights(state: AgentState) -> Command[AgentState]:
    logger.info("��� Node 3: Generating insights with LLM...")
    try:
        # Extract data
        analysis = state.get("analysis", {})
        model = state.get("model", "llama2")
        base_url = state.get("base_url")
        
        # Check previous node success
        if "error" in analysis:
            return Command(update={...})
        
        # Perform work
        insights = llm_generate_insights(
            analysis=analysis,
            model=model,
            base_url=base_url
        )
        
        # Return update
        return Command(update={"insights": str(insights)})
        
    except Exception as e:
        logger.error(f"�� Insights generation failed: {str(e)}")
        return Command(update={"error": f"Insights generation failed..."})
```

---

## LangGraph Component Hierarchy

```
��========================================================──┐
��                    StateGraph                            │
��  (Container for entire workflow)                         │
��                                                          │
��  ┌====================================================┐ │
��  │  Node: START (Special Entry Node)                  │ │
��  │  ↓                                                 │ │
��  │  ┌================─┐                               │ │
��  │  │  Node 1         │  (Receives state)             │ │
��  │  │  read_data      │  (Returns Command)            │ │
��  │  └================─┘                               │ │
��  │  ↓                                                 │ │
��  │  ┌================─┐                               │ │
��  │  │  Node 2         │  (Gets updated state)         │ │
��  │  │  analyze_data   │  (Returns Command)            │ │
��  │  └================─┘                               │ │
��  │  ↓                                                 │ │
��  │  ┌================─┐                               │ │
��  │  │  Node 3         │  (Gets updated state)         │ │
��  │  │generate_insights│  (Returns Command)            │ │
��  │  └================─┘                               │ │
��  │  ↓                                                 │ │
��  │  ┌================─┐                               │ │
��  │  │  Node 4         │  (Gets updated state)         │ │
��  │  │validate_output  │  (Returns Command(goto=END))  │ │
��  │  └================─┘                               │ │
��  │  ↓                                                 │ │
��  │  Node: END (Special Exit Node)                    │ │
��  └====================================================┘ │
��                                                          │
��  AgentState TypedDict:                                  │
��  ├─ spreadsheet_id: str                                │
��  ├─ read_range: str                                    │
��  ├─ raw_data: list (← Filled by Node 1)               │
��  ├─ analysis: dict (← Filled by Node 2)               │
��  ├─ insights: str (← Filled by Node 3)                │
��  └─ error: str (← Set if errors occur)                │
��========================================================──┘
```

---

## Execution Timeline

```
TIME �� COMPONENT           │ ACTION
====��┼====================┼================================──
T0   �� main.py            │ Load config, create initial state
T1   �� main.py            │ Call create_agent_graph()
T2   �� graph.py           │ Create StateGraph
T3   �� graph.py           │ Add 4 nodes to graph
T4   �� graph.py           │ Add 5 edges to graph
T5   �� graph.py           │ Compile graph
T6   �� main.py            │ Call agent_graph.invoke(state)
T7   �� LangGraph          │ START
T8   �� LangGraph          │ Execute Node 1
T9   �� node_read_data()   │ sheets.py -> Google Sheets API
T10  �� node_read_data()   │ Return with raw_data
T11  �� LangGraph          │ Update state + Execute Node 2
T12  �� node_analyze_data()│ analysis.py -> pandas
T13  �� node_analyze_data()│ Return with analysis
T14  �� LangGraph          │ Update state + Execute Node 3
T15  �� node_generate...() │ llm.py -> ChatOllama
T16  �� node_generate...() │ Return with insights
T17  �� LangGraph          │ Update state + Execute Node 4
T18  �� node_validate...() │ Check and prepare output
T19  �� node_validate...() │ Return Command(goto=END)
T20  �� LangGraph          │ END
T21  �� main.py            │ Receive final_state
T22  �� main.py            │ Display results
T23  �� main.py            │ Exit
```

---

**LangGraph manages all timing and coordination automatically!** ��
