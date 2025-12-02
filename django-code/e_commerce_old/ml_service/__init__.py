from .main import ModelServing

SENTIMENT_PREDICTOR_INSTANCE = ModelServing() 

def get_predictor_instance():
    return SENTIMENT_PREDICTOR_INSTANCE