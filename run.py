import os

from app import create_app
import app_config as config

env_setting = os.getenv("APP_SETTINGS")
# Incase there is no environment has been set fallback to production mode
if env_setting is None:
    env_setting = "development"
elif env_setting.strip() == "":
    env_setting = "development"

config_name = env_setting
app = create_app(config_name)

if __name__ == '__main__':
    app.run(debug=config.configurations[config_name].DEBUG)
