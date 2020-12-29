# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

<a name="api-documentaton"></a>
## API Documentation

Here you can find information on all endpoints, which methods can be used with them and examples of the responses you can expect to receive.

### Available endpoints
                         
       Endpoints                              |  Allowed Methods |
                                              |------------------|
      /questions                              |  GET, POST       | 
      /questions/<int:question_id>            |  DELETE          |  
      /questions/search                       |  POST            | 
      /categories                             |  GET             |   
      /categories/<int:category_id>/questions |  GET             |     
      /quizzes                                |  POST            |

### Endpoint details

### 1. GET /questions
- Fetches a list of dictionaries, each dictionary being a question.
- Request arguments: None
- Returns: An object of the following format. Questions are found in paginated_questions and a list of categories in category_names
    {
        'success': True,
        'questions': paginated_questions,
        'total_questions': len(selection),
        'categories': category_names,
        'current_category': category_names
    }
- Error: If an out of range page is requested, a 404 error will occur.

### 2. POST /questions
- Inserts a new question into the database.
- Request arguments:
    1. **string** `question` (<span style="color:red">*</span>required)
    2. **string** `answer` (<span style="color:red">*</span>required)
    3. **string** `category` (<span style="color:red">*</span>required)
    4. **integer** `difficulty` (<span style="color:red">*</span>required)
- Returns: An object containing the id of the new question and the new set of paginated questions.
    {
        'success': True,
        'qid': new_trivia.id,
        'questions': paginated_questions,
        'total_questions': len(selection)
    }
- Errors: If you try to insert a question without all the correct fields, a 400 error will occur.

### 3. DELETE /questions/<int:question_id>  
- Deletes a question from the database, based on question id
- Request arguments:
   - **integer** `question_id`
- Returns: id of deleted question
    {
        'success': True,
        'deleted': question_id
    }
- Errors: If you try to delete a question with an invalid id, a 400 error will occur.

### 4. POST /questions/search 
- Searches for a given string within the database. Case sensitive.
- Request arguments:
    **string** `searchTerm` (<span style="color:red">*</span>required)
- Returns: List of dictionaries, each dict being a question which matches the given search term.
    {
        'success': True,
        'questions': paginated_questions,
        'total_questions': len(search_results),
        'current_category': 'TBC'
    }
- Errors: If you try to search without a search term, a 400 error will occur.

### 5. GET /categories  
- Fetches a list of all `categories`
- Request Arguments: None
- Returns: A list of all categories with category `type` as the values
    {
        'success': True,
        'categories': {category.id: category.type for category in selection}
    }
- Errors: If any methor other than 'GET' is sent to /categories, a 405 error will occur. 
        
### 6. GET /categories/<int:category_id>/questions
- Get all questions from a specific category
- Request arguments: **integer** `category_id` 
- Returns: List of paginated questions, each belonging to the requested category
    {
        'success': True,
        'questions': paginated_questions,
        'total_questions': len(selection),
        'categories': all_categories,
        'current_category': 'TBC'
    }
- Errors: If you request questions for an invalid category id, a 400 error will occur.

### 7. POST /quizzes
- Provides questions, so that the quiz can be played, based on chosed categories and prevously asked questions.
- Request arguments:
     1. **list** `previous_questions` (empty at start of quiz)
     2. **dict** `quiz_category` (optional) with keys:
        1.  **string** type
        2. **integer** id from category
- Returns: One question as a dictionary, selected at random from all the questions matching the given criteria.
    {
        'success': True,
        'question': quiz_question_rand
      }
- Errors: If you try to send the request without accompanying json, a 400 error will occur.

## Errors
-   400
    {
      'success': False,
      'error': 400,
      "message": "bad request"
    }
  
-   404
    {
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }

-   405
    {
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }

-   422
    {
      'success': False,
      'error': 422,
      'message': 'unprocessable entity'
    }

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```