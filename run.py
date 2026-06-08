from app import create_app
from flask import redirect
from flask_login import current_user

app = create_app()


@app.route("/")
def home():

    if current_user.is_authenticated:
        return redirect("/dashboard/")

    return redirect("/auth/login")


if __name__ == "__main__":
    app.run(debug=True)