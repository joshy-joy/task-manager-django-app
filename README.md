# Task Manager Application
Simple task management app developed in Django



## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Technologies
1. Django
2. MySql

## Installation

1. Create an environment and install the requirements from requirements.txt
```
pip install -r requirements.txt
```

#### Database setup
MySql Databse is used for storing and retriving data

1. Create a schema named 'task-manager' using MySql workbench
2. Migrate databses
```
python manage.py makemigrations
```

```
python manage.py migrate
```

