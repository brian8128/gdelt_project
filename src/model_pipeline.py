from CONSTANTS import MODEL_PICKLE_PATH
from pickle_helper import pickle_, unpickle_


def pickle_model(model):
    """
    Convenience function for calling pickle
    """
    return pickle_(model, MODEL_PICKLE_PATH)


def unpickle_model():
    """
    Convenience function for unpickling
    """
    return unpickle_(MODEL_PICKLE_PATH)