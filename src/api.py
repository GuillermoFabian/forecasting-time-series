"""Script to setup REST API to serve predictions

"""

# import necessary libraries
import datetime
import json
import time
import logging
import uvicorn
from fastapi import FastAPI
from typing import Optional

from DataProcessor import DataProcessor
from utils.extract_config import configfile

# set logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

# get configurations
configfile = configfile()
db_url = configfile.get('database', 'database_url')

# create a FastAPI instance
description = "This API returns the forecasted sales predictions"
app = FastAPI(title="Forecasting Predictions", description=description)

@app.get("/predictions/")  # create predictions path with GET operation
def get_predictions(start: Optional[datetime.date] = None, end: Optional[datetime.date] = None, 
                    category: Optional[str] = None, store: Optional[str] = None):
    """
    Retrieve predictions data from database based on query parameters

    Parameters:
    start (datetime.date): Starting date to query from. Optional.
    end (datetime.date): Ending date to query to. Optional.
    category (str): Category to filter. Optional.
    store (str): Store to filter. Optional.

    Returns:
    parsed (JSON): Predictions data and relevant schema 
    """

    start_time = time.time()
    dataprocessor = DataProcessor()

    distinct_on_query_part = "distinct on (store_id, cat_id, date)"
    order_by_query_part = "order by store_id, cat_id, date, creation_time desc"


    if start is None and end is not None:
        predictions_df = dataprocessor.read_from_db(
            f"select {distinct_on_query_part} * from prediction where date <= '{end}' {order_by_query_part}",
            parse_dates=['date', 'creation_time'])
    elif start is not None and end is None:
        predictions_df = dataprocessor.read_from_db(
            f"select {distinct_on_query_part} * from prediction where date >= '{start}' {order_by_query_part}",
            parse_dates=['date', 'creation_time'])
    elif start is not None and end is not None:
        predictions_df = dataprocessor.read_from_db(
            f"select {distinct_on_query_part} * from prediction where date between '{start}' and '{end}' {order_by_query_part}",
            parse_dates=['date', 'creation_time'])
    else:
        predictions_df = dataprocessor.read_from_db(
            f"select {distinct_on_query_part} * from prediction {order_by_query_part} limit 100",
            parse_dates=['date', 'creation_time'])

    if category is not None:
        predictions_df = predictions_df.loc[predictions_df.cat_id == category]

    if store is not None:
        predictions_df = predictions_df.loc[predictions_df.store_id == store]

    result = predictions_df.to_json(orient="table", index=False)
    parsed = json.loads(result)
    

    logger.info(f"time taken: {time.time()-start_time}")

    return parsed


if __name__=='__main__':
    # start API
    uvicorn.run("api:app", host="127.0.0.1", port=8000, log_level="info")