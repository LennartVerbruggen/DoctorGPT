from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap4
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
import psycopg2

import os
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('.')
load_dotenv(dotenv_path=dotenv_path)

User_db = os.getenv('USER_DB')
Password_db = os.getenv('PASSWORD_DB')
Host_db = os.getenv('HOST_DB')
Port_db = os.getenv('PORT_DB')


# Default connection template, work in transactions
# conn = psycopg2.connect(database="postgres",  
#                         user="postgres", 
#                         password="t",  
#                         host="localhost",
#                         port="5432",
#                         options='-c search_path=doctorgpt')
# cur = conn.cursor()
#     cur.execute(''' Query schrijven => %s is parameter dat in de haken volgt''', (user_id))
#     data = cur.fetchone()
#     cur.close()
#     conn.close()


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
                        user=User_db, 
                        password=Password_db,  
                        host=Host_db,
                        port=Port_db,
                        options='-c search_path=doctorgpt')
        
    cur = conn.cursor()
    cur.execute('''SELECT * FROM users WHERE id = %s''', (user_id))
    data = cur.fetchone()
    cur.close()
    conn.close()
    if data is not None:
        user = User()
        user.id = user_id
        user.name = data[1]
        user.email = data[2]
        user.height = data[4]
        user.weight = data[5]
        user.birthdate = data[6]
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
                        user=User_db, 
                        password=Password_db,  
                        host=Host_db,
                        port=Port_db,
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
            user.name = data[1]
            user.email = data[2]
            user.height = data[4]
            user.weight = data[5]
            user.birthdate = data[6]
            login_user(user)    
            return redirect(url_for('start_chatting'))
            
    else:
        return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account')
@login_required
def account():
    user_id = current_user.get_id()
    user = load_user(user_id=user_id)
    return render_template('account.html', user_info=user)

@app.route("/createaccount", methods=['GET', 'POST'])
def createaccount():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        height = request.form['height']
        weight = request.form['weight']
        birthdate = request.form['birthdate']

        conn = psycopg2.connect(database="postgres",  
                            user=User_db, 
                            password=Password_db,  
                            host=Host_db,
                            port=Port_db,
                            options='-c search_path=doctorgpt')
        cur = conn.cursor()
        cur.execute(''' INSERT INTO users (name, email, password, height, weight, birthdate) VALUES (%s, %s, %s, %s, %s, %s)''', (name, email, password, height, weight, birthdate))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('login'))
    else:
        return render_template("create.html")

@app.route('/editaccount', methods=['POST'])
@login_required
def editaccount():

    conn = psycopg2.connect(database="postgres",  
                        user=User_db, 
                        password=Password_db,  
                        host=Host_db,
                        port=Port_db,
                        options='-c search_path=doctorgpt')
    cur = conn.cursor()

    user_id = current_user.get_id()
    updated_height = request.form['height']
    updated_weight = request.form['weight']
    updated_birthdate = request.form['age']

    cur.execute(''' UPDATE users SET height=%s, weight=%s, birthdate=%s WHERE id=%s''', (updated_height, updated_weight, updated_birthdate, user_id))
    conn.commit()
    cur.close()
    conn.close()

    user = load_user(user_id=user_id)

    return render_template('account.html', user_info=user)


@app.route('/deleteaccount', methods=['GET', 'POST'])
def deleteaccount():
    if request.method == 'POST':
        conn = psycopg2.connect(database="postgres",
                                user=User_db,
                                password=Password_db,
                                host=Host_db,
                                port=Port_db,
                                options='-c search_path=doctorgpt')
        cur = conn.cursor()

        user_id = current_user.get_id()
        anonimous_mail = user_id + 'anonimous@doctorgpt.be'
        cur.execute('''UPDATE users SET name=%s, email=%s, password=%s WHERE id=%s''', 
                    ('anonimous', anonimous_mail, 'anonimous', user_id))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('logout'))
    else:
        return render_template('confirmation.html')




@app.route('/start_chatting')
def start_chatting():
    # If the id of the current user is in my list of users, i want to get a message congrats otherwise i want to go to the log in page
    if current_user.is_authenticated:
        # Retrieve current user id
        user_id = current_user.get_id()

        # Build connection to db
        conn = psycopg2.connect(database="postgres",  
                        user=User_db, 
                        password=Password_db,  
                        host=Host_db,
                        port=Port_db,
                        options='-c search_path=doctorgpt')
        
        cur = conn.cursor()
        cur.execute('''SELECT sender, message FROM chat_messages WHERE user_id = %s''', (user_id))
        data = cur.fetchall()
        cur.close()
        conn.close()
        
        return render_template('chat.html', messages=data)
    else:
        return redirect(url_for('login'))
    

@app.route("/send", methods=['POST'])
def send_message():
    # If the user is logged he can send a message
    if current_user.is_authenticated:
        # Retrieve message from frontend and current user id
        userid = current_user.get_id()
        usermessage = request.form['message']

        botmessage = "That sucks for you!"

        # Build connection to db
        conn = psycopg2.connect(database="postgres",  
                        user=User_db, 
                        password=Password_db,  
                        host=Host_db,
                        port=Port_db,
                        options='-c search_path=doctorgpt')
        
        cur = conn.cursor()
        cur.execute(''' INSERT INTO chat_messages (user_id, sender ,message) VALUES (%s, %s, %s)''', (userid, 'user', usermessage))
        cur.execute(''' INSERT INTO chat_messages (user_id, sender ,message) VALUES (%s, %s, %s)''', (userid, 'bot', botmessage))
        conn.commit()
        cur.close()
        conn.close()

        # Trigger page reload
        return redirect(url_for('start_chatting'))
    else:
        return redirect(url_for('login'))

@app.route('/protected')
@login_required
def protected():
    return 'You are logged in as ' + UserMixin.get_id(current_user)


if __name__ == "__main__":
    app.run(debug=True)