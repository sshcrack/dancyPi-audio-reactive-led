import numpy as np

from base.GeneralPostProcess import GeneralPostProcess


class GeneralFilter(GeneralPostProcess):
    def run(self, data: np.ndarray):
        raise NotImplementedError
