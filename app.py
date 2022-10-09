# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

from create_data import Movie, Genre, Director
from schemas import MovieSchema, GenreSchema, DirectorSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['RESTX_JSON'] = {'ensure_ascii': False}
api = Api(app)

movie_ns = api.namespace('movies')
movies_schemas = MovieSchema(many=True)
movies_schema = MovieSchema()

@movie_ns.route("/")
class MovieViews(Resource):
    def get(self):
        query = Movie.query

        director_id = request.args.get('director_id')
        if director_id:
            query = query(Movie).filter(Movie.director_id == director_id)

        if genre_id := request.args.get('genre_id'):
            query = query(Movie).filter(Movie.genre_id == genre_id)

        return movies_schemas.dump(query)

    def post(self):
        data = request.json
        try:
            db.session.add(
                Movie(
                    **data
                )
            )
            db.session.commit()
            return 'Данные добавлены', 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

@movie_ns.route("/<int:bid>")
class MovieViews(Resource):
    def get(self, bid):
        query = Movie.query.get(bid)
        return movies_schema.dump(query)

    def put(self, bid):
        data = request.json
        try:
            db.session.query(Movie).filter(Movie.id == bid).update(
                data
            )
            db.session.commit()
            return 'Данные обновлены', 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

    def delete(self, bid):
        try:
            db.session.query(Movie).filter(Movie.id == bid).delete()
            db.session.commit()
            return 'Данные удалены', 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

genre_ns = api.namespace('genres')
genre_schemas = GenreSchema(many=True)
genre_schema = GenreSchema()
@genre_ns.route("/")
class GenreViews(Resource):
    def get(self):
        query = Genre.query

        return genre_schemas.dump(query)

    def post(self):
        data = request.json
        try:
            db.session.add(
                Genre(
                    **data
                )
            )
            db.session.commit()
            return 'Данные добавлены', 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

@genre_ns.route("/<int:bid>")
class GenreViews(Resource):
    def get(self, bid):
        query = Genre.query.get(bid)
        return genre_schema.dump(query)

    def put(self, bid):
        data = request.json
        try:
            db.session.query(Genre).filter(Genre.id == bid).update(
                data
            )
            db.session.commit()
            return 'Данные обновлены', 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

    def delete(self, bid):
        try:
            db.session.query(Genre).filter(Genre.id == bid).delete()
            db.session.commit()
            return 'Данные удалены', 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

director_ns = api.namespace('directors')
director_schemas = DirectorSchema(many=True)
director_schema = DirectorSchema()

@director_ns.route("/")
class DirectorViews(Resource):
    def get(self):
        query = Director.query
        return genre_schemas.dump(query)

    def post(self):
        data = request.json
        try:
            db.session.add(
                Director(
                    **data
                )
            )
            db.session.commit()
            return 'Данные добавлены', 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

@director_ns.route("/<int:bid>")
class DirectorViews(Resource):
    def get(self, bid):
        query = Director.query.get(bid)
        return director_schema.dump(query)

    def put(self, bid):
        data = request.json
        try:
            db.session.query(Director).filter(Director.id == bid).update(
                data
            )
            db.session.commit()
            return 'Данные обновлены', 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

    def delete(self, bid):
        try:
            db.session.query(Director).filter(Director.id == bid).delete()
            db.session.commit()
            return 'Данные удалены', 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200


if __name__ == '__main__':
    app.run(debug=True)
