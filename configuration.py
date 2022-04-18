from flaskext.mysql import MySQL
from application import application
sql = MySQL()

application.config["MYSQL_DATABASE_USER"] = "root"
application.config["MYSQL_DATABASE_PASSWORD"] = "fuzzy"
application.config["MYSQL_DATABASE_HOST"] = "localhost"
application.config["MYSQL_DATABASE_DB"] = "quiz"
sql.init_app(application)
