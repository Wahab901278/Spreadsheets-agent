import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from threading import Thread
import uuid

load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agent.graph import create_agent_graph, AgentState

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Store job results (in production, use Redis or a database)
job_results = {}


def run_analysis_job(job_id, config):
    """Run the analysis in a background thread"""
    try:
        logger.info(f"Starting analysis job {job_id}")
        job_results[job_id] = {"status": "running", "progress": "Initializing..."}
        
        # Create the agent graph
        agent_graph = create_agent_graph()
        
        # Update progress
        job_results[job_id]["progress"] = "Running analysis..."
        
        # Run the analysis
        final_state = agent_graph.invoke(config)
        
        # Store results
        if final_state.get("error"):
            job_results[job_id] = {
                "status": "error",
                "error": final_state["error"]
            }
        else:
            job_results[job_id] = {
                "status": "completed",
                "data": {
                    "rows_read": len(final_state.get('raw_data', [])),
                    "analysis": final_state.get('analysis', {}),
                    "insights": final_state.get('insights', ''),
                    "spreadsheet_id": final_state.get('spreadsheet_id'),
                    "write_range": final_state.get('write_range')
                }
            }
        
        logger.info(f"Analysis job {job_id} completed")
        
    except Exception as e:
        logger.error(f"Error in job {job_id}: {str(e)}", exc_info=True)
        job_results[job_id] = {
            "status": "error",
            "error": str(e)
        }


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Spreadsheet Analysis Agent API"
    }), 200


@app.route('/analyze', methods=['POST'])
def analyze_spreadsheet():
    """
    Start a spreadsheet analysis job
    
    Request body:
    {
        "spreadsheet_id": "your_spreadsheet_id",
        "read_range": "Sheet1!A1:Z1000",
        "write_range": "Sheet1!AB1",
        "service_account_json": "credentials/service_account.json",
        "model": "llama2",
        "base_url": "http://localhost:11434",
        "context": "Optional analysis context"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        # Build config with defaults
        config = {
            "spreadsheet_id": data.get("spreadsheet_id", os.getenv("SPREADSHEET_ID", "")),
            "read_range": data.get("read_range", os.getenv("READ_RANGE", "Sheet1!A1:Z1000")),
            "write_range": data.get("write_range", os.getenv("WRITE_RANGE", "Sheet1!AB1")),
            "service_account_json": data.get("service_account_json", os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "credentials/service_account.json")),
            "model": data.get("model", os.getenv("LLM_MODEL", "llama2")),
            "base_url": data.get("base_url", os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")),
            "context": data.get("context", os.getenv("ANALYSIS_CONTEXT", "")),
            "raw_data": [],
            "analysis": {},
            "insights": "",
            "error": ""
        }
        
        # Validate spreadsheet_id
        if not config["spreadsheet_id"]:
            return jsonify({"error": "spreadsheet_id is required"}), 400
        
        # Generate job ID
        job_id = str(uuid.uuid4())
        
        # Start analysis in background thread
        thread = Thread(target=run_analysis_job, args=(job_id, config))
        thread.daemon = True
        thread.start()
        
        logger.info(f"Created analysis job {job_id} for spreadsheet {config['spreadsheet_id']}")
        
        return jsonify({
            "job_id": job_id,
            "status": "started",
            "message": "Analysis job started successfully",
            "config": {
                "spreadsheet_id": config["spreadsheet_id"],
                "read_range": config["read_range"],
                "model": config["model"]
            }
        }), 202
        
    except Exception as e:
        logger.error(f"Error starting analysis: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route('/status/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get the status of an analysis job"""
    if job_id not in job_results:
        return jsonify({"error": "Job not found"}), 404
    
    result = job_results[job_id]
    
    if result["status"] == "running":
        return jsonify({
            "job_id": job_id,
            "status": "running",
            "progress": result.get("progress", "Processing...")
        }), 200
    
    elif result["status"] == "completed":
        return jsonify({
            "job_id": job_id,
            "status": "completed",
            "data": result["data"]
        }), 200
    
    elif result["status"] == "error":
        return jsonify({
            "job_id": job_id,
            "status": "error",
            "error": result["error"]
        }), 200


@app.route('/jobs', methods=['GET'])
def list_jobs():
    """List all jobs and their status"""
    jobs = []
    for job_id, result in job_results.items():
        jobs.append({
            "job_id": job_id,
            "status": result["status"]
        })
    
    return jsonify({
        "total_jobs": len(jobs),
        "jobs": jobs
    }), 200


@app.route('/analyze/sync', methods=['POST'])
def analyze_spreadsheet_sync():
    """
    Run a synchronous spreadsheet analysis (blocks until complete)
    Use this for smaller datasets or when you need immediate results
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        config = {
            "spreadsheet_id": data.get("spreadsheet_id", os.getenv("SPREADSHEET_ID", "")),
            "read_range": data.get("read_range", os.getenv("READ_RANGE", "Sheet1!A1:Z1000")),
            "write_range": data.get("write_range", os.getenv("WRITE_RANGE", "Sheet1!AB1")),
            "service_account_json": data.get("service_account_json", os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "credentials/service_account.json")),
            "model": data.get("model", os.getenv("LLM_MODEL", "llama2")),
            "base_url": data.get("base_url", os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")),
            "context": data.get("context", os.getenv("ANALYSIS_CONTEXT", "")),
            "raw_data": [],
            "analysis": {},
            "insights": "",
            "error": ""
        }
        
        if not config["spreadsheet_id"]:
            return jsonify({"error": "spreadsheet_id is required"}), 400
        
        logger.info(f"Starting synchronous analysis for spreadsheet {config['spreadsheet_id']}")
        
        # Create and run the agent graph
        agent_graph = create_agent_graph()
        final_state = agent_graph.invoke(config)
        
        if final_state.get("error"):
            return jsonify({
                "status": "error",
                "error": final_state["error"]
            }), 500
        
        return jsonify({
            "status": "completed",
            "data": {
                "rows_read": len(final_state.get('raw_data', [])),
                "analysis": final_state.get('analysis', {}),
                "insights": final_state.get('insights', ''),
                "spreadsheet_id": final_state.get('spreadsheet_id'),
                "write_range": final_state.get('write_range')
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in synchronous analysis: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info("=" * 80)
    logger.info("SPREADSHEET ANALYSIS AGENT API")
    logger.info("=" * 80)
    logger.info(f"Starting Flask server on port {port}")
    logger.info(f"Debug mode: {debug}")
    logger.info("=" * 80)
    
    app.run(host='0.0.0.0', port=port, debug=debug)