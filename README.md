# website_coffee_and_work

I created a web application "coffee and work". It shows different coffee places that also work as working places. Users can  explore cafes and share their experiences through reviews.
The web application allows users to view, add, and review cafes. Additionally, users can register for an account, log in/log out, and write reviews for cafes.

The website got deployed with render. You can find it here: https://coffe-and-work.onrender.com/

Components:
Flask: The web framework used for building the application, handling routes, and rendering templates.
SQLAlchemy: An ORM (Object-Relational Mapping) tool used for interacting with the database. It allows to work with Python objects instead of SQL statements directly.
Flask-Login: Provides user session management, including login, logout, and user authentication.
Flask-Bootstrap: Integration with the Bootstrap framework for styling and layout.
Flask-Gravatar: Integration with Gravatar to display user avatars based on their email addresses.

Database Models:
There are 3 database models: Cafe, User, and Review. These models define the structure of the database tables and their relationships.
Using Rest API the information about the coffee places is extracted from a database and shown on the website. 

Routes:
Various routes handle different functionalities of the application, such as user registration, login, logout, viewing cafes, adding cafes and writing reviews.

Forms:
The application uses WTForms for form validation and rendering. Forms are used for user registration, login, adding cafes and writing reviews.

HTML Templates:
HTML templates are used for rendering the user interface. Templates include pages for viewing cafes, individual cafes, user registration, login, adding cafes and writing reviews.



