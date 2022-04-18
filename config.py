# imporing libraries
from flaskext.mysql import MySQL
from app import app

# configuring database
sql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'

app.config['MYSQL_DATABASE_PASSWORD'] = 'fuzzy'

app.config['MYSQL_DATABASE_DB'] = 'quiz'

app.config['MYSQL_DATABASE_HOST'] = 'localhost'

sql.init_app(app)

