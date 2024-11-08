# backend-messaging-system
This is a basic backend messaging system where two users can chat with each other


## Technology Stack
- Django
- Django REST Framework
- Django channels

### Setting Up For Local Development

-   Check that python 3 is installed:

    ```
    python --version
    >> Python 3.7.0
    ```

-   Install virtualenv or pipenv:

-   Clone the backend-messaging-system repo and cd into it:

    ```
    git clone https://github.com/ferrumie/backend-messaging-system.git
    ```
- Create a virtual enviroment
	```
	python3 -m venv env
	```
- Activate the virtual enviroment:
    - On Linux/Mac:
	    ```
	    source env/bin/activate
	    ```
    -  On Windows:
        ```
	   env/scripts/activate
	    ```
	Feel free to use other tools such as pipenv

-   Install dependencies from requirements.txt file:

    ```
    pip install -r requirements.txt
    ```


-   Apply migrations:

    ```
     run python manage.py migrate
    ```


*   Run the application with the command

    ```
    python manage.py runserver
    ```

* Once the server is running navigate to http://127.0.0.1:8000 to access the project

### Why did I implement this way?
Implementing with DRF, Django channels and SQLite provides a simple and flexible yet effective solution for developing a full featured chat backend. 
DRF provides structured way to handle user auth, and data serialization, django channels supports websockers, which basically makes real time communication possible, it also works well with JWT based auth. Django channels enables 
the creation of consumers and allows the exchange of messages in real time.
SQlite is lightweight, aand simple to use for a small sized project( since there is an instruction to not bother about scaling)

### What I couldn't complete
- I could only implement this for two users chat room, i could not complete the implementation for more than one users,
- My test coverage is super low and i could not complete the testing like i should, due to time limitation
- I could not add a simple UI to make the user experience better
- I could not add more sanity checks, validation for messages and attachment supports
- I couldn't complete the dockerization steps

### Idea for future Improvement
- Using PostgresSql for User and MongoDB for the messages
- Dockerizing the project
- Improving test coverage
- Improving the validation process
- Implementing a multiple user chat room
- Implementing a 'typing' feature
- Supporting Attachments, Voice Recordings
- Adding support for read receipts
- Chat Search support
- Message notifications 
- Message Deletion and edition
- User tags
- Location sharing
- message encryption
- message threads 
- message pinning
- AI recommendations
