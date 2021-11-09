import os
from flask import Flask, request, abort, jsonify
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .database.models import setupDB,setupMigration,Movie,Actor
from .auth.auth import AuthError,requires_auth
import datetime

OBJECTS_PER_PAGE = 10
def paginate(request, all_list):
  page = request.args.get("page", 1, type=int)
  start = (page - 1) * OBJECTS_PER_PAGE
  end = start + OBJECTS_PER_PAGE
  all_list = [object_.format() for object_ in all_list]
  paginated_list = all_list[start:end]
  return paginated_list

def createApp():
  # create and configure the app
  app = Flask(__name__)
  setupDB(app)
  setupMigration(app)
  CORS(app)
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

  #Routs
  @app.route('/')
  def home():
      return jsonify({
          "success": True,
          "message": "Hello, Om kolthoum is the best singer of all times"
      })
  
  # routes for actors
  @app.route('/actors')
  @requires_auth('get:actors')
  def getActors(jwt):
    actors = Actor.query.all()
    paginated_actors=paginate(request,actors)
    if len(paginated_actors) == 0:
        abort(404)
    
    return jsonify({
        "success": True,
        "actors": paginated_actors
    })
    

  @app.route('/actors', methods=['POST'])
  @requires_auth('add:actors')
  def createActor(jwt):
    data = request.get_json()
    if 'name' not in data or 'age' not in data or 'gender' not in data:
        abort(400)
    actor = Actor(name=data['name'],
                  age=data['age'], gender=data['gender'])
    actor.insert()
    return jsonify({
        "success": True,
        "actor_id": actor.id
    })


  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def modifyActor(jwt, actor_id):
    data = request.get_json()
    if data is None:
      abort(400)
    actor = Actor.query.get(actor_id)
    if actor is None:
      abort(404)
    if 'name' in data:
      actor.name = data["name"]
    if 'age' in data:
      actor.age = data["age"]
    if 'gender' in data:
      actor.gender = data["gender"]
    actor.update()
    return jsonify({
        "success": True,
        "actor": actor.format()
    })

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def deleteActor(jwt, actor_id):
    actor = Actor.query.get(actor_id)
    if actor is None:
      abort(404)
    actor.delete()
    return jsonify({
        "success": True,
        "deleted": actor.id
    })

  #Movie Routs
  @app.route('/movies',methods=['GET'])
  @requires_auth('get:movies')
  def getMovies(jwt):
    movies = Movie.query.all()
    paginated_movies = paginate(request,movies)
    if len(paginated_movies)==0:
      abort(404)
    return jsonify({"success": True,
                    "movies": paginated_movies})


  @app.route('/movies', methods=['POST'])
  @requires_auth('add:movies')
  def addMovie(jwt):
    data = request.get_json()
    if 'title' not in data or 'release_date' not in data or 'genre' not in data:
      abort(400)

    movie = Movie(title=data['title'],
                  release_date=datetime.date.fromisoformat(data['release_date']), genre=data['genre'])
    movie.insert()
    return jsonify({
        "success": True,
        "movie_id": movie.id
    })
    
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def modifyMovie(jwt, movie_id):
      data = request.get_json()
      if data is None:
        abort(400)
  
      movie = Movie.query.get(movie_id)
      if movie is None:
        abort(404)
      if 'title' in data:
        movie.title = data["title"]
      if 'release_date' in data:
        movie.release_date = data["release_date"]
      if 'genre' in data:
        movie.genre = data["genre"]
      movie.update()
      return jsonify({
          "success": True,
          "movie": movie.format()
      })

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def deleteMovie(jwt, movie_id):
    movie = Movie.query.get(movie_id)
    if movie is None:
        abort(404)
    movie.delete()
    return jsonify({
        "success": True,
        "deleted": movie.id
    })

  @app.errorhandler(400)
  def badRequest(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400

  @app.errorhandler(404)
  def errorResourceNotFound(error):
    return jsonify({
        "success": False,
        "message": "Resource not found",
        "error": 404
    }), 404

  @app.errorhandler(AuthError)
  def authError(ex):
      print(ex)
      return jsonify({
          "success": False,
          "error": ex.status_code,
          "message": ex.error
      }), ex.status_code
  
  
  return app  

app = createApp()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)