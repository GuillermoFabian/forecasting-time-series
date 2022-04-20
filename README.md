# Forecasting daily sales 

Running app in /src:

    uvicorn api:app --reload

Predict example: 

    http://127.0.0.1:8000/predictions/?start=2016-04-25



##### Retrieve predictions data from database based on query parameters
    Parameters:

    start (datetime.date): Starting date to query from. Optional.
    end (datetime.date): Ending date to query to. Optional.
    category (str): Category to filter. Optional.
    store (str): Store to filter. Optional.

    Returns:

    parsed (JSON): Predictions data and relevant schema 
    