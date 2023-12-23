from faker import Faker
from flask import Flask, render_template, request

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

fake = Faker()
Faker.seed(5)

posts = [
    {
        "author": fake.name(),
        "title": f"post_{i}",
        "content": fake.sentence(),
        "date_posted": fake.date(),
    }
    for i in range(10)
]


@app.route("/")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/greeting")
def greeting():
    return render_template("user_input.html", title="Greeting")


@app.route("/greeting", methods=["POST"])
def greeting_post():
    text = request.form["text"]
    count = request.form["count"]
    return f"Hello {text.upper()}!<br>" * int(count)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
