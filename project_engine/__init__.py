from flask import Flask, session
from flask_mail import Mail
import yaml

with open(r'project_engine/utilities/default.yaml') as yaml_file:
    yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)

app = Flask(__name__)

# SqlAlchemy Database Configuration With Mysql
app.config.from_pyfile('../config.py')

app.config["MAIN_DICT"]["host"] = yaml_data["app"]["host"]
app.config["MAIN_DICT"]["port"] = yaml_data["app"]["port"]


# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'codescatter8980@gmail.com'
app.config['MAIL_PASSWORD'] = 'qrnvtobwftsippyd'
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Database configurations
# app.config["DATABASE"] = yaml_data["DATABASE"]
# app.config["ENGINE"] = yaml_data["ENGINE"]
# app.config["USERNAME"] = yaml_data["USERNAME"]
# app.config["PASSWORD"] = yaml_data["PASSWORD"]
# app.config["HOST"] = yaml_data["HOST"]
# app.config["PORT"] = yaml_data["PORT"]
#
# SQLALCHEMY_DATABASE_URI_MAIN = f'{app.config["ENGINE"]}://{app.config["USERNAME"]}:{app.config["PASSWORD"]}@{app.config["HOST"]}/{app.config["DATABASE"]}'

