from flask import Flask, render_template, json, request, redirect, url_for, session, escape
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__) #, template_folder='./templates',static_folder='./static')
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'eivind.lund'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ETPh2289'
app.config['MYSQL_DATABASE_DB'] = 'skipark'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showProfile')
def showProfile():
    _name = escape(session['name'])
    _email = escape(session['email'])
    print("Open profile.html with name ", _name, " and email ", _email)
    return render_template('profile.html', name = _name, email = _email)

@app.route('/signUp',methods=['POST'])
def signUp():

    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    #print("Inne i SignUp() med Epost ", _email)
    # validate the received values

    conn = mysql.connect()
    cursor = conn.cursor()

    _hashed_password = generate_password_hash(_password)
    cursor.callproc('sp_createUser',(_name,_email,_hashed_password))

    session['name'] = _name
    session['email'] = _email

    data = cursor.fetchall()

    print("Before commit")
    if len(data) is 0:
        conn.commit()
        #return redirect(url_for('showProfile'))
        return json.dumps({'message':'User created successfully !'})
    else:
        return json.dumps({'error':str(data[0])})

    #if _name and _email and _password:
    #    return json.dumps({'html':'<span>All fields good !!</span>'})
    #else:
    #    return json.dumps({'html':'<span>Enter the required fields</span>'})


if __name__ == "__main__":
    app.run(debug=True)
