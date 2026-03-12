from flask import Blueprint, render_template, request
from formulaone.extensions import db
from formulaone.models import FormulaOne

core_bp = Blueprint(
    "core",
    __name__,
    template_folder="templates"
)

@core_bp.route("/")
def index():

    page = request.args.get("page", 1, type=int)

    formulaones = db.paginate(
        db.select(FormulaOne),
        per_page=4,
        page=page
    )

    return render_template(
        "core/index.html",
        formulaones=formulaones
    )