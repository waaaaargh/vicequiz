from os.path import join as opj
from os.path import dirname as opd

from flask import Flask, request, Response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.restful import Resource, Api

app = Flask(__name__, 
            template_folder=opj(opd(__file__), '..', 'templates'),
            static_folder=opj(opd(__file__), '..', 'static'))

import config
app.config.from_object(config)

db = SQLAlchemy(app)
from vicequiz.models import *

from vicequiz.views import *
