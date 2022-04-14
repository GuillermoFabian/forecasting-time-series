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

    # logic to read relevant predictions data based on query parameters
    


    # convert dataframe to JSON to serve data
    

    logger.info(f"time taken: {time.time()-start_time}")

    return parsed


if __name__=='__main__':
    # start API
    uvicorn.run("api:app", host="127.0.0.1", port=8000, log_level="info")