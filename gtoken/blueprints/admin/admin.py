from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

@admin.route('/admin')
def index():
    return render_template('admin/index.htlml')
