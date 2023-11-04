from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap4
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
import psycopg2


# Default connection template, work in transactions
# conn = psycopg2.connect(database="postgres",  
#                         user="postgres", 
#                         password="t",  
#                         host="localhost",
#                         port="5432",
#                         options='-c search_path=doctorgpt')

app = Flask(__name__)
app.secret_key = 'doctorgpt'
bootstrap = Bootstrap4
login_manager = LoginManager()
login_manager.init_app(app)


# Hardcoded users.
users = {'test1@t.be': {'password': 'test1', 'height': 180, 'weight': 75, 'age': 20}, 'zieke@t.be': {'password': 'griep', 'height': 160, 'weight': 95, 'age': 25}}

# Hardcoded messages.
# messages = [
#     {"sender": "bot", "message": "Hello! How can I help you today?"},
#     {"sender": "user", "message": "I have a question about my account."},
#     {"sender": "bot", "message": "Sure, I'll do my best to assist you."},
#     {"sender": "user", "message": "How do I change my account password?"},
#     {"sender": "bot", "message": "To change your password, you can go to your account settings and follow the 'Change Password' option."},
#     {"sender": "user", "message": "Thank you for your help!"},
# ]


# Create a User class to represent users.
class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):

    conn = psycopg2.connect(database="postgres",  
                        user="postgres", 
                        password="t",  
                        host="localhost",
                        port="5432",
                        options='-c search_path=doctorgpt')
        
    cur = conn.cursor()
    cur.execute('''SELECT * FROM users WHERE id = %s''', (user_id))
    data = cur.fetchone()
    cur.close()
    conn.close()
    if data is not None:
        user = User()
        user.id = user_id
        # user.name = data[1]
        # user.email = data[2]
        # user.height = data[4]
        # user.weight = data[5]
        # user.birthdate = data[6]
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

        conn = psycopg2.connect(database="postgres",  
                        user="postgres", 
                        password="t",  
                        host="localhost",
                        port="5432",
                        options='-c search_path=doctorgpt')
        
        cur = conn.cursor()
        cur.execute('''SELECT * FROM users WHERE email = %s AND password = %s''', (email, password))
        data = cur.fetchone()
        cur.close()
        conn.close()
        print(data)

        if data is not None:
            user = User()
            user.id = data[0]
            # user.name = data[1]
            # user.email = data[2]
            # user.height = data[4]
            # user.weight = data[5]
            # user.birthdate = data[6]
            print(user.id)
            login_user(user)
            print(current_user.is_authenticated)
            return redirect(url_for('start_chatting'))
            
    else:
        print("test")
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

@app.route('/editaccount', methods=['POST'])
@login_required
def editaccount():
    user = users[current_user.get_id()]
    user['height'] = request.form['heigth']
    user['weight'] = request.form['weight']
    user['age'] = request.form['age']
    return render_template('account.html', user_info=user, email=current_user.get_id())

@app.route('/start_chatting')
def start_chatting():
    # If the id of the current user is in my list of users, i want to get a message congrats otherwise i want to go to the log in page
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        print("chat ophalen")
        conn = psycopg2.connect(database="postgres",  
                        user="postgres", 
                        password="t",  
                        host="localhost",
                        port="5432",
                        options='-c search_path=doctorgpt')
        
        cur = conn.cursor()
        cur.execute('''SELECT sender, message FROM chat_messages WHERE user_id = 2''')
        data = cur.fetchall()
        cur.close()
        conn.close()
        print(data)
        
        return render_template('chat.html', messages=data)
    else:
        return redirect(url_for('login'))

@app.route('/protected')
@login_required
def protected():
    return 'You are logged in as ' + UserMixin.get_id(current_user)


if __name__ == "__main__":
    app.run(debug=True)