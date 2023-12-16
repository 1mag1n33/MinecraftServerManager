from .utils import *
from bs4 import BeautifulSoup
from distutils.version import LooseVersion

import requests
import os


# Jar downloads

class Paper:
    """Class for interacting with Paper API and downloading Paper builds."""

    def __init__(self, server_name: str = None, version: str = None, download_path: str = None):
        """Initialize Paper instance.

            Args:
                server_name (str): Server name.
                version (str): Paper version.
                download_path (str): Path to save the downloaded Paper JAR.
        """
        self.server_name = server_name
        self.latest_build = None
        self.version = version
        self.download_path = download_path
        self.paper_api_url = f"https://api.papermc.io/v2/projects/paper/versions/"

    @staticmethod
    def get_paper_versions():
        try:
            response = requests.get("https://api.papermc.io/v2/projects/paper/")
            response.raise_for_status()
            data = response.json()
            if 'versions' in data and data['versions']:
                vers = data['versions']
                return vers
        except requests.RequestException as e:
            print(f"Error fetching Paper build: {e}")
        return None

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
    """Class for managing and interacting with Vanilla Minecraft server versions."""

    def __init__(self, server_name: str = None, version: str = None, download_path: str = None):
        """
        Initialize a Vanilla instance.

            Args:
                server_name (str): Name of the Minecraft server.
                version (str): Minecraft server version.
                download_path (str): Path where the server files will be downloaded.
        """
        self.version = version
        self.server_name = server_name
        self.download_path = download_path
        self.vanilla_api_url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

    def get_version_info(self, version_id):
        """
        Get version information for a specific Minecraft version.

        Parameters:
        - version_id (str): ID of the Minecraft version.

        Returns:
        - str: URL containing information about the specified version.
        """
        try:
            response = requests.get(self.vanilla_api_url)
            response.raise_for_status()
            data = response.json()

            for entry in data['versions']:
                if version_id == entry['id']:
                    return entry['url']

            print(f"Version {version_id} not found.")
            return None

        except requests.RequestException as e:
            print(f"Error fetching version information for {version_id}: {e}")
            return None

    def get_version_group(self, group_name):
        """
        Get a list of versions belonging to a specific group.

        Parameters:
        - group_name (str): Name of the version group.

        Returns:
        - list: List of version IDs belonging to the specified group.
        """
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
        """
        Get the URL containing information for a specific Minecraft version.

        Parameters:
        - version_id (str): ID of the Minecraft version.

        Returns:
        - str: URL containing information about the specified version.
        """
        version_info = self.get_version_info(version_id)
        if version_info:
            return version_info
        return None

    def download_vanilla(self):
        """
        Download the Vanilla Minecraft server.

        Downloads the server based on the specified version and saves it in the designated download path.
        """
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
    """Class for managing and interacting with Spigot Minecraft server versions."""

    def __init__(self, server_name: str = None, version: str = None, download_path: str = None):
        """
        Initialize a Spigot instance.

        Parameters:
        - server_name (str): Name of the Minecraft server.
        - version (str): Minecraft server version.
        - download_path (str): Path where the server files will be downloaded.
        """
        self.server_name = server_name
        self.version = version
        self.download_path = download_path
        self.buildtools_download = "https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar"
        self.versions_url = "https://hub.spigotmc.org/versions/"

    def get_spigot_versions(self):
        """
        Get a list of Spigot Minecraft server versions.

        Returns:
        - list: List of Spigot Minecraft server versions.
        """
        try:
            response = requests.get(self.versions_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            versions = [link.get('href') for link in soup.find_all('a', href=True) if link['href'].startswith('1.')]
            filtered_versions = [version.replace('.json', '') for version in versions if
                                 all(substring not in version for substring in ['pre7', 'pre5', 'pre8', 'pre4', 'rc3'])]

            # Sort using custom_key
            sorted_versions = sorted(filtered_versions, key=custom_key, reverse=True)
            return sorted_versions
        except requests.RequestException as e:
            print(f"Error fetching Spigot versions: {e}")
            return None

    def download_spigot(self):
        """
        Download the Spigot Minecraft server.

        Downloads the server based on the specified version and saves it in the designated download path.
        """
        try:
            download_file(self.buildtools_download, self.download_path, "BuildTools.jar",
                          os.path.join(self.server_name, "BuildTools"))
            build_tools_path = os.path.join(self.download_path, self.server_name, "BuildTools", "BuildTools.jar")

            os.chdir(os.path.dirname(build_tools_path))

            os.system(f"java -jar BuildTools.jar --rev {self.version}")

            spigot_jar = f"spigot-{self.version}.jar"
            spigot_path = os.path.join(self.download_path, self.server_name, spigot_jar)
            os.rename(spigot_jar, spigot_path)

            print(f"Spigot {self.version} server downloaded successfully.")

        except requests.RequestException as e:
            print(f"Error downloading Spigot server: {e}")
        finally:
            os.chdir(os.path.dirname(os.path.realpath(__file__)))
