This program is to create a multi-thread web server in python

Contents:
* Execution steps
* Available functions
* Reminder


Execution steps
--------------------------------------------
In order to execute, the user should first run the projectCode.py to execute the server.
Then, the user should be a line with "Listening on port 8000 ..."
to indicate it is ready to connect

The user can then find the desired file contents in the server through web access.


Available functions
----------------------------------------------
The program initial provides 3 types of file:
1. html file
2. txt file
3. png file

The user can input http://localhost:8000/desired_file to find the content in the server.
For instance, http://localhost:8000/helloworld.html will provide the contents of
the helloworld.html file.


Reminder
----------------------------------------------
There are a few reminders when using this program

1. This program only provides http get method, thus other methods like post & delete
   will cause 400 BAD REQUEST respond.
2. If the desired_file is not found in the server, the server will return 404 NOT FOUND
   to the user, the user can then enter another file or the correct name of the file.