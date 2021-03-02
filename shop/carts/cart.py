from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app


@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        pass
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)