from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

def get_ollama(model,temperature=0.2,base_url=None):
    model_name=model
    url=base_url
    return ChatOllama(model=model_name,temperature=temperature,base_url=url)


def craft_prompt(analysis,context):
    sys=(
        "You are a data analyst. Given the summary statistics."
        "write 3-6 concise, actionable insights for a business audience." \
        
    )
    summary_of_numericals=analysis['summary_of_numerical_columns']
    summary_of_categoricals=analysis['summary_of_categorical_columns']

    lines=[]
    if summary_of_numericals:
        lines.append("Preliminary insights of numerical columns: \n" + "\n- ".join(str(row)) for row in summary_of_numericals['summary'])
    

    if summary_of_categoricals:
        lines.append("Preliminary insights of categorical columns: \n" + "\n- ".join(str(row)) for row in summary_of_categoricals['summary'])
        
    if context:
        lines.append(f"Context: {context}")

    user=(
        "Using the information above, generate a short narrative with bullet points focusing on trends,"
        "anomalies, and recommendations. Keep it under 120 words"
    )

    return [SystemMessage,HumanMessage]

def llm_generate_insights(analysis,model,base_url):
   try:
       llm=get_ollama(model=model,base_url=base_url)
       msgs=craft_prompt(analysis)
       resp=llm.invoke(msgs)

       return resp
   except Exception as e:
       return f"LLM Unavailable or failed to load"