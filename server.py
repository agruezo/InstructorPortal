from flask_app import app
# DON'T FORGET TO IMPORT ALL YOUR CONTROLLERS!!!
from flask_app.controllers import topics, users, lessons

if __name__ == '__main__':
    app.run(debug=True)
from flask_app import app

from flask_app.controllers import users, topics, lessons

if __name__ == '__main__':
    app.run(debug=True)
