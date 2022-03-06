import os

from flask import Flask, Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import create_engine
from werkzeug import secure_filename
from datetime import datetime

from .forms import AdminRegistrationForm, LogInForm
from candidate.forms import CandidateRegistrationForm
from models import AdminDetail, CandidateDetail, UserQuestionSet, QuestionSet
from config import Config
from api_server import bcrypt, db
from config import Config

admin = Blueprint('admin', __name__, url_prefix="/admin")


@admin.route("/registration", methods=['GET', 'POST'])
def registration():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data.strip()).decode('utf-8')
        detail_entry = AdminDetail(fullname=form.full_name.data, email_id=form.email_id.data.strip(),
                                   mobile_no=form.mobile_no.data, password=hashed_password)
        db.session.add(detail_entry)
        db.session.commit()
        return redirect(url_for('admin.login'))
    return render_template('admin_registration.html', form=form)


@admin.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.start_test'))

    form = LogInForm()
    if form.validate_on_submit():
        user = AdminDetail.query.filter_by(email_id=form.email_id.data.strip()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data.strip()):
            login_user(user, form.remember.data)
            flash('Login Successful!!', 'success')
            return redirect(request.args.get('next') or url_for('admin.dashboard'))
        else:
            flash('Invalid Email Id or Password', 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@admin.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


@login_required
@admin.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')


@login_required
@admin.route("/user_list")
def user_list():
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login'))
    candidates = CandidateDetail.query.all()
    return render_template('user_list.html', candidates=candidates)


@login_required
@admin.route("/user_status/<int:id>")
def user_status(id):
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login'))

    candidate = CandidateDetail.query.filter_by(id=id).first()
    if candidate.enable:
        candidate.enable = False
    else:
        candidate.enable = True
    db.session.commit()
    return redirect(url_for('admin.user_list'))


@login_required
@admin.route("/delete/<int:id>")
def delete_candidate(id):
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login'))

    entry = CandidateDetail.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('admin.user_list'))


@login_required
@admin.route("/assign_test/<login_id>")
def assign_test(login_id):
    user = CandidateDetail.query.filter_by(email_id=login_id).first()
    user_test = UserQuestionSet.query.filter_by(login_id=login_id).first()
    return render_template('assign_test.html', user=user, user_test=user_test)


@login_required
@admin.route("/add_test/<login_id>")
def add_test(login_id):
    entry = UserQuestionSet(login_id=login_id, status=0)
    user_test = UserQuestionSet.query.filter_by(login_id=login_id).first()
    if not user_test:
        db.session.add(entry)
        db.session.commit()
    user = UserQuestionSet.query.filter_by(login_id=login_id).first()
    check = QuestionSet.query.filter_by(user_que_set_id=user.id).first()
    if check:
        flash('Test already Added', 'success')
    else:
        test_question(user.id)
        flash('Test Added', 'success')
    return redirect(url_for('admin.assign_test', login_id=login_id))


@login_required
@admin.route("/add_candidate")
def add_candidate():
    form = CandidateRegistrationForm()
    if form.validate_on_submit():
        uploaded_file = request.files.get('resume', None)
        resume_dir = '../Resume'
        if not os.path.exists(resume_dir):
            os.makedirs(resume_dir)
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = date_str + uploaded_file.filename
        uploaded_file.save(os.path.join(resume_dir, secure_filename(file_name)))
        hashed_password = bcrypt.generate_password_hash(Config.PASSWORD).decode('utf-8')
        detail_entry = CandidateDetail(first_name=form.first_name.data, last_name=form.last_name.data,
                                       email_id=form.email_id.data, password=hashed_password,
                                       mobile_no=form.mobile_no.data, state=form.state.data,
                                       city=form.city.data, ssc_board=form.ssc_board.data,
                                       ssc_marks=form.ssc_marks.data, hsc_board=form.hsc_board.data,
                                       hsc_marks=form.hsc_marks.data, ug_degree=form.ug_degree.data,
                                       ug_college=form.ug_college.data, ug_university=form.ug_university.data,
                                       ug_marks=form.ug_marks.data, pg_degree=form.pg_degree.data,
                                       pg_college=form.pg_college.data, pg_university=form.pg_university.data,
                                       pg_marks=form.pg_marks.data, skill=form.skill.data,
                                       linked_link=form.linked_link.data, skype_id=form.skype_id.data,
                                       resume_remark=form.resume_remark.data, resume=file_name, enable=False)
        db.session.add(detail_entry)
        db.session.commit()
        flash('New Candidate Added!!', 'success')
        return redirect(url_for('admin.user_list'))
    return render_template('add_candidate.html', form=form)


def test_question(id):
    count = 1
    for x in range(0, Config.TEST_DIFFICULTY_LEVEL+1):
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        with engine.connect() as conn:
            query_string = f"SELECT r1.id as id, answer FROM questions_tbl AS r1 JOIN (SELECT CEIL(RAND() * (SELECT MAX(id)-10 FROM questions_tbl " \
                           f"where difficulty_level = {x})) AS id) AS r2 WHERE r1.id >= r2.id and difficulty_level = {x}  " \
                           f"ORDER BY r1.id ASC  LIMIT {Config.NO_OF_QUESTION};"
            records = conn.execute(query_string)
            for record in records:
                entry = QuestionSet(user_que_set_id=id, question_id=record.id, answer=record.answer,
                                    chosen_answer="", sequence_no=count, status=0,
                                    is_last=True if count == Config.TEST_DIFFICULTY_LEVEL * Config.NO_OF_QUESTION else False)
                db.session.add(entry)
                db.session.commit()
                count = count+1

# test_question(1)