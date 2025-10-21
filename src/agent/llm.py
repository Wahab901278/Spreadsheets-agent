from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

def get_ollama(model,temperature=0.2,base_url=None):
    model_name=model
    url=base_url
    return ChatOllama(model=model_name,temperature=temperature,base_url=url)


def craft_prompt(analysis, context):
    sys = (
        "You are a data analyst. Given the summary statistics, "
        "write 3-6 concise, actionable insights for a business audience."
    )
    summary_of_numericals = analysis.get('summary_of_numerical_columns', {})
    summary_of_categoricals = analysis.get('summary_of_categorical_columns', {})

    lines = []
    if summary_of_numericals and 'summary' in summary_of_numericals:
        lines.append("Preliminary insights of numerical columns:\n" + "\n- ".join(str(row) for row in str(summary_of_numericals['summary']).split('\n')))
    
    if summary_of_categoricals and 'summary' in summary_of_categoricals:
        lines.append("Preliminary insights of categorical columns:\n" + "\n- ".join(str(row) for row in str(summary_of_categoricals['summary']).split('\n')))
        
    if context:
        lines.append(f"Context: {context}")

    user_content = (
        "Using the information above, generate a short narrative with bullet points focusing on trends, "
        "anomalies, and recommendations. Keep it under 120 words"
    )

    combined_content = "\n\n".join(lines) + "\n\n" + user_content

    return [SystemMessage(content=sys), HumanMessage(content=combined_content)]

def llm_generate_insights(analysis, model, base_url, context=""):
    try:
        llm = get_ollama(model=model, base_url=base_url)
        msgs = craft_prompt(analysis, context)
        resp = llm.invoke(msgs)

        return resp.content if hasattr(resp, 'content') else str(resp)
    except Exception as e:
        return f"LLM Unavailable or failed to load: {str(e)}"