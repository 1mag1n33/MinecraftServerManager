from flask import Flask, render_template, request, jsonify
from Cogs.Utils.server_utils import Paper, Vanilla, Spigot
from Cogs.Utils.utils import save_server_info
from Cogs.SocketServer.Server import Socket

app = Flask(__name__, static_folder="./static", template_folder="./templates")

psocket = Socket()
servers = {"servers": []}
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/create', methods=['GET', 'POST'])
def create_server():
    if request.method == 'POST':
        server_id = psocket.server_id
        server_info = psocket.json_data
        server_name = request.form.get('server_name')
        server_type = request.form.get('server_type')
        selected_version = request.form.get('server_version')
        download_path = request.form.get('download_path')
        release_group = request.form.get('release_group')

        server_json = {
            "id": server_id,
            "name": server_name,
            "type": server_type,
            "version": selected_version,
            "release_group": release_group,
            "server_info": [server_info]
        }

        servers["servers"].append(server_json)

        save_server_info(servers)
        if server_type == 'vanilla':
            vanilla = Vanilla(server_name, selected_version, download_path)
            vanilla.download_vanilla()

        elif server_type == 'paper':
            paper = Paper(server_name, selected_version, download_path)
            paper.download_paper()

        elif server_type == 'spigot':
            spigot = Spigot(server_name, selected_version, download_path)
            spigot.download_spigot()

        else:
            # Handle the case where the selected version is not recognized
            print(f"Unsupported server type: {server_type}")

    return render_template('create_server.html')


@app.route('/api/get_server_types')
def get_server_types():
    # Logic to get server types (replace with your implementation)
    server_types = ['vanilla', 'spigot', 'paper']
    return jsonify({'serverTypes': server_types})


@app.route('/api/get_server_versions/<server_type>')
def get_server_versions(server_type):
    p = Paper()
    s = Spigot()
    if server_type == 'spigot':
        versions = s.get_spigot_versions()
    elif server_type == 'paper':
        versions = p.get_paper_versions()
    else:
        versions = []

    return jsonify({'versions': versions})


@app.route('/api/get_release_groups')
def get_release_groups():
    release_groups = ['release', 'snapshot', 'beta', 'alpha']
    return jsonify({'releaseGroups': release_groups})


@app.route('/api/get_versions/<release_group>')
def get_vanilla_versions(release_group):
    v = Vanilla()
    versions = v.get_version_group(release_group)
    return {'versions': versions}


if __name__ == '__main__':
    app.run(debug=True)
