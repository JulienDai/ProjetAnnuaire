from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import flask

db = SQLAlchemy()


def init_database():
    db.create_all()


