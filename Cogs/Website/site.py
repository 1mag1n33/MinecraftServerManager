from flask import Flask, render_template

app = Flask(__name__, static_folder="./static", template_folder="./templates")

@app.route('/')
def home():
    # Add logic to get server status, player list, etc.
    server_status = "Running"
    players_online = ["Player1", "Player2"]

    return render_template('index.html', server_status=server_status, players_online=players_online)

if __name__ == '__main__':
    app.run(debug=True)
