# To Do Application
This application was made by adapting this [The Mega Flask Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-facelift)  by Miguel Grinberg and following the college tutorials.

A user is able to
- register
- login
- create a task
- update a task
- delete a task
- mark a task as completed
- view their current active tasks
## How to run the application?
### Run the following commands on the terminal:
```commandline
python -m venv venv
(Mac/Linux) source venv/bin/activate
(Windows) venv/scripts/activate
pip install -r requirements.txt
flask db upgrade
flask run
```


###  How to run the tests?
There are no tests currently