import types

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import backend.constants as constants

def get_connection_url(database_config: constants.Database):
    
    return (f"postgresql+psycopg2://{database_config.username}:{database_config.password}" +
            f"@{database_config.hostname}:{database_config.port}/{database_config.database}")

db = SQLAlchemy()
migrate = Migrate()