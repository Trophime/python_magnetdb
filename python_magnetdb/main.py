from fastapi import FastAPI
from fastapi_pagination import Page, add_pagination, paginate

from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, escape, request
from . import flask_routers

flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = "powerful secretkey"
flask_app.config['WTF_CSRF_SECRET_KEY'] = "a csrf secret key"

flask_app.register_blueprint(flask_routers.urls_blueprint)

from .routers import itemrouter

app = FastAPI()
app.include_router(itemrouter)

app.mount("/", WSGIMiddleware(flask_app))

add_pagination(app)