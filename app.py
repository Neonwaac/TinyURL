from flask import Flask
from src.controllers.links_controller import links_controller

app = Flask(__name__, template_folder='src/templates')

app.register_blueprint(links_controller)

if __name__ == '__main__':
    app.run(debug=True)