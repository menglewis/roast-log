import os
from app import create_app
from app.settings import ProdConfig, DevConfig

if os.environ.get("ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

application = app
