import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .database.models import setup_db#, Drink
from .auth.auth import AuthError, HiFromAuth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  # CORS(app)
  # @APP.after_request
  # def after_request(response):
  #   response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
  #   response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
  #   # response.headers.add('Access-Control-Allow-Origin', '*')
  #   return response













  return app  
APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)