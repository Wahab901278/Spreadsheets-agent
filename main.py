import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agent.graph import create_agent_graph, AgentState

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    
    logger.info("=" * 80)
    logger.info("STARTING SPREADSHEET ANALYSIS AGENT")
    logger.info("=" * 80)
    
    config = {
        "spreadsheet_id": os.getenv("SPREADSHEET_ID", "your_spreadsheet_id"),
        "read_range": os.getenv("READ_RANGE", "Sheet1!A1:Z1000"),
        "write_range": os.getenv("WRITE_RANGE", "Sheet1!AB1"),
        "service_account_json": os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "crediantials/service_account.json"),
        "model": os.getenv("LLM_MODEL", "llama2"),
        "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        "context": os.getenv("ANALYSIS_CONTEXT", ""),
        "raw_data": [],
        "analysis": {},
        "insights": "",
        "error": ""
    }
    
    try:
        logger.info("\nCreating LangGraph workflow...")
        agent_graph = create_agent_graph()
        
        initial_state: AgentState = config
        
        logger.info("\nInvoking workflow with the following config:")
        logger.info(f"  - Spreadsheet ID: {config['spreadsheet_id']}")
        logger.info(f"  - Read Range: {config['read_range']}")
        logger.info(f"  - LLM Model: {config['model']}")
        logger.info(f"  - Ollama Base URL: {config['base_url']}")
        logger.info("\n" + "=" * 80)
        
        final_state = agent_graph.invoke(initial_state)
        
        logger.info("=" * 80)
        logger.info("\nWORKFLOW EXECUTION COMPLETED\n")
        
        if final_state.get("error"):
            logger.warning(f"Workflow completed with error: {final_state['error']}")
        else:
            logger.info("Workflow completed successfully!\n")
            logger.info("INSIGHTS GENERATED:")
            logger.info("-" * 80)
            insights = final_state.get("insights", "No insights generated")
            logger.info(insights)
            logger.info("-" * 80)
        
        logger.info("\nFINAL STATE:")
        logger.info(f"  - Data rows read: {len(final_state.get('raw_data', []))}")
        logger.info(f"  - Analysis completed: {'Yes' if final_state.get('analysis') else 'No'}")
        logger.info(f"  - Insights generated: {'Yes' if final_state.get('insights') else 'No'}")
        
        if final_state.get("error"):
            logger.error(f"\nError: {final_state['error']}")
            return 1
        
        logger.info("\n" + "=" * 80)
        logger.info("Agent execution completed successfully!")
        logger.info("=" * 80)
        return 0
        
    except Exception as e:
        logger.error(f"\nCritical error occurred: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
