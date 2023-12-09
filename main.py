import subprocess
import time

from Cogs.utils import Paper, Vanilla


def run_script(script_name):
    subprocess.Popen(['start', 'cmd', '/k', 'python', script_name], shell=True)


if __name__ == "__main__":
    vanilla_instance = Vanilla()
    stable_versions = vanilla_instance.get_stable_versions()
    snapshot_versions = vanilla_instance.get_snapshot_versions()
    beta_versions = vanilla_instance.get_beta_versions()
    alpha_versions = vanilla_instance.get_alpha_versions()
    version_id = "1.17.1"
    version_url = vanilla_instance.download_server(version_id)

    print("Stable Versions:", stable_versions)
    print("Snapshot Versions:", snapshot_versions)
    print("Beta Versions:", beta_versions)
    print("Alpha Versions:", alpha_versions)
    print("Server Url:", version_url)

    #run_script('./Cogs/Website/site.py')

    #time.sleep(5)

    #run_script("./Cogs/SocketServer/Server.py")
