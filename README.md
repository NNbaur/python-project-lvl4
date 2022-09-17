### Hexlet tests and linter status:
[![Actions Status](https://github.com/NNbaur/python-project-lvl4/workflows/hexlet-check/badge.svg)](https://github.com/NNbaur/python-project-lvl4/actions) [![Actions Status](https://github.com/NNbaur/python-project-lvl4/actions/workflows/github-action.yml/badge.svg)](https://github.com/NNbaur/python-project-lvl4/actions) <a href="https://codeclimate.com/github/NNbaur/python-project-lvl4/maintainability"><img src="https://api.codeclimate.com/v1/badges/a8670ff28326526a79b5/maintainability" /></a> <a href="https://codeclimate.com/github/NNbaur/python-project-lvl4/test_coverage"><img src="https://api.codeclimate.com/v1/badges/a8670ff28326526a79b5/test_coverage" /></a>

### Description
______
TaskManager is a small web application helping to deal with tasks. Designed for usage by a small team but also suitable for single person usage.

### Features
______

* Application is configured to work with PostgreSQL database;
* User authorization system;
* Only the user can edit and update himself;
* If the status/label is associated with at least one task, it cannot be deleted;
* Only logged users can view, create, update, delete statuses/labels;
* After authorization, the user can create a task for himself by specifying its name, description, status, executor from the list of registered users and, if necessary, select one or more labels from the list; 
* Only logged users can create, update and view tasks;
* Only the author can delete tasks;
* User can display a list of tasks with the ability to filter by status, author, executor, and labels;
* Available two languages of website: RU, EN.


### Local usage
______

You will need the following environment variables specified in your .env file:

* SECRET_KEY
* ACCESS_TOKEN
* DATABASE_URL
* DEBUG

Run the following commands to use locally:

```
$ git clone https://github.com/NNbaur/python-project-lvl4 
```
or

```
pip install git+https://github.com/NNbaur/python-project-lvl4.git
```

python manage.py runserver

The app will be available at http://127.0.0.1:8000/

### Task Manager
______

Avaiable at https://rocky-plateau-42258.herokuapp.com/