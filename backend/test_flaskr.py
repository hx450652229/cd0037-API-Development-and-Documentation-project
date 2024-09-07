import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, QUESTIONS_PER_PAGE
from models import setup_db, Question, Category, db

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        
        # assume that the test database has been initialized same as production database
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client
                
        self.new_question = {
            'question': 'New question',
            'answer': 'New answer',
            'category': 2,
            'difficulty': 1
            }

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories_success(self):
        """Test get categories successfully"""
        res = self.client().get('/api/v1.0/categories')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreater(data['total_categories'], 0)
        self.assertGreater(len(data['categories']), 0)
    
    def test_get_questions_success(self):
        """Test get questions successfully"""
        res = self.client().get('/api/v1.0/questions')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreater(data['total_questions'], 0)
        self.assertGreater(len(data['questions']), 0)
        self.assertGreater(len(data['categories']), 0)
    
    def test_get_paginated_questions_success(self):
        """Test get paginated questions successfully"""
        res = self.client().get('/api/v1.0/questions?page=1')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreater(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), QUESTIONS_PER_PAGE)
        self.assertGreater(len(data['categories']), 0)
    
    def test_get_paginated_questions_invalid_page(self):
        """Test get paginated questions with invalid page"""
        res = self.client().get('/api/v1.0/questions?page=10000')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreater(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0) # empty results with invalid page
        self.assertGreater(len(data['categories']), 0)
    
    def test_create_question_success(self):
        """Test create question successfully"""
        res = self.client().post('/api/v1.0/questions', json=self.new_question)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        
        # remove the new question
        with self.app.app_context():
            Question.query.filter(Question.question == self.new_question['question']).delete()
            db.session.commit()
    
    def test_create_question_422_unprocessable(self):
        """Test create question with invalid data"""
        invalid_question = {
            'question': 'Invalid question',
            'answer': 'Invalid answer',
            'category': 20,
            'difficulty': 1
            }
        res = self.client().post('/api/v1.0/questions', json=invalid_question)
        self.assertEqual(res.status_code, 422)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Unprocessable')
    
    def test_delete_question_success(self):
        """Test delete question successfully"""
        # add new question
        with self.app.app_context():
            q = Question(question=self.new_question['question'],
                        answer=self.new_question['answer'],
                        category=self.new_question['category'],
                        difficulty=self.new_question['difficulty'])
            q.insert()
            db.session.commit()
            q_id = q.id
        
        res = self.client().delete(f'/api/v1.0/questions/{q_id}')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
    
    def test_delete_question_404_not_found(self):
        """Test delete question with invalid id"""
        res = self.client().delete(f'/api/v1.0/questions/1234567890')
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource Not Found')
    
    def test_search_question_success(self):
        """Test search question successfully"""
        res = self.client().post('/api/v1.0/questions/search?search_term=Indian')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['questions'][0]['question'], 'The Taj Mahal is located in which Indian city?')
        self.assertEqual(data['questions'][0]['answer'], 'Agra')
    
    def test_search_question_emtpy_results(self):
        """Test search question with emtpy results returned"""
        res = self.client().post('/api/v1.0/questions/search', query_string={'search_term': 'blablabla'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)
    
    def test_get_questions_by_category_success(self):
        """Test get questions by category successfully"""
        res = self.client().get('/api/v1.0/categories/1/questions')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 3)
        self.assertEqual(len(data['questions']), 3)
        self.assertEqual(data['current_category'], 'Science')
    
    def test_get_questions_by_category_404_not_found(self):
        """Test get questions by category with invalid category id"""
        res = self.client().get('/api/v1.0/categories/1234/questions')
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource Not Found')
    
    def test_play_quiz_no_previous_success(self):
        """Test play quiz without previous questions"""
        res = self.client().post('/api/v1.0/quizzes', json={'previous_questions': [], 'quiz_category': {'id': 1}})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])
    
    def test_play_quiz_with_previous_success(self):
        """Test play quiz with previous questions"""
        res = self.client().post('/api/v1.0/quizzes', json={'previous_questions': [20, 22], 'quiz_category': {'id': 1}})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        # the only remaining question in this category
        self.assertEqual(data['question']['id'], 21)
    
    def test_play_quiz_no_more_questions(self):
        """Test play quiz after having consumed all questions in this category"""
        res = self.client().post('/api/v1.0/quizzes', json={'previous_questions': [20, 21, 22], 'quiz_category': {'id': 1}})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        # no more question in this category
        self.assertIsNone(data['question'])
    
    def test_play_quiz_invalid_category_id(self):
        """Test play quiz with invalid category id"""
        res = self.client().post('/api/v1.0/quizzes', json={'previous_questions': [5], 'quiz_category': {'id': 12345}})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIsNone(data['question'])
        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()