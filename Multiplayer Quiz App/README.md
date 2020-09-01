 Online Quiz Platform  

Authors:
Talin Taparia 
        
# Design and development of the application
The Application has some few main functions for the user. these are Register, Log In, Take Quiz, View Quiz Attempts, Admin.
Firstly, the user needs to register an account, the process for this to provide unique username and email and provide a password. There is verifaction of username and email, so that there is no discrepency in the database and it doesnt affect the user ability to use the app.
The user uses the credentials, provided on the register page to log in, moreover, to better the user interface a remember me button is added.
The logged in user has 3 possible options - quiz selector, profile and logout. In the profile page, the user can see their username, user email and the list of all the quizzes attempted. Moreover, in the quiz selector page, the user can see a list of all the available quizzes and select them and then moves on to take quiz page.
There is also a result graph which shows the total marks and the number os users who acheived that mark, this lets the users observe the result in a bell curve histogram.
In the admin section, with the administration account logged in, we can delete, create, upload the user detail and users results of the quiz. The admin also has the ability to create and delete quiz's and create and delete questions in that quiz.


# Instructions to launch the applictaion
  Within the project file
  execute:
  python3 project2.py
  And should be available to visit by browser using localhost:5000
# Dependencies (i.e. required modules)
  All dependencies can be found in the file requirements.txt,
  To install all required dependencies  write:
  pip install -r requirements.txt
# Testing
  unittest:
  python3 test.py
