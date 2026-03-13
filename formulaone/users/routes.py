from flask import Blueprint, render_template, request, redirect, url_for, flash
from formulaone.extensions import db, bcrypt
from formulaone.models import User
from flask_login import login_user, logout_user, login_required, current_user

users_bp = Blueprint("users", __name__, template_folder="templates")


# Profile Page
@users_bp.route("/profile")
@login_required
def profile():
    return render_template("users/index.html", title="User Page")


# Register
@users_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("core.index"))

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        query = db.select(User).where(User.username == username)
        user = db.session.scalar(query)

        if user:
            flash("Username already exists!", "warning")
            return redirect(url_for("users.register"))

        query = db.select(User).where(User.email == email)
        user = db.session.scalar(query)

        if user:
            flash("Email already exists!", "warning")
            return redirect(url_for("users.register"))

        if password != confirm_password:
            flash("Password not match!", "warning")
            return redirect(url_for("users.register"))

        pwd_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(
            username=username,
            email=email,
            password=pwd_hash
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Register successful!", "success")
        return redirect(url_for("users.login"))

    return render_template("users/register.html", title="Register Page")


# Login
@users_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("core.index"))

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        query = db.select(User).where(User.username == username)
        user = db.session.scalar(query)

        if not user:
            flash("Username not found!", "warning")
            return redirect(url_for("users.login"))

        if not bcrypt.check_password_hash(user.password, password):
            flash("Password incorrect!", "warning")
            return redirect(url_for("users.login"))

        login_user(user)
        flash("Login successful!", "success")

        return redirect(url_for("core.index"))

    return render_template("users/login.html", title="Login Page")


# Logout
@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout successful!", "success")
    return redirect(url_for("core.index"))


# Change Password
@users_bp.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":

        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not bcrypt.check_password_hash(current_user.password, current_password):
            flash("Current password incorrect!", "warning")
            return redirect(url_for("users.change_password"))

        if new_password != confirm_password:
            flash("New password not match!", "warning")
            return redirect(url_for("users.change_password"))

        new_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")

        current_user.password = new_hash
        db.session.commit()

        flash("Password changed successfully!", "success")
        return redirect(url_for("users.profile"))

    return render_template(
        "users/change_password.html",
        title="Change Password"
    )