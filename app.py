from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Foydalanuvchi va admin ma'lumotlari
users = {'user1': {'password': 'password1', 'balance': 100}}  # Foydalanuvchi ro'yxati
admins = {'admin': {'password': 'adminpass'}}  # Admin ro'yxati

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Foydalanuvchi tekshirish
    if username in users and users[username]['password'] == password:
        session['username'] = username
        return redirect(url_for('dashboard'))

    # Admin tekshirish
    if username in admins and admins[username]['password'] == password:
        session['username'] = username
        return redirect(url_for('admin_dashboard'))

    return "Login failed. Check your credentials."

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    user = users[session['username']]
    return render_template('dashboard.html', user=user)

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' not in session or session['username'] not in admins:
        return redirect(url_for('index'))
    return render_template('admin_dashboard.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
