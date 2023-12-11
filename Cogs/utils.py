import os
import requests
import json


# Jar downloads

class Paper:
    """Class for interacting with Paper API and downloading Paper builds."""

    def get_paper_versions(self):
        try:
            response = requests.get("https://api.papermc.io/v2/projects/paper/")
            response.raise_for_status()
            data = response.json()
            if 'versions' in data and data['versions']:
                vers = data['versions']
                print(vers)
                return vers
        except requests.RequestException as e:
            print(f"Error fetching Paper build: {e}")
        return None

    def __init__(self, server_name: str = None, version: str = None, download_path: str = None):
        """Initialize Paper instance.

            Args:
                version (str): Paper version.
                download_path (str): Path to save the downloaded Paper JAR.
        """
        self.server_name = server_name
        self.latest_build = None
        self.version = version
        self.download_path = f"{download_path}\\{self.server_name}"
        self.paper_api_url = f"https://api.papermc.io/v2/projects/paper/versions/"

    def get_latest_build(self):

        """Retrieve the download URL for the latest Paper build.

            Returns:
                str: Download URL if successful, None otherwise.
        """
        try:
            response = requests.get(self.paper_api_url + f'{self.version}/builds')
            response.raise_for_status()  # Raise HTTPError for bad responses
            data = response.json()
            if 'builds' in data and data['builds']:
                self.latest_build = data['builds'][1]['build']
                paper_download_url = f"{self.paper_api_url}{self.version}/builds/{self.latest_build}/downloads/paper-{self.version}-{self.latest_build}.jar"
                return paper_download_url
        except requests.RequestException as e:
            print(f"Error fetching Paper build: {e}")
        return None

    def download_paper(self):
        """Download the latest Paper build.

            Returns:
                bool: True if successful, False otherwise.
        """
        paper_download_url = self.get_latest_build()
        jar_file = f"paper-{self.version}-{self.latest_build}.jar"

        if paper_download_url:
            download_file(paper_download_url, self.download_path, jar_file, self.server_name)
            return True
        return False


class Vanilla:
    def __init__(self, server_name: str = None, version: str = None, download_path: str = None):
        self.version = version
        self.server_name = server_name
        self.download_path = download_path
        self.vanilla_api_url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

    def get_version_info(self, version_id):
        try:
            response = requests.get(self.vanilla_api_url)
            response.raise_for_status()
            data = response.json()

            for entry in data['versions']:
                if version_id == entry['id']:
                    return entry['url']

            # If version_id is not found
            print(f"Version {version_id} not found.")
            return None

        except requests.RequestException as e:
            print(f"Error fetching version information for {version_id}: {e}")
            return None

    def get_version_group(self, group_name):
        try:
            response = requests.get(self.vanilla_api_url)
            response.raise_for_status()
            data = response.json()
            group_versions = [entry['id'] for entry in data['versions'] if
                              group_name and group_name.lower() in entry.get('type', '').lower()]
            return group_versions
        except requests.RequestException as e:
            print(f"Error fetching version group {group_name}: {e}")
            return None

    def get_version_url(self, version_id):
        version_info = self.get_version_info(version_id)
        if version_info:
            return version_info
        return None

    def download_server(self):
        try:
            version_url = self.get_version_url(self.version)
            if version_url:
                response = requests.get(version_url, allow_redirects=True)
                response.raise_for_status()

                data = response.json()
                server_url = data['downloads']['server']['url']
                jar_file = f"vanilla-{self.version}.jar"

                download_file(server_url, self.download_path, jar_file, self.server_name)

        except requests.RequestException as e:
            print(f"Error fetching server download URL: {e}")

        return None


class Spigot:
    def __init__(self):
        self.buildtools_download = ("https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact"
                                    "/target/BuildTools.jar")


def download_file(url, save_path, jar_file, server_name):
    s_path = f"{save_path}\\{server_name}"
    save_path = os.path.abspath(s_path)
    d_path = os.path.join(save_path, jar_file)
    os.makedirs(os.path.dirname(d_path), exist_ok=True)
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_path = save_path
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            return True
    except requests.RequestException as e:
        print(f"Error downloading file: {e}")

    return False
