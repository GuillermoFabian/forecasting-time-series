"""Script for evaluating model performance

"""

# import necessary libraries
import traceback
import logging
from logging.handlers import TimedRotatingFileHandler
import mlflow
from datetime import datetime

from DataProcessor import DataProcessor
from utils.compute_metrics import compute_wmae, compute_wmape, compute_eval_data_ratio
from utils.extract_config import configfile


# get configurations
configfile = configfile()
log_path = configfile.get('logging', 'log_path')
mlflow_tracking_uri = configfile.get('optimization', 'mlflow_tracking_uri')
mlflow_eval_experiment_name = configfile.get('optimization', 'mlflow_eval_experiment_name')

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
    # read in evaluation data
    dataprocessor = DataProcessor()
    evaluation_df, training_df = dataprocessor.get_data_for_eval()
    logger.info("Evaluation: data for evaluation obtained")

    # set MLflow path to log data
    mlflow.set_tracking_uri(mlflow_tracking_uri)

    # set experiment name to organize runs
    mlflow.set_experiment(mlflow_eval_experiment_name)
    experiment = mlflow.get_experiment_by_name(mlflow_eval_experiment_name)

    with mlflow.start_run(experiment_id = experiment.experiment_id):
        # log date as param so as to visualize metrics by date
        

        # compute model metrics
       

        # compute data metrics
        

        # log metrics
        

except Exception:
    logger.error(traceback.format_exc())