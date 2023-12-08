import os
import requests


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
        self.download_path = os.path.abspath(self.download_path)
        paper_download_url = self.get_latest_build()
        download_path = os.path.join(self.download_path, f"paper-{self.version}-{self.latest_build}.jar")

        # Ensure the directory exists
        os.makedirs(os.path.dirname(download_path), exist_ok=True)

        if paper_download_url:
            download_file(paper_download_url, download_path)
            return True
        return False


class Vanilla:
    def __init__(self):
        pass


class Spigot:
    def __init__(self):
        pass


def download_file(url, save_path):
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
