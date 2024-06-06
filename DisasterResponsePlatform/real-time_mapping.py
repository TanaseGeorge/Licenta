from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
socketio = SocketIO(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sqluser1'
app.config['MYSQL_DB'] = 'disaster_response'

mysql = MySQL(app)


def get_data():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT * FROM volunteers')
    volunteers = cursor.fetchall()

    cursor.execute('SELECT * FROM resources')
    resources = cursor.fetchall()

    cursor.execute('SELECT * FROM incidents')
    incidents = cursor.fetchall()

    cursor.close()

    return {
        'volunteers': volunteers,
        'resources': resources,
        'incidents': incidents
    }


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('request_update')
def handle_request_update():
    data = get_data()
    socketio.emit('update_data', data)


if __name__ == '__main__':
    socketio.run(app, debug=True)
