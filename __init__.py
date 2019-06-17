import os

from flask import Flask, render_template, json, request

from flaskext.mysql import MySQL

from werkzeug import generate_password_hash, check_password_hash


def create_app(test_config=None):

    mysql = MySQL()

    # create and configure the app
    app = Flask(__name__)

    # MySQL configurations
    app.config['MYSQL_DATABASE_USER'] = 'mysql_dev'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'dev@123'
    app.config['MYSQL_DATABASE_DB'] = 'bucketlist'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)

    # all the routes are defined here
    @app.route("/")
    def main():
        return render_template('index.html')

    @app.route('/showSignUp')
    def showSignUp():
        return render_template('signup.html')

    @app.route('/signUp', methods=['POST', 'GET'])
    def signUp():

        try:
            # read the posted values from the UI
            _name = request.form['name']
            _email = request.form['email']
            _password = request.form['password']

            # validate the received values
            if _name and _email and _password:

                # All Good, let's call MySQL

                conn = mysql.connect()
                cursor = conn.cursor()
                _hashed_password = generate_password_hash(_password)
                cursor.callproc('sp_createUser',
                                (_name, _email, _hashed_password))
                data = cursor.fetchall()

                if len(data) is 0:
                    conn.commit()
                    return json.dumps(
                        {'message': 'User created successfully !'})
                else:
                    return json.dumps({'error': str(data[0])})
            else:
                return json.dumps(
                    {'html': '<span>Enter the required fields</span>'})

        except Exception as e:
            return json.dumps({'error': str(e)})
        finally:
            cursor.close()
            conn.close()

    return app
