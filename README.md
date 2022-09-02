## SimpleForum
This project is the backend service for forum application. Its hierarchy is as follows:
- Threads - the main structure, they should behave like groups of topics (e.g. Pets, Medicine...)
- Posts - Posts behave like topics, they can be created inside the thread (e.g. How can I ...?)
- Comments - Comments exist inside posts, visually, they follow the post, but are bound to the post structure

Service should implement authentication mechanism. It consists of:
- Registration - Simple registration using username and password
- Login - Simple login method using username and password
- Logout - Simple logout method, removes user session


### Project structure
Every group of endpoints is separated by directory. Every directory includes these files:
- `__init__.py` - Can be used for declaring external imports, but still optional
- `endpoints.py` - Endpoints for specific group, along with their API router
- `helpers.py` - Can be used for any additional functions, you can also create specific file if necessary, for functions
- `schemas.py` - Used for **pydantic** models, which are used for validation and consistency. Every endpoint that needs 
more than one argument to function properly should use a validation model.

You should follow this structure, but any changes are welcome, if you find them necessary.


### Authentication
Authentication mechanism is as follows:
Registration is going through username and password, password should be validated, to be strong enough (At least one uppercase letter, at least one special character, at least one number, length minimum of 8 characters).
Login, if correct, should set JWT cookie. 

Data that should be inside of JWT:

```json lines
{
  "sub": "112", // ID of the user in the system
  "iat": 1662032329, // Token creation time
  "exp": 1662035929, // Token expiration timestamp (Must be integer, use jwt datetime_to_int)
  "data": {} // If there is anything that can be stored in token, that can be used to implement some endpoints
}
```

JWT should be sent using setcookie response method (FastAPI documentation provides that). Field for the cookie can be named auth_token, sess_token etc.
Expiration time is 1 hour.

Also, signature needs to be checked, and all JWTs sent need to be signed. If the token expires, session expires as well (remove cookie, or set cookie to None, or null). Then user needs to login again. (Use middleware for checking the token)
Logout functions the same as expiration, removing the token from the cookies.


### Threads, posts, comments
Every node in the hierarchy can be created by any user. When created, any of the nodes created by the specific user can only be updated by the same user. 

#### Threads

Thread needs to contain title, datetime of creation, datetime of update, some information of the user that created it (e.g. Link to their avatar or None, username). 
Datetime of the update is updated any time the post or comment is created or updated, as well as when the thread is updated.

Example of the thread:
```json
{
  "title": "Some thread title",
  "dtCreated": "2022-01-01T00:00:00.000",
  "dtUpdated": "2022-01-01T00:00:00.000",
  "user": {
    "username": "somebody133",
    "avatar": "https://example.com/avatar.jpg",
    "signature": "Some signature"
  }
}
```
#### Posts

Posts function similarly to threads, they should contain the same things as threads (Title, user data, datetime of creation, datetime of update).
They must also contain text content, with a size of minimum 50 characters, and optionally contain attachments (Attachments are uploaded as files, there can be multiple attachments on the same post).

Example of the post without attachments:

```json
{
  "title": "Some post",
  "dtCreated": "2022-01-01T00:00:00.000",
  "dtUpdated": "2022-01-01T00:00:00.000",
  "user": {
    "username": "somebody133",
    "avatar": "https://example.com/avatar.jpg",
    "signature": "Some signature"
  },
  "content": "This is some cool post, ....",
  "attachments": {}
}
```

Example of the post with attachments:

```json
{
  "title": "Some post",
  "dtCreated": "2022-01-01T00:00:00.000",
  "dtUpdated": "2022-01-01T00:00:00.000",
  "user": {
    "username": "somebody133",
    "avatar": "https://example.com/avatar.jpg",
    "signature": "Some signature"
  },
  "content": "This is some cool post with attachments, here is one attachment: ~[1123~], and there is also another one ~[1124~]",
  "attachments": {
    "1123": "https://example.com/attachment1.jpg",
    "1124": "https://example.com/attachment2.jpg"
  }
}
```

Datetime of the post update is updated any time the comment is created or updated, as well as when the post is updated.

#### Comments

Comments are simplified posts, they cannot contain attachments, only text.
```json
{
  "title": "Some comment",
  "dtCreated": "2022-01-01T00:00:00.000",
  "dtUpdated": "2022-01-01T00:00:00.000",
  "user": {
    "username": "somebody133",
    "avatar": "https://example.com/avatar.jpg",
    "signature": "Very cool signature"
  },
  "content": "This is a simple comment to a post"
}
```

