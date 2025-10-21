import pandas as pd
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

def analyze_rows(rows: List[List[Any]]):
    if not rows:
        return {
            "error":"No Data"
        }
    header=rows[0]
    data=rows[1:]
    if not data:
        return {
            "error":"no rows after header"
        }
    df=pd.DataFrame(data,columns=header)

    logger.info("Summary of the numerical columns")
    summary_of_numerical_columns={}
    summary_of_numerical_columns['summary']=df.describe()
    logger.info("Summary of categorical columns")
    summary_of_categorical_columns={}

    summary_of_categorical_columns['summary']=df.describe(include='object')

    summary={"summary_of_numerical_columns":summary_of_numerical_columns,
             "summary_of_categorical_columns":summary_of_categorical_columns}

    return summary
