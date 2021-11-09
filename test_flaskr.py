import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr.database.models import setupDB,createAll, Movie, Actor
from flaskr import createApp
import datetime

TEST_DATABASE_URI = os.getenv('DATABASE_URL')
# ASSISTANT_TOKEN = os.getenv('ASSISTANT_TOKEN')
# DIRECTOR_TOKEN = os.getenv('DIRECTOR_TOKEN')
# PRODUCER_TOKEN = os.getenv('PRODUCER_TOKEN')
# TEST_DATABASE_URI = 'postgresql://postgres:2271996@localhost:5432/castingagency'
ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjYwRk5PUFlGTHNLMklmUlRMRUs0aCJ9.eyJpc3MiOiJodHRwczovL2Rldi00cHlmN3JoOS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE3MTNjZjcxZTM4ZDkwMDY4NjIyMDljIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYzNjQ3NDM5NiwiZXhwIjoxNjM2NDgxNTk2LCJhenAiOiJYMEJRMzZpVzYzQ0VZOXBSZ2pjaVlEVXNnRTVDVldQYyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.x-36m9QTUP75sb26kxzrr0lRTGtacTo4Muf246v_LifTEZPDYOQS69GwopdHF_mzfnCflh1DEOZzIzERjIV-6wwY61eNg9R_v31bLJvFJuwGD7RjrBuCKix_EQkPfh0-GeGBtZbQRKSYFUa6ZAMD-VFzac9F6c0ZtHzYME0LxKyoX_rOO6U3KUUreXh5i38WlCgC-2-URxU9oQF9aEpmyuo3TJXreb_e86Td8ArcH413pYjxtw8rb5EGlDuP2rplyZJg2yrJ3cRQuKrVnC2cRpHD32TqMoLlack91ui1clAKFndtiX30ODJzXVRkrqi4F6rJIp060SQMnGw_6yDdKg'
DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjYwRk5PUFlGTHNLMklmUlRMRUs0aCJ9.eyJpc3MiOiJodHRwczovL2Rldi00cHlmN3JoOS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE3MTNjYjdmZjg2ZjYwMDZhM2JlMGQyIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYzNjQ3NDQzOCwiZXhwIjoxNjM2NDgxNjM4LCJhenAiOiJYMEJRMzZpVzYzQ0VZOXBSZ2pjaVlEVXNnRTVDVldQYyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyJdfQ.tcRoZofMnPwmHBe1bg3SpH9NgTIcQapKhrXd0tKb0eT7edo7uGLCVJvNFeP4FHIb9ztZPY9hqmO0bo46t-ikq8Goi14EnTYsQe_Qabw-eiKrNEeW_7QH5Ecevy_j2YQtbJfMcaV5Pa1VA--hRCKreLR2luLnL8KiKFzv-scnJLdtOME1LFHhlVk5oKBD7PeJXoi_PZvfkyZ6uWJmoon6R-41kJVbVuGeC49UNRS-Ls3Zu2jhFdNWWY2wokjsFPE15KN8RNhF7H3XUFaIMk6V0Ex4xbDWcFbal_EvEW7_A2fR8mwRaiTz-4hBJ6Y5rgNMwDaroqEpKtsVqERGz00SUw'
PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjYwRk5PUFlGTHNLMklmUlRMRUs0aCJ9.eyJpc3MiOiJodHRwczovL2Rldi00cHlmN3JoOS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE4ODAzNjVhYjc5YzkwMDcxMzVlNmI2IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYzNjQ3NDQ5NywiZXhwIjoxNjM2NDgxNjk3LCJhenAiOiJYMEJRMzZpVzYzQ0VZOXBSZ2pjaVlEVXNnRTVDVldQYyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIl19.UhCg4Y_KbJ3r5NUh8ALF3E_HkNJ5Tw5sxIPosiwDiFVJ5eIBeiA_Em5fIfrTSYT6Py2nvtolsDoa90EK1Q0s8dRv5kqvPpVOY7PtT3tUUa7nautwXxm18IccklU5lWkPuW3rmApjQp9-bBHw6osaxIMuERkuqfkAXh7lL3ssBDT-ks6drstBScfDRa_UuBoNMefFZnMTh-YD-wqJ5k8_0bybURlH3TWr3czinNTefUnqufToAcyokdJ_a11sD-0bBIP9adARtn0C0iL2HY7Y60cZtt0j-yFhLaaNLXWWE44QfdbPxSAS5HZnZy9EUePqCvkJOf2AuQY0SmbXuAl-yw'

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

    def testPostActorsCastingDirector(self):
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

    def testPostActorsCastingAssistant(self):
        actor = {
            "name": "Alpachino",
            "gender": "male",
            "age": 70
        }
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.casting_assistant)
                                 }, json=actor)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(403, res.status_code)

    
    def testPatchActorProducer(self):
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

    def testPatchActorCastingAssistant(self):
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
            "Authorization": "Bearer {}".format(self.casting_assistant)
        }, json=actor_patch)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(403, res.status_code)



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

    
    def testPostMoviesProducer(self):
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


    def testPostMoviesCastingAssistant(self):
        movie = {
            "title": "Inglourious Basterds",
            "release_date": "2009-05-09",
            "genre": "Tarantino"
        }

        res = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.casting_assistant)
                                 }, json=movie)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(403, res.status_code)


    def testPatchMovieProducer(self):
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

    def testPatchMovieCastingAssistant(self):
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
            "Authorization": "Bearer {}".format(self.casting_assistant)
        }, json=movie_patch)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(403, res.status_code)
    

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