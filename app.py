# -*- coding: utf-8 -*-
import json
import sys
import os
import hashlib
import plotly
import psycopg2
import pandas as pd
import numpy as np
import plotly.graph_objs as go

from flask import Flask, redirect, url_for, render_template, request, session, flash, Markup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_socketio import SocketIO, emit

from spending import SpendingHistory

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

socketio = SocketIO(app)
database = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='allow')

db = SQLAlchemy(app)

from models import *

# ======== Routing =========================================================== #


@app.route('/', methods=['GET', 'POST'])
def home():

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if 'email' in session:
            name = session['email'].split("@")[0]

            # df = pd.read_sql_query(
            #     "SELECT * FROM history WHERE email='%s'" % (session['email']), database)
            # 
            # if df.empty:
            #     return redirect(url_for('refresh'))
            # 
            # else:
            #     df['currentval'] = np.nan
            #     df['currentval'] = df['price'] - df['currentval']
            #     df.currentval = 1350 + df.price.cumsum()
            #     df.drop(columns=['date', 'time'], inplace=True)
            #     df.set_index('datetime', inplace=True)

            graphs = 0
            
            return render_template('home2.html', user=name, graphs=graphs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # login form
    if request.method == 'GET':
        return render_template('login.html')
    else:
        _email = request.form['email']
        _pass = hashlib.md5(request.form['pass'].encode())
        _pass = _pass.hexdigest()

        print(_email, _pass, request.form['email'], request.form['pass'])

        try:

            # hash the password. if the same, then login
            data = User.query.filter_by(email=_email, password=_pass).first()

            if data is not None:
                session['logged_in'] = True
                session['email'] = request.form['email']
                session['pass'] = request.form['pass']

                return redirect(url_for('home'))
            else:
                flash("Try again")
                return render_template('login.html')
        except:
            flash("Some error")
            return render_template("login.html")


@app.route('/signup', methods=['GET', 'POST'])
def register():
    # registration form
    if request.method == 'GET':
        return render_template('signup.html')

    try:
        if request.method == 'POST':

            password = hashlib.md5(request.form['pass'].encode())
            hashed_pass = password.hexdigest()
            new_user = User(
                name=request.form['name'], email=request.form['email'], password=hashed_pass)

            db.session.add(new_user)
            db.session.commit()

            session['email'] = request.form['email']
            session['pass'] = request.form['pass']

            flash("please login now")
            return render_template('login.html')

    except exc.IntegrityError:
        flash("Error")
        return render_template("signup.html")


@app.route('/info', methods=['GET', 'POST'])
def info():
    if session.get('logged_in'):
        return render_template('info.html', user=session['username'])
    else:
        return redirect(url_for('login'))


@app.route('/refresh', methods=['GET', 'POST'])
def refresh():

    SpendingHistory(session['email'], session['pass']).spending_history()
    # print(session['spending'])

    flash('GWorld Dining Dollars Data Updated!')

    return redirect(url_for('home'))


@app.route('/spending_graph', methods=['GET', 'POST'])
def spending_history():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
    else:

        initial_gworld = 1350

        df = pd.read_sql_query(
            "SELECT * FROM history WHERE email='%s'" % (session['email']), database)
        df['currentval'] = np.nan
        df['currentval'] = df['price'] - df['currentval']
        df.currentval = initial_gworld + df.price.cumsum()
        df.drop(columns=['date', 'time'], inplace=True)
        df.set_index('datetime', inplace=True)

        graph = dict(
            data=[go.Scatter(
                x=df.index,
                y=df['currentval']
            )],
            layout=dict(
                title='Total Spending By Day',
                yaxis=dict(
                    title="Spending"
                ),
                xaxis=dict(
                    title="Date"
                )
            )
        )
        graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
        # graphJSON = Markup(graphJSON)

        return render_template('spending_history.html', graphJSON=graphJSON)


@app.route('/logout/')
def logout():
    # logout form
    session['logged_in'] = False
    return redirect(url_for('home'))


@socketio.on('disconnect')
def disconnect_user():
    session.clear()
    session.pop('random-key', None)


#
#
# # -------- Settings ---------------------------------------------------------- #
# @app.route('/settings', methods=['GET', 'POST'])
# def settings():
#     if session.get('logged_in'):
#         if request.method == 'POST':
#             password = request.form['password']
#             if password != "":
#                 password = helpers.hash_password(password)
#             email = request.form['email']
#             helpers.change_user(password=password, email=email)
#             return json.dumps({'status': 'Saved'})
#         user = helpers.get_user()
#         return render_template('settings.html', user=user)
#     return redirect(url_for('login'))
#
#


# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
