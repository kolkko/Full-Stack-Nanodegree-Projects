import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','a','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

#----------------------------------------------------------------------------#
# Test: /questions GET (success & error)
#----------------------------------------------------------------------------#

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])

    def test_get_questions_paginated(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])

    def test_error_404_get_questions(self):
        """Test out of scope page"""
        res = self.client().get('/questions?page=1000')
        print('TESTING')
        data = json.loads(res.data)
        print('DATA: ', data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

#----------------------------------------------------------------------------#
# Test: /questions POST (success & error)
#----------------------------------------------------------------------------#

    def test_create_question(self):
        # New question details, for test
        json_test_question = {
            'question': 'Test question',
            'answer': 'Test answer',
            'category': '1',
            'difficulty': 1
        }

        res = self.client().post('/questions', json = json_test_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['qid']),
        self.assertTrue(data['questions'])

    def test_error_400_create_question(self):
        json_test_question = {
            'answer': 'Test answer',
            'category': '1',
            'difficulty': 1
        }

        res = self.client().post('/questions', json = json_test_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

#----------------------------------------------------------------------------#
# Test: /questions DELETE (success & error)
#----------------------------------------------------------------------------#

    def test_delete_question(self):
        # Create a new question, so that it can be deleted
        json_test_question = {
            'question': 'Delete Test question',
            'answer': 'Delete Test answer',
            'category': '1',
            'difficulty': 1
        }
        res = self.client().post('/questions', json = json_test_question)
        data = json.loads(res.data)
        question_id = data['qid']

        # Test the DELETE request by deleting the new question
        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_error_400_delete_question(self):
        """Try to delete an non-existant ID"""
        res = self.client().delete('/questions/{}'.format(99999))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

#----------------------------------------------------------------------------#
# Test: /questions SEARCH (success & error)
#----------------------------------------------------------------------------#

    def test_search_questions(self):
        # Search term, for test
        json_test_search = {
            'searchTerm': 'title'
        }

        res = self.client().post('/questions/search', json = json_test_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True),
        self.assertTrue(data['questions'])

    def test_error_400_search_questions(self):
        res = self.client().post('/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

#----------------------------------------------------------------------------#
# Test: /categories GET (success & error)
#----------------------------------------------------------------------------#

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_error_405_get_categories(self):
        """Test using wrong method"""
        res = self.client().patch('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

#----------------------------------------------------------------------------#
# Test: /questions/<int:category_id> GET (success & error)
#----------------------------------------------------------------------------#

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])

    def test_error_400_get_questions_by_category(self):
        """Test 400 if non-existent category requested"""
        res = self.client().get('/categories/56556565/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

#----------------------------------------------------------------------------#
# Test: /quizzes POST (success & error)
#----------------------------------------------------------------------------#
    def test_quizzes_with_category(self):
        """Test /quizzes works with a given category"""
        json_quiz_data = {
            'previous_questions' : '',
            'quiz_category' : {
                'type' : 'History',
                'id' : '4'
            }
        }
        res = self.client().post('/quizzes', json = json_quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']['question'])

    def test_quizzes_with_category_previous_questions(self):
        """Test /quizzes works with a given category and questions"""
        json_quiz_data = {
            'previous_questions' : '5',
            'quiz_category' : {
                'type' : 'History',
                'id' : '4'
            }
        }
        res = self.client().post('/quizzes', json = json_quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']['question'])

    def test_quizzes_no_category(self):
        """Test /quizzes works with no category"""
        json_quiz_data = {
            'previous_questions' : '',
        }
        res = self.client().post('/quizzes', json = json_quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']['question'])

    def test_quizzes_no_json(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()