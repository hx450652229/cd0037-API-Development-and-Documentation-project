import os
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS, cross_origin
import random
from werkzeug.exceptions import HTTPException

from models import setup_db, Question, Category, db
from functools import wraps

QUESTIONS_PER_PAGE = 10


def categories_to_dict(categories):
    """Converts a category list to dict

    Args:
        categories (List[Category]): List of categories

    Returns:
        dict: Category dict as {category.id: category.type}
    """
    categories_dict = dict()
    for c in categories:
        categories_dict[c.id] = c.type
    return categories_dict


def handle_exceptions(f):
    """Try-except decorator

    Args:
        f (function): Endpoint function

    Returns:
        function: Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except HTTPException as e:
            # forward known http exception
            raise e
        except Exception as e:
            # abort with 500 for unknown exception
            print(e)
            abort(500)
        finally:
            db.session.rollback()
            db.session.close()

    return decorated_function


def create_app(test_config=None):
    """Create and configure app

    Args:
        test_config (dict): Test configuration. Defaults to None.

    Returns:
        Flask: The flask app
    """
    app = Flask(__name__)

    with app.app_context():
        if test_config is None:
            setup_db(app)
        else:
            db_path = test_config.get('SQLALCHEMY_DATABASE_URI')
            setup_db(app, db_path=db_path)

    # Set up CORS. Allow '*' for origins
    CORS(app, resources={r'/api/*': {"origins": "*"}})

    @app.after_request
    def after_request(response):
        """The after_request decorator to set Access-Control-Allow"""
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/api/v1.0/categories')
    @cross_origin()
    @handle_exceptions
    def get_categories():
        """Endpoint to handle GET requests for all available categories."""
        categories = Category.query.all()
        return jsonify({
            'success': True,
            'total_categories': len(categories),
            'categories': categories_to_dict(categories)
        })

    @app.route('/api/v1.0/questions')
    @cross_origin()
    @handle_exceptions
    def get_paginated_questions():
        """
        Endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        This endpoint should return a list of questions,
        number of total questions, current category, categories.

        TEST: At this point, when you start the application
        you should see questions and categories generated,
        ten questions per page and pagination at the bottom of the screen for three pages.
        Clicking on the page numbers should update the questions.
        """
        page = request.args.get('page', 1, type=int)
        questions = Question.query.order_by(Question.id).paginate(
            page=page, per_page=QUESTIONS_PER_PAGE, error_out=True).items
        categories = Category.query.order_by(Category.id).all()
        categories_dict = categories_to_dict(categories)

        return jsonify({
            'success': True,
            'total_questions': len(questions),
            'questions': [q.format() for q in questions],
            'categories': categories_dict,
        })

    @app.route('/api/v1.0/questions/<int:question_id>', methods=['DELETE'])
    @cross_origin()
    @handle_exceptions
    def delete_question(question_id):
        """
        Endpoint to DELETE question using a question ID.

        TEST: When you click the trash icon next to a question, the question will be removed.
        This removal will persist in the database and when you refresh the page.
        """
        q = Question.query.get(question_id)
        if q is None:
            abort(404)

        q.delete()
        return jsonify({
            'success': True,
            'id': question_id
        })

    @app.route('/api/v1.0/questions', methods=['POST'])
    @cross_origin()
    @handle_exceptions
    def create_question():
        """
        Endpoint to POST a new question,
        which will require the question and answer text,
        category, and difficulty score.

        TEST: When you submit a question on the "Add" tab,
        the form will clear and the question will appear at the end of the last page
        of the questions list in the "List" tab.
        """
        form = request.get_json()

        # check question and answer validity
        if form['question'] == '' or form['answer'] == '' or form['question'] is None or form['answer'] is None:
            abort(422)

        # check category validity
        if Category.query.get(form['category']) is None:
            abort(422)

        question = Question(
            question=form['question'],
            answer=form['answer'],
            difficulty=form['difficulty'],
            category=form['category'],
        )
        question.insert()
        return jsonify({
            'success': True
        })

    @app.route('/api/v1.0/questions/search', methods=['POST'])
    @cross_origin()
    @handle_exceptions
    def search_question():
        """
        POST endpoint to get questions based on a search term.
        It should return any questions for whom the search term
        is a substring of the question.

        TEST: Search by any phrase. The questions list will update to include
        only question that include that string within their question.
        Try using the word "title" to start.
        """
        search_term = request.args.get('search_term', '', type=str)
        questions = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).all()
        return jsonify({
            'success': True,
            'total_questions': len(questions),
            'questions': [q.format() for q in questions]
        })

    @app.route('/api/v1.0/categories/<int:category_id>/questions')
    @cross_origin()
    @handle_exceptions
    def get_questions_by_category(category_id):
        """
        GET endpoint to get questions based on category.

        TEST: In the "List" tab / main screen, clicking on one of the
        categories in the left column will cause only questions of that
        category to be shown.
        """
        category = Category.query.get(category_id)
        if category is None:
            abort(404)

        questions = [q.format() for q in Question.query.filter(
            Question.category == category_id).all()]
        return jsonify({
            'success': True,
            'total_questions': len(questions),
            'questions': questions,
            'current_category': category.type
        })

    @app.route('/api/v1.0/quizzes', methods=['POST'])
    @cross_origin()
    @handle_exceptions
    def play_quiz():
        """
        POST endpoint to get questions to play the quiz.
        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.

        TEST: In the "Play" tab, after a user selects "All" or a category,
        one question at a time is displayed, the user is allowed to answer
        and shown whether they were correct or not.
        """
        data = request.json
        category_id = data['quiz_category']['id']
        if int(category_id) > 0:
            question = Question.query.filter(Question.category == category_id, Question.id.not_in(
                data['previous_questions'])).order_by(func.random()).limit(1).all()
        else:
            question = Question.query.filter(Question.id.not_in(
                data['previous_questions'])).order_by(func.random()).limit(1).all()

        question_res = None
        if len(question) > 0:
            question_res = question[0].format()
        return jsonify({
            'success': True,
            'question': question_res
        })

    @app.errorhandler(404)
    def not_found(err):
        """Error handler for 404 not found"""
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404

    @app.errorhandler(400)
    def bad_request(err):
        """Error handler for 400 bad request"""
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(422)
    def unprocessable(err):
        """Error handler for 422 unprocessable"""
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(err):
        """Error handler for internal server error"""
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app
