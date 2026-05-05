import flask
import os

app = flask.Flask(
    __name__,
    instance_path=os.path.abspath(os.path.join(__file__, "..", "instance"))
    )