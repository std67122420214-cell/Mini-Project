from flask import Blueprint, render_template, request, flash, redirect, url_for
from formulaone.extensions import db
from formulaone.models import FormulaOne, Team
from flask_login import login_required, current_user

formulaone_bp = Blueprint("formulaone", __name__, template_folder="templates")


@formulaone_bp.route("/")
@login_required
def index():

    page = request.args.get("page", 1, type=int)

    query = db.select(FormulaOne).where(FormulaOne.user_id == current_user.id)

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
        number = request.form.get("number")
        world_championships = request.form.get("world_championships")
        nationality = request.form.get("nationality")
        img_url = request.form.get("img_url")

        team_ids = request.form.getlist("teams")

        selected_teams = []
        for id in team_ids:
            team = db.session.get(Team, id)
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