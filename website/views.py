from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from .models import User
from . import db
import json
import matplotlib.pyplot as plt
import numpy as np
import datetime
import pandas as pd
import plotly.express as px
import plotly.offline as pf

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        time = request.form.get('time')
        activity = request.form.get('activity')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id, time=time, activity=activity)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/activity', methods=['POST'])
def activity():
    return render_template("activity.html", user=current_user)


@views.route('/statistics')
@login_required
def statistics():
    months = []
    time_in_month = []
    for note in current_user.notes:
        if note.date.strftime("%B") + ' ' + note.date.strftime("%Y") not in months:
            months.append(note.date.strftime("%B") + ' ' + note.date.strftime("%Y"))
            time_in_month.append(note.time)
        else:
            time_in_month[months.index(note.date.strftime("%B") + ' ' + note.date.strftime("%Y"))] += note.time

    fig = px.histogram(x=months, y=time_in_month)
    fig.update_layout(
        title="Time in months",
        xaxis_title="Months",
        yaxis_title="Time in month",
    )
    fig.update_layout(bargap=0.2)
    div = pf.plot(fig, include_plotlyjs=False, output_type='div')

    days = []
    time_in_day = []
    for note in current_user.notes:
        days.append(note.date.strftime("%d") + ' ' + note.date.strftime("%B") + ' ' + note.date.strftime("%Y"))
        time_in_day.append(note.time)
    fig2 = px.histogram(x=days, y=time_in_day)
    fig2.update_layout(
        title="Time in days",
        xaxis_title='Days',
        yaxis_title='Time in a day',
    )
    fig2.update_layout(bargap=0.2)
    divvv = pf.plot(fig2, include_plotlyjs=False, output_type='div')

    return render_template("statistics.html", user=current_user, divv=div, divvv=divvv)


@views.route('/about')
def about():
    return render_template("about.html", user=current_user)


@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        email = request.form.get('email')
        if firstname != "":
            user = User.query.filter_by(id=current_user.id).first()
            user.first_name = firstname
            db.session.commit()
        if email != "":
            user = User.query.filter_by(id=current_user.id).first()
            user.email = email
            db.session.commit()
    return render_template("settings.html", user=current_user)


@views.route('/ranking')
def ranking():
    return render_template("ranking.html", userss=User.query, user=current_user)


@views.route('/maps')
def maps():
    return render_template("maps.html", user=current_user)

@views.route('/weather')
def weather():
    return render_template("weather.html", user=current_user)