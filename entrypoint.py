from app import create_app
import os

settings_module = os.getenv('APP_SETTINGS_MODULE')
print('settings module externa-->', settings_module)
app = create_app('config.local')

# Inicio de la app de forma provisional
if __name__ == '__main__':
    app.run(port='8000', debug=True)
