# Dynamic-Project-Schedule-Revamped
Source code for Django backend of Dynamic Project Schedule App.

What does the app do?
After completion, the app should allow you to register your organisation using which you can get your managers and associates registered. Post registration manager can create a project and add or remove associates. Any associate or manager(working on the project) will be able to add comments about what they did for the day and everyone can see the total project progress. Screenshots of the final app is attached 

* The development of this app follows TDD(Test Driven Development) principles.

## Running the code
You can run the app using the docker command: docker-compose up
To run tests: docker-compose run dpsa sh -c "python manage.py test user"

## Main apps/modules:
1. Core: This module holds all the models. Also includes commands and test cases for testing models.

2. User: This module holds views for login/logout and other apis related to users. There are three types of users organisation, manager, and associate. Aside from this it also holds 
serializers, permissions, and tokens.

3. Project(Work in progress): Holds views and test cases related to project schedule.


### Permissions:
Each type of account/user has a set of permission with most permissions given to organisation and associate has the least number of permissions.

Organisation Permissions:
    'change_user',
    'add_user',
    'delete_user',
    'change_user',
    'add_organisationaccount',
    'view_organisationaccount',
    'change_organisationaccount',
    'delete_organisationaccount',
    'add_manageraccount',
    'view_manageraccount',
    'change_manageraccount',
    'delete_manageraccount',
    'add_associateaccount',
    'view_associateaccount',
    'change_associateaccount',
    'delete_associateaccount'

Manager Permissions: 
    'change_user',
    'add_user',
    'delete_user',
    'change_user',
    'add_manageraccount',
    'view_manageraccount',
    'change_manageraccount',
    'delete_manageraccount',
    'add_associateaccount',
    'view_associateaccount',
    'change_associateaccount',
    'delete_associateaccount'
    
Associate Permissions: 
    'change_user',
    'add_user',
    'delete_user',
    'change_user',
    'add_associateaccount',
    'view_associateaccount',
    'change_associateaccount',
    'delete_associateaccount'



