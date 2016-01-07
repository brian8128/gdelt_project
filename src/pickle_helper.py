import cPickle as pickle
from CONSTANTS import PROJECT_HOME


def pickle_(obj, path):
    """
    Deletes the current pickled ticker price df if one exists and writes the given
    df to the file.
    """
    filename = PROJECT_HOME + path

    with open(filename, 'w') as f:
        pickle.dump(obj, f)

    return


def unpickle_(path):
    """
    Loads the the pickled ticker price df
    :return:
    """
    filename = PROJECT_HOME + path

    with open(filename, 'r') as f:
        return pickle.load(f)
