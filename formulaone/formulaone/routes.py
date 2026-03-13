from flask import Blueprint, render_template, request, flash, redirect, url_for
from formulaone.extensions import db
from formulaone.models import FormulaOne, Team
from flask_login import login_required, current_user

formulaone_bp = Blueprint("formulaone", __name__, template_folder="templates")


@formulaone_bp.route("/")
@login_required
def index():

    page = request.args.get("page", 1, type=int)
    search = request.args.get("search")

    query = (
        db.select(FormulaOne)
        .where(FormulaOne.user_id == current_user.id)
        .order_by(FormulaOne.id.desc())
    )

    if search:
        query = query.where(
            FormulaOne.name.ilike(f"%{search}%")
        )

    formulaones = db.paginate(
        query,
        per_page=4,
        page=page
    )

    return render_template(
        "formulaone/index.html",
        title="Formula One Page",
        formulaones=formulaones
    )


@formulaone_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_formulaone():

    teams = db.session.scalars(db.select(Team)).all()

    if request.method == "POST":

        name = request.form.get("name")
        number = int(request.form.get("number") or 0)
        world_championships = int(request.form.get("world_championships") or 0)
        nationality = request.form.get("nationality")
        img_url = request.form.get("img_url")
        biography = request.form.get("biography")

        team_ids = request.form.getlist("teams")

        selected_teams = []
        for team_id in team_ids:
            team = db.session.get(Team, team_id)
            if team:
                selected_teams.append(team)

        existing = db.session.scalar(
            db.select(FormulaOne).where(FormulaOne.name == name)
        )

        if existing:
            flash(f"Driver {name} already exists!", "warning")
            return redirect(url_for("formulaone.new_formulaone"))

        new_driver = FormulaOne(
            name=name,
            number=number,
            world_championships=world_championships,
            nationality=nationality,
            img_url=img_url,
            biography=biography,
            user_id=current_user.id,
            teams=selected_teams,
        )

        db.session.add(new_driver)
        db.session.commit()

        flash("Driver added successfully!", "success")
        return redirect(url_for("formulaone.index"))

    return render_template(
        "formulaone/new_formulaone.html",
        title="New Driver",
        teams=teams
    )


# Edit Driver
@formulaone_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):

    driver = db.session.get(FormulaOne, id)

    if not driver or driver.user_id != current_user.id:
        flash("Driver not found!", "danger")
        return redirect(url_for("formulaone.index"))

    teams = db.session.scalars(db.select(Team)).all()

    if request.method == "POST":

        driver.name = request.form.get("name")
        driver.number = int(request.form.get("number") or 0)
        driver.world_championships = int(request.form.get("world_championships") or 0)
        driver.nationality = request.form.get("nationality")
        driver.img_url = request.form.get("img_url")
        driver.biography = request.form.get("biography")

        team_ids = request.form.getlist("teams")

        selected_teams = []
        for team_id in team_ids:
            team = db.session.get(Team, team_id)
            if team:
                selected_teams.append(team)

        driver.teams = selected_teams

        db.session.commit()

        flash("Driver updated successfully!", "success")
        return redirect(url_for("formulaone.index"))

    return render_template(
        "formulaone/edit_formulaone.html",
        title="Edit Driver",
        driver=driver,
        teams=teams
    )


# Delete Driver
@formulaone_bp.route("/delete/<int:id>")
@login_required
def delete(id):

    driver = db.session.get(FormulaOne, id)

    if not driver or driver.user_id != current_user.id:
        flash("Driver not found!", "danger")
        return redirect(url_for("formulaone.index"))

    db.session.delete(driver)
    db.session.commit()

    flash("Driver deleted successfully!", "success")

    return redirect(url_for("formulaone.index"))