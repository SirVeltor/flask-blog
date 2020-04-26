from app import create_app
from config.config import Config, DevelopingConfig

config = DevelopingConfig
app = create_app(config)

# Inicio de la app de forma provisional
if __name__ == '__main__':
    app.run(port='8000', debug=True)
