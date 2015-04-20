from datetime import datetime
from flask import render_template, redirect, url_for, request
from flask.ext.login import login_required, current_user
from app import db
from app.models import Bean, Roaster, Roast
from .forms import BeanForm, RoasterForm, RoastForm, flash_form_errors
from . import roast


@roast.route('/', methods=['GET'])
@login_required
def index():
    roasts = Roast.query.filter_by(user_id=current_user.id).order_by(Roast.roast_datetime.desc()).all()
    beans = Bean.query.filter_by(user_id=current_user.id).all()
    roasters = Roaster.query.filter_by(user_id=current_user.id).all()
    return render_template('roast/index.html', roasts=roasts, beans=beans, roasters=roasters)


@roast.route('/beans', methods=['GET'])
@login_required
def bean_list():
    beans = Bean.query.filter_by(user_id=current_user.id).all()
    return render_template('roast/bean_list.html', beans=beans)


@roast.route('/beans/new', methods=['GET', 'POST'])
@login_required
def bean_new():
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
            return redirect(url_for('roast.bean_detail', bean_id=bean.id))
        else:
            flash_form_errors(form)
    return render_template('roast/bean_new.html', form=form)


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
    return render_template('roast/bean_edit.html', form=form, bean=bean)


@roast.route('/roasters', methods=['GET'])
@login_required
def roaster_list():
    roasters = Roaster.query.filter_by(user_id=current_user.id).all()
    return render_template('roast/roaster_list.html', roasters=roasters)

@roast.route('/roasters/new', methods=['GET', 'POST'])
@login_required
def roaster_new():
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
            return redirect(url_for('roast.roaster_detail', roaster_id=roaster.id))
        else:
            flash_form_errors(form)
    return render_template('roast/roaster_new.html', form=form)


@roast.route('/roasters/<int:roaster_id>', methods=['GET'])
@login_required
def roaster_detail(roaster_id):
    roaster = Roaster.query.get(roaster_id)
    return render_template('roast/roaster_detail.html', roaster=roaster)


@roast.route('/roasters/edit/<int:roaster_id>', methods=['GET', 'POST'])
@login_required
def roaster_edit(roaster_id):
    if request.method == 'POST':
        form = RoasterForm(request.form)
        if form.validate_on_submit():
            roaster = Roaster.query.get(roaster_id)
            roaster.name = form.name.data
            roaster.description = form.description.data
            db.session.add(roaster)
            db.session.commit()
            return redirect(url_for('roast.roaster_detail', roaster_id=roaster.id))
        else:
            flash_form_errors(form)
    roaster = Roaster.query.get(roaster_id)
    form = RoasterForm(obj=roaster)
    return render_template('roast/roaster_edit.html', form=form, roaster=roaster)


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

@roast.route('/roasts/edit/<int:roast_id>', methods=['GET', 'POST'])
@login_required
def roast_edit(roast_id):
    form = RoastForm(request.form)
    beans = Bean.query.filter_by(user_id=current_user.id).all()
    roasters = Roaster.query.filter_by(user_id=current_user.id).all()
    form.bean.choices = [(str(bean.id), bean.name) for bean in beans]
    form.roaster.choices = [(str(roaster.id), roaster.name) for roaster in roasters]

    if request.method == 'POST':
        if form.validate_on_submit():
            roast = Roast.query.get(roast_id)
            roast.bean_id = form.bean.data
            roast.roaster_id = form.roaster.data
            roast.start_time = form.start_time.data
            roast.start_temp = form.start_temp.data
            roast.start_weight = form.start_weight.data
            roast.fc_start_time = form.fc_start_time.data
            roast.fc_start_temp = form.fc_start_temp.data
            roast.fc_end_time = form.fc_end_time.data
            roast.fc_end_temp = form.fc_end_temp.data
            roast.sc_start_time = form.sc_start_time.data
            roast.sc_start_temp = form.sc_start_temp.data
            roast.sc_end_time = form.sc_end_time.data
            roast.sc_end_temp = form.sc_end_temp.data
            roast.end_time = form.end_time.data
            roast.end_temp = form.end_temp.data
            roast.end_weight = form.end_weight.data
            roast.roast_datetime = datetime.strptime(form.roast_datetime.data, "%m/%d/%Y %I:%M:%S %p")
            roast.notes = form.notes.data
            db.session.commit()
            return redirect(url_for('roast.roast_detail', roast_id=roast.id))
        else:
            flash_form_errors(form)
    if request.method == 'GET':
        roast = Roast.query.get(roast_id)
        form = RoastForm(obj=roast)
        form.roast_datetime.data = roast.formatted_datetime
        form.bean.choices = [(str(bean.id), bean.name) for bean in beans]
        form.roaster.choices = [(str(roaster.id), roaster.name) for roaster in roasters]

    return render_template('roast/roast_edit.html', form=form, beans=beans, roasters=roasters, roast=roast)




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
            roast_datetime = datetime.strptime(form.roast_datetime.data, "%m/%d/%Y %I:%M:%S %p")
            roast = Roast(
                user_id=current_user.id,
                bean_id=form.bean.data,
                roaster_id=form.roaster.data,
                start_time=form.start_time.data,
                start_temp=form.start_temp.data,
                start_weight=form.start_weight.data,
                fc_start_time=form.fc_start_time.data,
                fc_start_temp=form.fc_start_temp.data,
                fc_end_time=form.fc_end_time.data,
                fc_end_temp=form.fc_end_temp.data,
                sc_start_time=form.sc_start_time.data,
                sc_start_temp=form.sc_start_temp.data,
                sc_end_time=form.sc_end_time.data,
                sc_end_temp=form.sc_end_temp.data,
                end_time=form.end_time.data,
                end_temp=form.end_temp.data,
                end_weight=form.end_weight.data,
                roast_datetime=roast_datetime,
                notes=form.notes.data,
            )
            db.session.add(roast)
            db.session.commit()
            return redirect(url_for('roast.roast_detail', roast_id=roast.id))
        else:
            flash_form_errors(form)
    return render_template('roast/roast_new.html', form=form, beans=beans, roasters=roasters)

