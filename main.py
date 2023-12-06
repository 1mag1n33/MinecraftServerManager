import subprocess
import time

from Cogs.utils import Paper


def run_script(script_name):
    subprocess.Popen(['start', 'cmd', '/k', 'python', script_name], shell=True)


if __name__ == "__main__":
    paper = Paper("1.20.2", "./test")
    paper.download_paper()

    run_script('./Cogs/Website/site.py')

    time.sleep(5)

    run_script("./Cogs/SocketServer/Server.py")
