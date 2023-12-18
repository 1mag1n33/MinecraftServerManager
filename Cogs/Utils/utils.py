import os
import requests
import json


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


def save_server_info(data):
    with open("server_data.json", 'w') as f:
        json.dump(data, f, indent=4)


def save_to_json(json_file: str, data):
    # Write server data to a JSON file
    with open(json_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def load_from_json(json_file: str, data):
    # Read server data from a JSON file
    try:
        with open(json_file, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        # Handle the case where the file does not exist
        pass
