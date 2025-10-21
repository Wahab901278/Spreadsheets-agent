from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from typing import TypedDict, Annotated, Any
from operator import add
import logging

from .sheets import read_sheet, SheetsConfig
from .analysis import analyze_rows
from .llm import llm_generate_insights

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


def node_read_data(state: AgentState) -> Command[AgentState]:
    logger.info("Node 1: Reading data from Google Sheets...")
    try:
        config = SheetsConfig(
            spreadsheet_id=state.get("spreadsheet_id"),
            read_range=state.get("read_range"),
            write_range=state.get("write_range"),
            service_account_json=state.get("service_account_json", "crediantials/service_account.json")
        )
        raw_data = read_sheet(config)
        logger.info(f"Successfully read {len(raw_data)} rows from sheet")
        
        return Command(update={"raw_data": raw_data})
    except Exception as e:
        logger.error(f"Failed to read data: {str(e)}")
        return Command(update={"error": f"Data reading failed: {str(e)}"})


def node_analyze_data(state: AgentState) -> Command[AgentState]:
    logger.info("Node 2: Analyzing data...")
    try:
        raw_data = state.get("raw_data", [])
        if not raw_data:
            return Command(update={"error": "No data to analyze"})
        
        analysis = analyze_rows(raw_data)
        
        if "error" in analysis:
            return Command(update={"error": analysis["error"]})
        
        logger.info("Data analysis completed")
        return Command(update={"analysis": analysis})
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return Command(update={"error": f"Analysis failed: {str(e)}"})


def node_generate_insights(state: AgentState) -> Command[AgentState]:
    logger.info("Node 3: Generating insights with LLM...")
    try:
        analysis = state.get("analysis", {})
        model = state.get("model", "qwen2.5:0.5b")
        base_url = state.get("base_url")
        context = state.get("context", "")
        
        if "error" in analysis:
            return Command(update={"error": f"Cannot generate insights: {analysis['error']}"})
        
        insights = llm_generate_insights(
            analysis=analysis,
            model=model,
            base_url=base_url
        )
        
        logger.info("Insights generated successfully")
        return Command(update={"insights": str(insights)})
    except Exception as e:
        logger.error(f"Insights generation failed: {str(e)}")
        return Command(update={"error": f"Insights generation failed: {str(e)}"})


def node_validate_output(state: AgentState) -> Command[AgentState]:
    logger.info("Node 4: Validating output...")
    try:
        error = state.get("error")
        if error:
            logger.warning(f"Workflow completed with error: {error}")
            return Command(goto=END)
        
        insights = state.get("insights", "")
        if not insights:
            logger.warning("No insights generated")
            return Command(update={"error": "No insights generated"}, goto=END)
        
        logger.info("Output validation passed")
        return Command(goto=END)
    except Exception as e:
        logger.error(f"Validation failed: {str(e)}")
        return Command(update={"error": f"Validation failed: {str(e)}"}, goto=END)


def create_agent_graph():
    logger.info("Building agentic workflow graph...")
    
    graph = StateGraph(AgentState)
    
    graph.add_node("read_data", node_read_data)
    graph.add_node("analyze_data", node_analyze_data)
    graph.add_node("generate_insights", node_generate_insights)
    graph.add_node("validate_output", node_validate_output)
    
    graph.add_edge(START, "read_data")
    graph.add_edge("read_data", "analyze_data")
    graph.add_edge("analyze_data", "generate_insights")
    graph.add_edge("generate_insights", "validate_output")
    
    compiled_graph = graph.compile()
    logger.info("Graph compiled successfully")
    
    return compiled_graph
