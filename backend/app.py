from flask import Flask, render_template, request, redirect, session
from database import db
from models import User, Post
from auth import create_user, verify_user
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "frontend", "templates"), static_folder=os.path.join(BASE_DIR, "frontend", "static"))
app.secret_key = "secret123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///insta.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = verify_user(request.form["username"], request.form["password"])
        if user:
            session["user_id"] = user.id
            return redirect("/feed")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        create_user(request.form["username"], request.form["password"])
        return redirect("/")
    return render_template("signup.html")

@app.route("/feed")
def feed():
    posts = Post.query.all()
    return render_template("feed.html", posts=posts)

@app.route("/create", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        post = post(image_url=request.form["image"], caption=request.form["caption"], user_id=session["user_id"])
        db.session.add(post)
        db.session.commit()
        return redirect("/feed")
    return render_template("create_post.html")

if __name__ == "__main__":
    app.run(debug=True)