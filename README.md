## SimpleForum
This project is the backend service for forum application. Its hierarchy is as follows:
- Threads - the main structure, they should behave like groups of topics (e.g. Pets, Medicine...)
- Posts - Posts behave like topics, they can be created inside the thread (e.g. How can I ...?)
- Comments - Comments exist inside posts, visually, they follow the post, but are bound to the post structure

Service should implement basic authentication mechanism. It consists of:
- Registration - Simple registration using username and password
- Login - Simple login method using username and password
- Logout - Simple logout method, removes user session

### Authentication

Authentication mechanism is as follows:
Registration is going through username and password, password should be validated, to be strong enough (At least one uppercase letter, at least one special character, at least one number, length minimum of 8 characters).
Login, if correct, should set JWT cookie. 

Data that should be inside of JWT:

```json
{
  "sub": "112", // ID of the user in the system
  "iat": 1662032329, // Token creation time
  "exp": 1662035929 // Token expiration timestamp (Must be integer, use jwt datetime_to_int)
  "data": {} // If there is anything that can be stored in token, that can be used to implement some of the endpoints
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
User can add, update and delete their avatar (Through image upload), and also add, update and delete their signature

User can also create and read messages.

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



### Additional implementation commentary
For all of the services that need to run, in order for application to work properly, must be dockerized.

Have fun, and good luck. For any questions, feel free to contact us through email we provided.
