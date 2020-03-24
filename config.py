

import os
import sys
from flask_sqlalchemy import SQLAlchemy




# dev_db='mysql+pymysql://root:root@localhost/test'

dev_db ='mysql+pymysql://root:root@localhost/test'



SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI',dev_db)

DEBUG = True


SECRET_KEY = os.urandom(24)

SQLALCHEMY_TRACK_MODIFICATIONS=False

