# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## API Reference

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "Bad request"
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 500: Internal Server Error

### Endpoints 

`GET '/api/v1.0/categories'`

- Description: Fetches all available categories
- Request Arguments: None
- Returns: Success value, categories as dictionary and number of total categories
- Sample: `/api/v1.0/categories`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```

`GET '/api/v1.0/questions'`

- Description: Fetches paginated questions with maximum 10 questions in each page
- Request Arguments:
  - `page` (optional, int): Specifies the page number for pagination. Default is 1 if not provided.
- Returns: Success value, questions in the specified page, number of all questions and all available categories
- Sample: `/api/v1.0/questions?page=1`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

`DELETE '/api/v1.0/questions/<int:question_id>'`

- Description: Deletes the question with given id
- Request Arguments:
  - `question_id` (integer, required): The ID of the question to delete.
- Returns: Success value, id of deleted question
- Sample: `/api/v1.0/questions/1` (DELETE request)
```json
{
  "success": true,
  "id": 1
}
```

`POST '/api/v1.0/questions'`

- Description: Creates a new question by submitting the question text, answer, category, and difficulty score.
- Request Arguments: 
  - `question` (string, required): The question text.
  - `answer` (string, required): The answer to the question.
  - `difficulty` (integer, required): Difficulty level of the question (1-5).
  - `category` (integer, required): The ID of the category to which the question belongs.
- Returns: Success value indicating whether the question was successfully created.
- Sample: `/api/v1.0/questions` (POST request)
  
  Input:
  ```json
  {
    "question": "What is the capital of France?",
    "answer": "Paris",
    "difficulty": 2,
    "category": 3
  }
  ```
  Response:
  ```json
  {
    "success": true
  }
  ```

`POST '/api/v1.0/questions/search'`

- Description: Searches for all questions that contain the search term as a substring in the question text.
- Request Arguments:
  - `search_term` (string, optional): The search term to be used for finding questions. Defaults to empty string.
- Returns: Success value, total number of matched questions, and the list of questions that match the search term.

- Sample: `/api/v1.0/questions/search?search_term=Indian` (POST request)
```json
{
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

`GET '/api/v1.0/categories/<int:category_id>/questions'`

- Description: Fetches all questions that belong to a specific category.
- Request Arguments:
  - `category_id` (integer, required): The ID of the category whose questions need to be fetched.
- Returns: Success value, total number of questions in the category, the list of questions, and the current category's name.

- Sample: `/api/v1.0/categories/1/questions`
```json
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

`POST '/api/v1.0/quizzes'`
- Description: Fetches a random question for a quiz game. The request should include a category and a list of previously asked questions. If category = 0, a random question from all categories is returned.

- Request Arguments:
  - `quiz_category` (integer, required): Contains the category ID (can be 0 to include all categories).
  - `previous_questions` (list, required): A list of IDs of the questions that have already been asked to avoid repeating them.
- Returns: Success value and a random question that matches the criteria (not in previous_questions and optionally filtered by category).
- Sample: `/api/v1.0/quizzes` (POST request)
  Input:
  ```json
  {
    "quiz_category":
    {
      "id": 1,
      "type": "Science"
    },
    "previous_questions": [20, 22]
  }
  ```
  Response:
  ```json
  {
    "question": {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    "success": true
  }
  ```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
