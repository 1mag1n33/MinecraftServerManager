import subprocess
import time

from Cogs.Utils.server_utils import Spigot


def run_script(script_name):
    subprocess.Popen(['start', 'cmd', '/k', 'python', script_name], shell=True)


if __name__ == "__main__":

    run_script('./Cogs/Website/site.py')

    time.sleep(5)

    run_script("./Cogs/SocketServer/Server.py")
