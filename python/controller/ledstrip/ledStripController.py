from base.controller import GeneralController
from controller.ledstrip.modes.stack import StackMode
from controller.ledstrip.modes.scanner import ScannerMode
from controller.ledstrip.modes.visualization.chunk import ChunkMode
from controller.ledstrip.modes.visualization.energy import EnergyVisualizerMode
from controller.ledstrip.modes.visualization.scroll import ScrollVisualizerMode
from controller.ledstrip.modes.visualization.spectrum import SpectrumVisualizerMode


class LEDStripController(GeneralController):
    def __init__(self, deviceId: str, gui=False, additionalModes=None):
        modes = {
            "stack": StackMode,
            "scanner": ScannerMode,
            "chunk": ChunkMode,
            "energy": EnergyVisualizerMode,
            "scroll": ScrollVisualizerMode,
            "spectrum": SpectrumVisualizerMode
        }

        defaultConfig = {
            "stack_concurrent": 6,
            "stack_speed": 1,
            "scanner_size": 1,
            "scanner_shadow": 10
        }

        if additionalModes is None:
            additionalModes = {}

        super().__init__(deviceId, {**additionalModes, **modes}, filters={}, configDefaults=defaultConfig, gui=gui)