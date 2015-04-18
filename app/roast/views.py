from datetime import datetime
from flask import render_template, redirect, url_for, request
from flask.ext.login import login_required, current_user
from app import db
from app.models import Bean, Roaster, Roast
from .forms import BeanForm, RoasterForm, RoastForm, flash_form_errors
from .utils import convert_times_to_second_diff
from . import roast


@roast.route('/', methods=['GET'])
@login_required
def index():
    roasts = Roast.query.filter_by(user_id=current_user.id)
    return render_template('roast/index.html', roasts=roasts)


@roast.route('/beans', methods=['GET', 'POST'])
@login_required
def beans():
    form = BeanForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            bean = Bean(
                name=form.name.data,
                description=form.description.data,
                user_id=current_user.id,
            )
            db.session.add(bean)
            db.session.commit()
            return redirect(url_for('roast.beans'))
        else:
            flash_form_errors(form)
    beans = Bean.query.filter_by(user_id=current_user.id).all()
    return render_template('roast/beans.html', beans=beans, form=form)


@roast.route('/beans/<int:bean_id>', methods=['GET'])
@login_required
def bean_detail(bean_id):
    bean = Bean.query.get(bean_id)
    return render_template('roast/bean_detail.html', bean=bean)

@roast.route('/beans/edit/<int:bean_id>', methods=['GET', 'POST'])
@login_required
def edit_bean(bean_id):
    if request.method == 'POST':
        form = BeanForm(request.form)
        if form.validate_on_submit():
            bean = Bean.query.get(bean_id)
            bean.name = form.name.data
            bean.description = form.description.data
            db.session.add(bean)
            db.session.commit()
            return redirect(url_for('roast.bean_detail', bean_id=bean.id))
        else:
            flash_form_errors(form)
    bean = Bean.query.get(bean_id)
    form = BeanForm(obj=bean)
    return render_template('roast/edit_bean.html', form=form, bean=bean)


@roast.route('/roasters', methods=['GET', 'POST'])
@login_required
def roasters():
    form = RoasterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            roaster = Roaster(
                name=form.name.data,
                description=form.description.data,
                user_id=current_user.id,
            )
            db.session.add(roaster)
            db.session.commit()
            return redirect(url_for('roast.roasters'))
        else:
            flash_form_errors(form)
    roasters = Roaster.query.filter_by(user_id=current_user.id).all()
    return render_template('roast/roasters.html', roasters=roasters, form=form)


@roast.route('/roasters/<int:roaster_id>', methods=['GET'])
@login_required
def roaster_detail(roaster_id):
    roaster = Roaster.query.get(roaster_id)
    return render_template('roast/roaster_detail.html', roaster=roaster)


@roast.route('/roasters/edit/<int:roaster_id>', methods=['GET', 'POST'])
@login_required
def edit_roaster(roaster_id):
    if request.method == 'POST':
        form = RoasterForm(request.form)
        if form.validate_on_submit():
            roaster = Roaster.query.get(roaster_id)
            roaster.name = form.name.data
            roaster.description = form.description.data
            db.session.add(roaster)
            db.session.commit()
            return redirect(url_for('roast.beans'))
        else:
            flash_form_errors(form)
    roaster = Roaster.query.get(roaster_id)
    form = RoasterForm(obj=roaster)
    return render_template('roast/edit_roaster.html', form=form, roaster=roaster)


@roast.route('/roasts', methods=['GET', 'POST'])
@login_required
def roast_list():
    roasts = Roast.query.filter_by(user_id=current_user.id).all()
    return render_template('roast/roast_list.html', roasts=roasts)


@roast.route('/roasts/<int:roast_id>', methods=['GET'])
@login_required
def roast_detail(roast_id):
    roast = Roast.query.get(roast_id)
    return render_template('roast/roast_detail.html', roast=roast)


@roast.route('/roasts/new', methods=['GET', 'POST'])
@login_required
def roast_new():
    form = RoastForm(request.form)
    beans = Bean.query.filter_by(user_id=current_user.id).all()
    roasters = Roaster.query.filter_by(user_id=current_user.id).all()
    form.bean.choices = [(str(bean.id), bean.name) for bean in beans]
    form.roaster.choices = [(str(roaster.id), roaster.name) for roaster in roasters]

    if request.method == 'POST':
        if form.validate_on_submit():
            start_time = form.start_time.data
            roast_datetime = datetime.strptime(form.roast_datetime.data, "%m/%d/%Y %I:%M:%S %p")
            roast = Roast(
                user_id=current_user.id,
                bean_id=form.bean.data,
                roaster_id=form.roaster.data,
                start_time=0,
                start_temp=form.start_temp.data,
                start_weight=form.start_weight.data,
                first_crack_start_time=convert_times_to_second_diff(start_time, form.fc_start_time.data),
                first_crack_start_temp=form.fc_start_temp.data,
                first_crack_end_time=convert_times_to_second_diff(start_time, form.fc_end_time.data),
                first_crack_end_temp=form.fc_end_temp.data,
                second_crack_start_time=convert_times_to_second_diff(start_time, form.sc_start_time.data),
                second_crack_start_temp=form.sc_start_temp.data,
                second_crack_end_time=convert_times_to_second_diff(start_time, form.sc_end_time.data) if form.sc_end_time.data else None,
                second_crack_end_temp=form.sc_end_temp.data,
                end_time=convert_times_to_second_diff(start_time, form.end_time.data) if form.end_time.data else None,
                end_temp=form.end_temp.data,
                end_weight=form.end_weight.data,
                roast_datetime=roast_datetime,
                notes=form.notes.data,
            )
            db.session.add(roast)
            db.session.commit()
            return redirect(url_for('roast.index'))
        else:
            flash_form_errors(form)
    return render_template('roast/roast_new.html', form=form, beans=beans, roasters=roasters)

