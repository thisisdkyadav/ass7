from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='my_database'
    )
    return connection

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        mobile_number = request.form['mobile_number']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                flash('User already exists!', 'error')
                return render_template('register.html')
        except:
            flash('An error occurred. Please try again.', 'error')
            return render_template('register.html')
        
        if not mobile_number.isdigit():
            flash('Mobile number must contain only digits', 'error')
            return render_template('register.html')
        if len(mobile_number) != 10:
            flash('Mobile number must be 10 digits long', 'error')
            return render_template('register.html')
        
        try:
            cursor.execute("INSERT INTO users (user_id, mobile_number, password) VALUES (%s, %s, %s)", (user_id, mobile_number, password))
        except:
            flash('An error occurred. Please try again.', 'error')
            return render_template('register.html')

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id = %s AND password = %s", (user_id, password))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            session['user_id'] = user_id
            return redirect(url_for('index'))
        else:
            flash('Invalid user id or password', 'error')
            return render_template('loginI. .html')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
