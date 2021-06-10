import subprocess
import platform

# default file explorer on Raspberry Pi 3 is pcmanfm, change the name if the user wants to use another file explorer


def main():
    default_folder = "/home/pi/Desktop"
    p = subprocess.Popen(["pcmanfm", default_folder], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.communicate()
