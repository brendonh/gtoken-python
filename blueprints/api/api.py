from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

api = Blueprint('api', __name__)

@api.route('/api/1/account/register')
def register():
    return ''
