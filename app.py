from flask import Flask
from flask import render_template
from databaseApp.database import db_session, init_db
import datetime, json
from jinja2 import Environment, PackageLoader
from sqlalchemy import func,exc

app = Flask(__name__)
if __name__ == '__main__':
	app.run(debug = True,host='0.0.0.0')
