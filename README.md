# API Yamdb - reviews web application

API Yamdb web application collects user reviews for books, movies and music. It 
works only via API and has admin site. 

Users can publish reviews and leave their rate from 1 to 10. Users rates will
form average rating. Web application is not designed to store books, movies or
music. They are represented by name, year and short description. Users are 
also allowed to comment other users reviews.


## Technology stack
- Python 3.7
- Django 2.2.16
- Django Filter 21.1
- Django REST Framework 3.12.4
- Simple JWT 5.2.0


## ORM - models
В веб-приложении используются следующие модели:
- User - custom user model.
- Title - books, movies or music. 
- Genre - genres.
- Category - categories.
- Review - reviews.
- Comment - review comments.


## Roles and access rights
- Anonymous user - only read reviews and comments.
- Authenticated user - publish reviews and comments.
- Moderator - manage (edit or delete) reviews and comments.
- Administrator - manage all content and user roles. 
- Superuser - unlimited rights to manage the project.


## User registration
To create a new user:
- Send api request with email address and username.
- Receive email with confirmation code.
- Send api request with confirmation code to get authentication token.

Email with confirmation code is sent to a file which is stored in 
`api_yamdb/sent_emails/` directory. This functionality is implemented with 
django email backend `django.core.mail.backends.filebased.EmailBackend`. If you
would like the web application to send email to mailbox, please reconfigure
`settings.py` file.


## How to install and run
```
# Clone the repository
git clone https://github.com/evgeny81d/api_yamdb.git

# Go to the project directory
cd api_yamdb

# Create Python 3.7 virtual environment
python3.7 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt --upgrade pip

# Run migrations
python3 api_yamdb/manage.py migrate

# Create superuser
python3 api_yamdb/manage.py createsuperuser

# Run project on django development server
python3 api_yamdb/manage.py runserver
```

## Finally the web application is ready for use

 - [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/) - API documentation
 - [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) - admin site


## Security notice
The above instructions how to install and run the project have only
demonstration purpose and can be used on local host. 

If you would like to deploy the project on web server, please read the 
[documentation](https://docs.djangoproject.com/en/2.2/howto/deployment/).

 
## Authors
[Евгений Дериглазов](https://github.com/evgeny81d) |
Team lead. Custom User model, registration and authentication.

[Александр Гетманов](https://github.com/SelfGenius) | Developer. Administrator content.

[Герман Кабачков](https://github.com/tinkofoxil) | Developer. User content.
