import numpy as np


def vectorize_method(method):
    """"
      A decorator for creating a vectorized method inside a class
    """

    def vectorized_method(self, *args, **kwargs):
        return np.vectorize(method)(self, *args, **kwargs)
    return vectorized_method
