# Tutor Me

Tutor Me is a web application used to connect tutors and students.

**Heroku service no longer available.

## Getting Started

In terminal, clone the repository to your local machine

Using HTTPS:
```
$ git clone https://github.com/uva-cs3240-s23/project-a-28.git
```
OR\
Using SSH:
```
$ git clone git@github.com:uva-cs3240-s23/project-a-28.git
```
## Setting up venv

It is recommended to install packages and run Python within a virtual environment.

Move into the /project-a-28 directory and run the following to create the venv (only run this once):
```
$ python3 -m venv venv
```
Everytime you work on the project, you'll want to activate the venv\
Do so with the following commands:\
\
On MacOS/Linux:
```
$ source venv/bin/activate
```
On Windows:
```
$ venv/Scripts/activate
```
## Installing packages

All required packages are managed using pip and requirements.txt.
Install all packages inside the venv
```
(venv)$ pip3 install -r requirements.txt
```
If you ever install new packages yourself, they can be added to the requirements.txt using the following:
```
(venv)$ pip3 freeze > requirements.txt
```

## Run Tutor Me locally
You should now be able to run the project locally:

```
(venv)$ python3 manage.py runserver
```

## Deployment
GitHub Actions is set to automatically deploy the app to Heroku when changes are pushed to branch ```dev```

## Internal Development Info

 ### Current models flow for auth
 - overwrote django User model with custom user model
 - custom User in login/models.py
 - User model stores email and is created by django-allauth when google authenticates
 - Tutor and Student models both have foreign key fields to User model
 - essentially, every Student and Tutor model has a User model field it points to that has auth/perms info

 ### Login/Signup flow
 - after user is authenticated with google
    - if new user, they are sent to /create endpoint
    - if exisiting, sent to respective dashboard endpoint (/student/dashboard or /tutor/dashboard)
- after this, login app is done, user stays on respective student or tutor app

## Authors

* **Wilson Zheng**
* **Oscar Lauth**
* **Malina Nelson**
Add names to file
