import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr.database.models import setupDB,createAll, Movie, Actor
from flaskr import createApp
import datetime

# TEST_DATABASE_URI = os.getenv('TEST_DATABASE_URI')
# ASSISTANT_TOKEN = os.getenv('ASSISTANT_TOKEN')
# DIRECTOR_TOKEN = os.getenv('DIRECTOR_TOKEN')
# PRODUCER_TOKEN = os.getenv('PRODUCER_TOKEN')
TEST_DATABASE_URI = 'postgresql://postgres:2271996@localhost:5432/castingagency'
ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjYwRk5PUFlGTHNLMklmUlRMRUs0aCJ9.eyJpc3MiOiJodHRwczovL2Rldi00cHlmN3JoOS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE3MTNjZjcxZTM4ZDkwMDY4NjIyMDljIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYzNjM3NTA5OCwiZXhwIjoxNjM2MzgyMjk4LCJhenAiOiJYMEJRMzZpVzYzQ0VZOXBSZ2pjaVlEVXNnRTVDVldQYyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.eOoEATf7TrYrYld9oRsGFKQj4yndemIZl44YdwDGM5Jc17g2f06oNJp1PRBUsASBJR5pAbZpabs_U94UxeYFjzaY209NvLUhFj6i8p-s9tLlzv8oduxPUwqr0zDauHKx3jHcWcIjGw8POlUBjrGznAiVHTMp9PRNYFSKZxUtksxSDQz6rAlF80eazrN0h5-3aKVHrUkgrOBBu5LhDbb481y3uJWsmb2NxBGXEB1_hRzGJSswFKGwhRl-78eSN9orywSrvbPRR09kqdNITaXv6MRjoc7L6bAstAHc_4qMkN9_nXJRwf4YRpD-7e40__myT9xu1AsatINOccqkOfKAvA'
DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjYwRk5PUFlGTHNLMklmUlRMRUs0aCJ9.eyJpc3MiOiJodHRwczovL2Rldi00cHlmN3JoOS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE3MTNjYjdmZjg2ZjYwMDZhM2JlMGQyIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYzNjM3NjE5OSwiZXhwIjoxNjM2MzgzMzk5LCJhenAiOiJYMEJRMzZpVzYzQ0VZOXBSZ2pjaVlEVXNnRTVDVldQYyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyJdfQ.C82JrPXvO9BTVet9PgDF4KbnU171kpxBzXs2BjfYSLe_FynBJlsHoRpYhR8HnL0WmU7iP3pMKrLNijyqtC8YWt8ODLrFdnKSWj_iH-LZUBDskYf8YjmAgzqIyFtG_-WRY_2XWhMPABQcdiuBgfxKGBO6sDydXLUAY399Ff3aBEqv77YAnNGnRP-YirxBuSZzR3_PKZySYBFgK5smdQxdO5AmW4XX_i0zGlwmFs7LkExRazRoM6glLnP2hRmgeYUd9-hGYsEJ0W8d0zf3GGmVNk3ZaIvdqUl0RElsYaNjTzf3TCi3rr6QiNSEFnrlKI1jvfRR5ZIIVl88aQcv7htYpQ'
PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjYwRk5PUFlGTHNLMklmUlRMRUs0aCJ9.eyJpc3MiOiJodHRwczovL2Rldi00cHlmN3JoOS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE4ODAzNjVhYjc5YzkwMDcxMzVlNmI2IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYzNjM3NDYzNSwiZXhwIjoxNjM2MzgxODM1LCJhenAiOiJYMEJRMzZpVzYzQ0VZOXBSZ2pjaVlEVXNnRTVDVldQYyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIl19.GerSbqbeJ89d6sRLAlre_U_Pvoo-eLEbUbaDP5b4GrAXoqEKrVOzADpQ58u01WxyMSk0VpW_AmH6ZIe6WgAxPQRIiumr3VPwU9OFeHeVWmFWv7un5ZL3yNe58u6efrq-w31WpHFQoh0uNCbl_cEV0Ia5cTeakuTnDpDCPJuW78uVg_GD9kTolvy0Ab9g3CTihhlzlWjaqlpdN0PnxX8WgiEPylujAd-yP1j6Fi8r4JGhDKqA-xXmVT387x828vRpbECK3WR4x5J9kauZP5blZDruVo5iTLHk5smGSduq-Zqn4FNAvROvl7OEJ9S9sGdO1rBkRvkJPHfgQzfu_bFtYw'

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        self.app = createApp()
        self.client = self.app.test_client
        setupDB(self.app, TEST_DATABASE_URI)
        self.casting_assistant = ASSISTANT_TOKEN
        self.casting_director = DIRECTOR_TOKEN
        self.executive_producer = PRODUCER_TOKEN
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            createAll()

    def tearDown(self):
        """Executed after reach test"""
        pass
    
    
    def testGetActors(self):
        actor=Actor(name='Johny',
                    age=60,
                    gender='male')
        actor.insert()
        res=self.client().get('/actors',
                              headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.executive_producer)
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    def testPostActors(self):
        actor = {
            "name": "Alpachino",
            "gender": "male",
            "age": 70
        }

        res = self.client().post('/actors',
                                 headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.casting_director)
                                 }, json=actor)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        actor_db  = Actor.query.get(data['actor_id'])
        actor['id'] = data['actor_id']
        self.assertEqual(actor_db .format(), actor)

    def testPatchActor(self):
        actor=Actor(name='Johny',
                    age=60,
                    gender='male')
        actor.insert()#so we have at least one Actor
        
        actor_patch = {
            "gender": "male",
            "age": 70
        }

        res = self.client().patch('/actors/'+str(actor.id),
                                  headers={
            "Authorization": "Bearer {}".format(self.executive_producer)
        }, json=actor_patch)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(200, res.status_code)
        actor = Actor.query.get(data['actor']['id'])
        actor_json = actor.format()
        for key in actor_patch.keys():
            self.assertEqual(actor_patch[key], actor_json[key])

    def testDeleteActor(self):
        actor=Actor(name='Johny',
                    age=60,
                    gender='male')
        actor.insert()#so we have at least one Actor
        
        res = self.client().delete('/actors/'+str(actor.id),
                                    headers={
            "Authorization": "Bearer {}"
            .format(self.executive_producer)})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        actor = Actor.query.get(data['deleted'])
        self.assertEqual(actor, None) 

    def testPostActorFail400(self):
        actor = {
            "name": "Alpachino",
            "age": 70
        }
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.executive_producer)
                                 }, json=actor)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(400, res.status_code)
        self.assertNotEqual(len(data['message']), 'Bad request')

    def testGetActorsFails401(self):
        actor=Actor(name='Johny',
                    age=60,
                    gender='male')
        actor.insert()
        res=self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def testDeleteActorFail403(self):
        actor=Actor(name='Johny',
                    age=60,
                    gender='male')
        actor.insert()#so we have at least one Actor
         
        res = self.client().delete('/actors/'+str(actor.id),
                                    headers={
            "Authorization": "Bearer {}"
            .format(self.casting_assistant)})
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(403, res.status_code)
        
    def testPatchActorFail404(self):
        actor_patch = {
            "gender": "male",
            "age": 70
        }
        res = self.client().patch('/actors/1000',
                                  headers={
                                      "Authorization": "Bearer {}"
                                      .format(self.casting_director)
                                  }, json=actor_patch)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(404, res.status_code)
      
    def testPostActorFail400(self):
        actor = {
            "gender": "male",
            "age": 70
        }
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.executive_producer)
                                 }, json=actor)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(400, res.status_code)
        self.assertNotEqual(len(data['message']), 'Bad request') 
        


    def testGetMovies(self):
        movie=Movie(title='Inglourious Basterds',
                    release_date=datetime.date.fromisoformat('2009-05-09'),
                    genre='Tarantino')
        movie.insert()
        res=self.client().get('/movies',
                              headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.executive_producer)
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    def testPostMovies(self):
        movie = {
            "title": "Inglourious Basterds",
            "release_date": "2009-05-09",
            "genre": "Tarantino"
        }

        res = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.executive_producer)
                                 }, json=movie)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        movie_db = Movie.query.get(data['movie_id'])
        movie['id'] = data['movie_id']
        self.assertEqual(movie_db.format(), movie)

    def testPatchMovie(self):
        movie=Movie(title='Inglourious Basterds',
                    release_date=datetime.date.fromisoformat('2009-05-09'),
                    genre='Tarantino')
        movie.insert()#so we have at least one movie
        movie_patch = {
            "title": "Django Unchained",
            "release_date": "2010-01-02",
        }

        res = self.client().patch('/movies/'+str(movie.id),
                                  headers={
            "Authorization": "Bearer {}".format(self.executive_producer)
        }, json=movie_patch)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(200, res.status_code)
        movie = Movie.query.get(data['movie']['id'])
        movie_json = movie.format()
        for key in movie_patch.keys():
            self.assertEqual(movie_patch[key], movie_json[key])

    def testDeleteMovie(self):
        movie=Movie(title='Inglourious Basterds',
                    release_date=datetime.date.fromisoformat('2009-05-09'),
                    genre='Tarantino')
        movie.insert()#so we have at least one movie

        res = self.client().delete('/movies/'+str(movie.id),
                                    headers={
            "Authorization": "Bearer {}"
            .format(self.executive_producer)})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        movie = Movie.query.get(data['deleted'])
        self.assertEqual(movie, None) 

    def testPostMoviesFail400(self):
        movie = {
            "release_date": "2009-05-09",
            "genre": "Tarantino"
        }
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.executive_producer)
                                 }, json=movie)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(400, res.status_code)
        self.assertNotEqual(len(data['message']), 'Bad request')

    def testGetMoviesFails401(self):
        movie=Movie(title='Inglourious Basterds',
                    release_date=datetime.date.fromisoformat('2009-05-09'),
                    genre='Tarantino')
        movie.insert()
        res=self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def testDeleteMovieFail403(self):
        movie=Movie(title='Inglourious Basterds',
                    release_date=datetime.date.fromisoformat('2009-05-09'),
                    genre='Tarantino')
        
        movie.insert()#so we have at least one movie
        print("aaaaa"+str(movie.id))    
        res = self.client().delete('/movies/'+str(movie.id),
                                    headers={
            "Authorization": "Bearer {}"
            .format(self.casting_assistant)})
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(403, res.status_code)
        
    def testPatchMovieFail404(self):
        movie = {
            "title": "into the wild",
            "release_date": "2007-01-02",
        }
        res = self.client().patch('/movies/1000',
                                  headers={
                                      "Authorization": "Bearer {}"
                                      .format(self.casting_director)
                                  }, json=movie)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(404, res.status_code)
      
    def testPostMoviesFail400(self):
        movie = {
            "title": "Arrival",
            "release_date": "2016-01-02",
        }
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.executive_producer)
                                 }, json=movie)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(400, res.status_code)
        self.assertNotEqual(len(data['message']), 'Bad request') 
        
if __name__ == "__main__":
    unittest.main()