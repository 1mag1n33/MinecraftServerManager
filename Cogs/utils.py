import os
import requests


# Jar downloads

class Paper:
    """Class for interacting with Paper API and downloading Paper builds."""

    def __init__(self, version, download_path):
        """Initialize Paper instance.

            Args:
                version (str): Paper version.
                download_path (str): Path to save the downloaded Paper JAR.
        """
        self.latest_build = None
        self.version = version
        self.download_path = os.path.abspath(download_path)
        self.paper_api_url = f"https://api.papermc.io/v2/projects/paper/versions/{self.version}/builds"

    def get_latest_build(self):

        """Retrieve the download URL for the latest Paper build.

            Returns:
                str: Download URL if successful, None otherwise.
        """
        try:
            response = requests.get(self.paper_api_url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            data = response.json()
            if 'builds' in data and data['builds']:
                self.latest_build = data['builds'][1]['build']
                print(self.latest_build)
                paper_download_url = f"https://api.papermc.io/v2/projects/paper/versions/{self.version}/builds/{self.latest_build}/downloads/paper-{self.version}-{self.latest_build}.jar"
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
        download_path = f"{self.download_path}/paper-{self.version}-{self.latest_build}.jar"
        if paper_download_url:
            os.makedirs(os.path.dirname(self.download_path), exist_ok=True)
            download_file(paper_download_url, download_path)
            return True
        return False


def vanilla():
    pass


def spigot():
    pass


def download_file(url, save_path):
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
