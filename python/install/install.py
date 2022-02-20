# install.py
# Version: 1.0.0
# Installs dependences needed for Dancy Pi
# Author: Nazmus Nasir (modified by sshcrack)
# Website: https://www.easyprogramming.net / https://sshcrack.me
import sys
sys.path.append('..')

import os
from os import path
from tools.tools import check_int
from json import dumps
from shutil import copy2

add_service = False

def setup_service():
    global add_service
    if not add_service:
        return

    print("================== Adding service ======================")
    f = open("rpimusicvisualizer.service","r")
    content = f.read()
    f.close()

    run_path = path.abspath(path.join(path.dirname(__file__), "..", "run.sh"))
    run_dir = path.dirname(run_path)

    content = content.replace("WORK_DIR", run_dir)
    content = content.replace("RUN_SCRIPT", run_path)

    with open("/etc/systemd/system/rpimusicvisualizer.service", "w") as f:
        f.write(content)

    print("================== Completed adding service ============")
    print("================== Start enabling service ==============")
    os.system("systemctl enable rpimusicvisualizer.service")
    os.system("systemctl start rpimusicvisualizer")
    print("================== Completed enabling service ==========")
def setup_config():
    global add_servicdäe
    print("================== Setting up config ====================")
    led_pin = number_input("To which pin is your led strip connected? (default 18)", default=18, optional=True)
    led_invert = boolean_input("Do you have a inverting logic level converter installed? (Default False, if you dont know what it is just enter no)")
    n_pixels = number_input("How many leds does your led strip have?")
    status_led_pin = number_input("Where is your status led installed (enter if you dont have one)", True)
    gesture_sensor_enabled = boolean_input("Do you have a grove gesture sensor installed?")
    add_service = boolean_input("Do you want to start the visualizer at startup?")

    mappings = {
        "LED_PIN": led_pin,
        "LED_INVERT": led_invert,
        "N_PIXELS": n_pixels,
        "STATUS_LED_PIN": status_led_pin,
        "GESTURE_SENSOR_ENABLED": gesture_sensor_enabled
    }
    mapping_keys = list(mappings.keys())

    config_file = open("../config.py", "r")
    config = config_file.read()

    config_file.close()
    config = config.split("\n")

    for i in range(len(config)):
        entry = config[i]
        entry_var = entry.replace(" ", "").split("=")[0]

        if "=" not in entry or entry_var not in mapping_keys:
            continue

        entry = entry.split("=")
        entry[-1] = dumps(mappings[entry_var])
        entry = "=".join(entry)

        config[i] = entry

    config_result = "\n".join(config)
    print("================== Completed user prompts ================")
    print("================== Saving config =========================")
    with open("../config.py", "w") as f:
        f.write(config_result)

    print("================== Config saved ==========================")

def boolean_input(question: str):
    out = None
    while out == None:
        print(question + " (yes/no)")
        out_str = input(" >> ").lower()

        if out_str in [ "y", "yes"]:
            out = True
        elif out_str in [ "n", "no"]:
            out = False
        else:
            print("Invalid input can either be yes or no")
    return out

def number_input(question: str, optional = False, default=None):
    out = default
    while True:
        print(question)
        out_str = input(" >> ")
        if optional and len(out_str.replace(" ", "")) == 0:
            break

        if check_int(out_str):
            out = int(out_str)
            break
        else:
            print("Input has to be a number and can not have decimal points")
    return out

def install_dependencies():
    print("================== Start Installing PIP ==================")
    os.system("sudo apt install python3-pip -y")
    print("================== Completed Installing PIP ==================")

    print("================== Start Updating PIP ==================")
    os.system("sudo pip3 install --upgrade pip")
    print("================== Completed Updating PIP ==================")

    print("================== Start Installing Setuptools and Libatlas ==================")
    os.system("sudo apt install python-setuptools libatlas-base-dev -y")
    print("================== Completed Installing Setuptools and Libatlas ==================")

    print("================== Start Installing Fortran ==================")
    os.system("sudo apt install libatlas3-base libgfortran5 -y")
    print("================== Completed Installing Fortran ==================")

    print("================== Start Installing Numpy, Scipy, PyAudio, PyQtgraph ==================")
    os.system("sudo apt install python-numpy python-scipy python-pyaudio python-pyqtgraph -y")
    os.system("sudo pip3 install numpy scipy==1.4.1 pyaudio pyqtgraph")
    print("================== Completed Installing Numpy, Scipy, PyAudio, PyQtgraph ==================")

    print("================== Start Installing rpi_ws281x ==================")
    os.system("sudo pip3 install rpi_ws281x")
    print("================== Completed Installing rpi_ws281x ==================")


def replace_asound():
    print("================== Copying asound.conf ==================")
    copy2('asound.conf', '/etc/asound.conf')
    print("================== Completed copying to /etc/asound.conf ==================")


def edit_alsa_conf():
    print("================== Creating backup of alsa.conf ==================")
    copy2('/usr/share/alsa/alsa.conf', '/usr/share/alsa/alsa.conf.bak')
    print("================== Completed backup of alsa.conf -> alsa.conf.bak ==================")

    print("================== Replacing text in alsa.conf ==================")
    with open('/usr/share/alsa/alsa.conf', 'r') as file:
        filedata = file.read()
        filedata = filedata.replace("defaults.ctl.card 0", "defaults.ctl.card 1")
        filedata = filedata.replace("defaults.pcm.card 0", "defaults.pcm.card 1")
        filedata = filedata.replace("pcm.front cards.pcm.front", "# pcm.front cards.pcm.front")
        filedata = filedata.replace("pcm.rear cards.pcm.rear", "# pcm.rear cards.pcm.rear")
        filedata = filedata.replace("pcm.center_lfe cards.pcm.center_lfe", "# pcm.center_lfe cards.pcm.center_lfe")
        filedata = filedata.replace("pcm.side cards.pcm.side", "# pcm.side cards.pcm.side")
        filedata = filedata.replace("pcm.surround21 cards.pcm.surround21", "# pcm.surround21 cards.pcm.surround21")
        filedata = filedata.replace("pcm.surround40 cards.pcm.surround40", "# pcm.surround40 cards.pcm.surround40")
        filedata = filedata.replace("pcm.surround41 cards.pcm.surround41", "# pcm.surround41 cards.pcm.surround41")
        filedata = filedata.replace("pcm.surround50 cards.pcm.surround50", "# pcm.surround50 cards.pcm.surround50")
        filedata = filedata.replace("pcm.surround51 cards.pcm.surround51", "# pcm.surround51 cards.pcm.surround51")
        filedata = filedata.replace("pcm.surround71 cards.pcm.surround71", "# pcm.surround71 cards.pcm.surround71")
        filedata = filedata.replace("pcm.iec958 cards.pcm.iec958", "# pcm.iec958 cards.pcm.iec958")
        filedata = filedata.replace("pcm.spdif iec958", "# pcm.spdif iec958")
        filedata = filedata.replace("pcm.hdmi cards.pcm.hdmi", "# pcm.hdmi cards.pcm.hdmi")
        filedata = filedata.replace("pcm.modem cards.pcm.modem", "# pcm.modem cards.pcm.modem")
        filedata = filedata.replace("pcm.phoneline cards.pcm.phoneline", "# pcm.phoneline cards.pcm.phoneline")
    with open('/usr/share/alsa/alsa.conf', 'w') as file:
        file.write(filedata)

    print("================== Completed replacing text in alsa.conf ==================")


setup_config()
install_dependencies()
replace_asound()
edit_alsa_conf()
setup_service()
