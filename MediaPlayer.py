import subprocess
import tkinter.filedialog
import platform


def main():
    filepath = tkinter.filedialog.askopenfilename()
    media_process = subprocess.Popen(["vlc", filepath], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    media_process.communicate()
