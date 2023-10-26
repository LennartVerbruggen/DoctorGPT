from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap4
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = 'doctorgpt'
bootstrap = Bootstrap4
login_manager = LoginManager()
login_manager.init_app(app)


# Hardcoded users.
users = {'test1@t.be': {'password': 'test1', 'height': 180, 'weight': 75, 'age': 20}, 'zieke@t.be': {'password': 'griep', 'height': 160, 'weight': 95, 'age': 25}}

# Create a User class to represent users.
class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        user = User()
        user.id = user_id
        return user
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            user = User()
            user.id = email
            login_user(user)
            return redirect(url_for('start_chatting'))
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account')
@login_required
def account():
    email = current_user.get_id()
    user_info = users[email]  # Get user-specific data
    return render_template('account.html', user_info=user_info, email= email)

@app.route('/start_chatting')
def start_chatting():
    if UserMixin.is_authenticated:
        return redirect(url_for('login'))
    return 'Congrats you read the home page'

@app.route('/protected')
@login_required
def protected():
    return 'You are logged in as ' + UserMixin.get_id(current_user)


if __name__ == "__main__":
    app.run(debug=True)