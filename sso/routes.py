from flask import render_template
from init import app

from oauth.blueprint import register, token, tokeninfo


@app.errorhandler(404) 
def not_found(e):
    """ обработчик 404 ошибки """
    return render_template("404.html"), 404