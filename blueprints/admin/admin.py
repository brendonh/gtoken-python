from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

admin = Blueprint('admin', __name__)

@admin.route('/admin')
def index():
    return render_template('admin/index.htlml')
