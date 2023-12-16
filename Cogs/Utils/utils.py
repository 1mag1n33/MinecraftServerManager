import os
import requests


def download_file(url, save_path, jar_file, server_name):
    s_path = f"{save_path}\\{server_name}"
    dir_path = os.path.abspath(s_path)
    d_path = os.path.join(dir_path, jar_file)
    os.makedirs(os.path.dirname(d_path), exist_ok=True)
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_path = d_path
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            return True
    except requests.RequestException as e:
        print(f"Error downloading file: {e}")

    return False


def custom_key(version):
    """Custom sorting key for versions."""
    parts = version.split('.')
    return tuple(int(part) if part.isdigit() else float('inf') for part in parts)
