from api_server import create_app
from waitress import serve
from config import Config
app = create_app()


if __name__ == '__main__':
    serve(app, port=Config.PORT)
