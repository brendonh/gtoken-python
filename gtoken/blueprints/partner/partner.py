from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

partner = Blueprint('partner', __name__)

@partner.route('/partner/1/profile')
def profile():
    return ''
