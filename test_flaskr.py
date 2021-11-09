import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr.database.models import setupDB,createAll, Movie, Actor
from flaskr import createApp
import datetime

TEST_DATABASE_URI = os.getenv('DATABASE_URL')
ASSISTANT_TOKEN = os.getenv('ASSISTANT_TOKEN')
DIRECTOR_TOKEN = os.getenv('DIRECTOR_TOKEN')
PRODUCER_TOKEN = os.getenv('PRODUCER_TOKEN')
# TEST_DATABASE_URI = 'postgresql://postgres:2271996@localhost:5432/castingagency'
# ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjYwRk5PUFlGTHNLMklmUlRMRUs0aCJ9.eyJpc3MiOiJodHRwczovL2Rldi00cHlmN3JoOS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE3MTNjZjcxZTM4ZDkwMDY4NjIyMDljIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYzNjQ2NDMwNCwiZXhwIjoxNjM2NDcxNTA0LCJhenAiOiJYMEJRMzZpVzYzQ0VZOXBSZ2pjaVlEVXNnRTVDVldQYyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.CeiKpRBAIqewNAJWTfphnQfgOEGeG9RaHidiNoK3BVkDLYG47EU-Nfwzbw6fgO6Uducx1IPjyctHBcvxYe3rslnBIAe10tesZlFqgy4XS5meiaAbTVrPPubOld_pH_EKLLncJ2krpek0y93guyGxkH4PqzdWYnAwxUKyGwtQg6KasMrzEx8pk4g4Kw7q2m4-5ouyWNNtCZfCgvrUAgHWIRsPr2TvJGAw4ySiR291Xi9uW0cs2xPXKOhrm34Po1sTJ4Jg9RqusYiEoPVIZSZwRilzA3UzbdgxDvQpGR3Z9Kg3krk2tvg8CIRCr62DBNB8rM29-S4JdBGVfVw3kFo-Ag'
# DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjYwRk5PUFlGTHNLMklmUlRMRUs0aCJ9.eyJpc3MiOiJodHRwczovL2Rldi00cHlmN3JoOS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE3MTNjYjdmZjg2ZjYwMDZhM2JlMGQyIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYzNjQ2NDM1OCwiZXhwIjoxNjM2NDcxNTU4LCJhenAiOiJYMEJRMzZpVzYzQ0VZOXBSZ2pjaVlEVXNnRTVDVldQYyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyJdfQ.F_XVaEL770mqQtCSgHUCNhn3iNxoRqGS0m6VF5NDLdpr5TI2vwfQTKuRL6YCNh7cLhCHRp8q-AtfIvbv6PEiAFfqLEvcd8aC2NrhAtCrhdG8RCevhOdKPUrbEq9AjcTUixfW8gkmrNeqRu1iG22zZUhebZJPcvacsOKXMsaq9Iby-Ic8dyRvapJ5897CALPgGPkhTLROKXg0JCv3H5uXhhp5XI_0H6sFgaauKky-IL7RgFVHRpTcXZYrgveLhMwc0j9KcB5L5BjatG1oR9EFNICOfJak27BpTOUvAKc7ZkniFCnwfPywZ-Ultm7hF0BQHyi53pYqYhX8GyUhhYR1Yw'
# PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjYwRk5PUFlGTHNLMklmUlRMRUs0aCJ9.eyJpc3MiOiJodHRwczovL2Rldi00cHlmN3JoOS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE4ODAzNjVhYjc5YzkwMDcxMzVlNmI2IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYzNjQ2NDQxMCwiZXhwIjoxNjM2NDcxNjEwLCJhenAiOiJYMEJRMzZpVzYzQ0VZOXBSZ2pjaVlEVXNnRTVDVldQYyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIl19.LNvh6-OXlXsYnD5hnHuekTIV7UfWAyV85H7_mUQw5Jb47CQlsrMcg3KvffxQKbqjYWSE0FLGV5fiqpsRkO9hO5mrhNta05QahR-qV8CAoCPDK9fsamRo8lfsaginW85l0q97ZDWHjKts-BA2pKzSDdKqNYSskxDV9FGY4Ti9ND3XsbC31pTY6rBDi4aQAehwbiri93CECCa-cd-mP0brld6p33_CBdYLUIXVZDK58mlgego44jd8nsWw4OJfmK3uYPhuTA-LrhqWJL6fsEsphY6LAEjqwYrlQp4SCI8YCsEENBAF0LK2-N4XYWutjzG7xfIaesFY2UCCqnz9QlzO3w'

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