from flask import Flask, render_template, request, jsonify
from Cogs.utils import Paper

app = Flask(__name__, static_folder="./static", template_folder="./templates")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/create', methods=['GET', 'POST'])
def create_server():
    global paper
    if request.method == 'POST':
        # Handle form submission logic here
        server_name = request.form.get('server_name')
        server_type = request.form.get('server_type')
        selected_version = request.form.get('server_version')
        download_path = request.form.get('download_path')
        paper = Paper(server_name, selected_version, download_path)
        paper.download_paper()

        # For GET requests or after processing POST data
    server_versions = paper.get_paper_versions()
    return render_template('create_server.html', server_versions=server_versions)


@app.route('/api/get_server_types')
def get_server_types():
    # Logic to get server types (replace with your implementation)
    server_types = ['vanilla', 'spigot', 'paper']
    return jsonify({'serverTypes': server_types})


@app.route('/api/get_server_versions/<server_type>')
def get_server_versions(server_type):
    p = Paper()
    if server_type == 'vanilla':
        versions = ['1.17.1', '1.16.5', '1.15.2']
    elif server_type == 'spigot':
        versions = ['1.17', '1.16.4', '1.14.4']
    elif server_type == 'paper':
        versions = p.get_paper_versions()
    else:
        versions = []

    return jsonify({'versions': versions})


if __name__ == '__main__':
    app.run(debug=True)
