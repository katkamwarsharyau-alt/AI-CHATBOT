from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# ---------------- APP ----------------
app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DATABASE ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- MODELS ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    user_msg = db.Column(db.String(500))
    bot_msg = db.Column(db.String(500))

# ---------------- HOME ----------------
@app.route('/')
def home():
    if "user" in session:
        return render_template("index.html", user=session["user"])
    return redirect(url_for("login"))

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            return "User already exists"

        hashed = generate_password_hash(password)

        new_user = User(username=username, password=hashed)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user" in session:
        return redirect(url_for("home"))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user"] = username
            return redirect(url_for("home"))

        return "Invalid username or password"

    return render_template("login.html")

# ---------------- CHAT ----------------
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    msg = data['message'].lower()

    if "hello" in msg:
        reply = "Hello 👋 Welcome!"
    elif "exam" in msg:
        reply = "📅 Exam: Maths-10 Apr, Physics-12 Apr, Chemistry-15 Apr"
    elif "placement" in msg:
        reply = "💼 Placement: TCS-20 June, Infosys-25 June, Wipro-28 June"
    else:
        reply = "❌ Sorry, I don't understand"

    new_chat = Chat(
        username=session.get("user"),
        user_msg=msg,
        bot_msg=reply
    )
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({"reply": reply})

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ---------------- RUN ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
import os
@app.route("/")
def home():
    return "AI Chatbot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
