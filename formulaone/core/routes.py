from flask import Blueprint, render_template, request
from formulaone.extensions import db
from formulaone.models import FormulaOne, Team
core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def index():
  page = request.args.get('page',type=int)
  formulaones = db.paginate(db.select(formulaone), per_page=4, page=page)
  return render_template('core/index.html',
                         title='Home Page',
                         formulaones=formulaones)

@core_bp.route('/<int:id>/detail')
def detail(id):
  formulaone = db.session.get(formulaone, id)
  return render_template('core/formulaone_detail.html',
                         title='formulaone Detail Page',
                         formulaone=formulaone)