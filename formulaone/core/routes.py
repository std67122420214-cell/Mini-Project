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
    search = request.args.get("search", "")

    query = db.select(FormulaOne)

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
        "core/index.html",
        title="Home Page",
        formulaones=formulaones
    )


@core_bp.route("/detail/<int:id>")
def detail(id):

    formulaone = db.get_or_404(FormulaOne, id)

    return render_template(
        "core/detail.html",
        title=formulaone.name,
        formulaone=formulaone
    )