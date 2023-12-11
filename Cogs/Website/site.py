from flask import Flask, render_template, request, jsonify
from Cogs.utils import Paper, Vanilla, Spigot

app = Flask(__name__, static_folder="./static", template_folder="./templates")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/create', methods=['GET', 'POST'])
def create_server():
    if request.method == 'POST':
        # Handle form submission logic here
        server_name = request.form.get('server_name')
        server_type = request.form.get('server_type')
        selected_version = request.form.get('server_version')
        download_path = request.form.get('download_path')
        release_group = request.form.get('release_group')
        # Vanilla
        vanilla = Vanilla(server_name, selected_version, download_path, release_group)
        vanilla.download_server()

        # Paper
        paper = Paper(server_name, selected_version, download_path)
        paper.download_paper()

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
        versions = ['1.17', '1.16.4', '1.14.4']
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
    print(release_group)
    v = Vanilla()
    versions = v.get_version_group(release_group)
    # Logic to fetch and return versions based on the selected release group
    # You can use the release_group parameter in your logic

    return {'versions': versions}

if __name__ == '__main__':
    app.run(debug=True)
