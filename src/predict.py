"""Script for making predictions

"""

# import necessary libraries
import traceback
import logging
from logging.handlers import TimedRotatingFileHandler

from DataProcessor import DataProcessor
from Model import NBeatsModel
from utils.extract_config import configfile


# get configurations
configfile = configfile()
log_path = configfile.get('logging', 'log_path')

# set logging
logFormatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

fileHandler = TimedRotatingFileHandler(log_path, when='midnight', backupCount=90)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

logger.setLevel(logging.INFO)
logger.propagate = False


try:
    try:
        # read in data for making prediction
        dataprocessor = DataProcessor()
        df_for_prediction = dataprocessor.get_data_for_prediction()
        logger.info("Prediction: data for prediction obtained")

        # pass data to model
        model = NBeatsModel()
        predictions_df = model.predict(df_for_prediction)
        logger.info("Prediction: predictions made")

        # write predictions to db
        dataprocessor.write_to_db(predictions_df, 'prediction')
        logger.info("Prediction: predictions written to database")

    except Exception:
        logger.error(traceback.format_exc())




except Exception:
    logger.error(traceback.format_exc())
