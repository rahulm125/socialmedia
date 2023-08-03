from myapp import app
from myapp.models import db, WebSettings
from flask import redirect, url_for,render_template

########################################### providing index route ###########################################
@app.route('/')
def index():
    return redirect(url_for('users.signin'))


########################################### error 404 ###########################################
@app.errorhandler(404)
def page_not_found(e):
    detail = WebSettings.query.first()
    return render_template('404.html', detail=detail), 404

########################################### error 500 ###########################################
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

########################################### registering error handlers ###########################################
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_error)


########################################### server ###########################################
if __name__ == "__main__":
    app.run(debug=True)