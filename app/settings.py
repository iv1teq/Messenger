import flask
import os
import flask_socketio

app = flask.Flask(__name__,
                instance_path=os.path.abspath(os.path.join(__file__, "..", "instance"))
                )  
socket = flask_socketio.SocketIO(app = app)