### Users
User can add, update and delete their avatar (Through image upload), and also add, update and delete their signature.

User can also create and read messages. Messaging needs to be implemented using AMQP protocol. Documentation and general know-how is described in separate tasks.

#### Messages

Messages are the way of communication between users. Messages are temporary, and can only be received once (Optionally, you can store them). They are sent to the RabbitMQ, to user specific queue.
When the user wants to check their messages, a new connection to RabbitMQ is created, and service should then retrieve the messages that are in the queue.

Message example:
```json
{
  "dtCreated": "2022-01-01T00:00:00.000",
  "content": "Hello my friend, how are you today?",
  "user": {
    "username": "someotheruser",
    "avatar": "https://example.com/someotheravatar.jpg",
    "signature": "Very cool signature"
  }
}
```

All the libraries needed to complete this project are in requirements.txt

Additional services that should be used:
- PostgreSQL (DB solution)
- RabbitMQ (For messaging part)

Optional services:
- Redis
- Memcached

Libraries that should be used for project implementation:
- `fastapi` - Used for creating REST API (https://fastapi.tiangolo.com/)
- `SQLAlchemy` - Used as PostgreSQL tool and ORM (https://docs.sqlalchemy.org/en/14/)
- `pydantic` - Used for validating input and output data models (https://pydantic-docs.helpmanual.io/)
- `pyhumps` - Library used for a lot of string conversions (https://humps.readthedocs.io/en/latest/)
- `uvicorn` - ASGI web server implementation, similar to gunicorn, hypercorn etc. (https://www.uvicorn.org/)
- `pika` - RabbitMQ adapter, that fully supports AMQP 0-9-1 protocol (https://pika.readthedocs.io/en/stable/index.html)
- `aio-pika` - AsyncIO implementation of pika, can be used in async endpoints, preferred for messaging implementation (https://aio-pika.readthedocs.io/en/latest/)
- `alembic` - DB migration tool, specifically designed to be used with SQLAlchemy (https://alembic.sqlalchemy.org/en/latest/)
- `psycopg2` - DB driver for PostgreSQL (https://www.psycopg.org/docs/)
- `python-dotenv` - Library that supports reading the data from `.env` file, and adds it to `os.env`, to be used in application (https://github.com/theskumar/python-dotenv)
- `redis` - Redis python interface (https://github.com/redis/redis-py)
- `requests` - HTTP Library for python, used for FastAPI TestClient (https://requests.readthedocs.io/en/latest/)

Any additional libraries are not necessary for the project completion, but if they make the job of finishing easier, just note them in your repository, and what are they used for.

### Assignment workflow
To start working on this assignment, you need GitLab account. Assuming that you can view this repository, we are on track.

You should fork this project, and add emails for contact to your project, so we could track the progress,
and assist you with any questions you might have. Assignment needs to follow basic git flow, 
commit messages should have standardized structure. Base commit message must not be larger than 100 characters, 
and any additional work should be added as an additional comment.   

**Time to finish the assignment is 7 days, starting from the day you have received the assignment**.
Commits done after that time will not be included in assignment review.
If you need more time, you are free to contact us, and we will review
the progress you have made during that time, and notify you with the new due date.

### Additional implementation commentary
All services must be dockerized, in order for application to work properly. Only app port needs to be exposed on host, rest should work without exposing ports from docker network. For testing purposes, you can expose ports of external services, either for checking data in the database, or accessing RabbitMQ management application. Proper dependencies need to be in place 
in docker-compose.yaml. https://docs.docker.com/compose/compose-file/

Migrations need to be created through alembic CLI, for reference use https://alembic.sqlalchemy.org/en/latest/

For initialization process, database needs migration, and also needs to be created on the server, if it does not exist.
Initialization process can also be done while building the application, although preferred way is through init build process.

Some integration tests need to be implemented. Assignments for these are located in `tests` directory.

All assignments be marked with TODO comment. Functionalities like authentication middleware implementation, or best use case for dependency injection, 
are not described, as those are accounted as problem-solving skills. Database models are also not described, as this README provides 
enough information, and are considered as DB design problems. Overall application functionality will be assessed as general technical and problem-solving skills.

Preferred IDE to use is PyCharm, as it has multiple features, like integrated TODO tool, proper test runner, and proper virtual environment management.
PYTHONPATH should be root of this project, this is important for running tests, and also application.

**Have fun, and good luck. For any technical questions, feel free to contact us through the provided contact information.**
