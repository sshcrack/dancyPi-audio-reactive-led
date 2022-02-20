from setuptools import setup, find_packages


setup(
    name="RPI Music Visualizer",
    version="2.0",
    author="Nazmus Nasir/sshcrack",
    author_email="lesslie.bauer777@gmail.com",
    url="https://sshcrack.me",
    download_url="https://github.com/sshcrack/rpi-music-visualizer",
    description="Audio Reactive Raspberry Pi with WS2812b LEDs.",
    license="MIT",
    install_requires=['numpy', 'pyaudio', 'pyqtgraph', 'scipy==1.4.1', 'rpi_ws281x']
)
