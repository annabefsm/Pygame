from flask import Flask, render_template
from game import game_loop

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/play")
def play():
    game_loop()
    return "Jogo executado com sucesso!"

if __name__ == "__main__":
    app.run()