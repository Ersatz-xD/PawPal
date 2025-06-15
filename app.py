import webbrowser
from flask import Flask
from app.routes import main  # Import the Blueprint, not the Flask app

app = Flask(
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
)

app.secret_key = 'your-secret-key'  # Required for flashing messages
app.register_blueprint(main)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    open_browser()
    app.run(debug=True)