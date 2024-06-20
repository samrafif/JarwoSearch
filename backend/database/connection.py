from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

Base = declarative_base()
db = SQLAlchemy(model_class=Base)