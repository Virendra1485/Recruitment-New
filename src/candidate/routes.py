import os

from flask import Flask, Blueprint, render_template, redirect, request, flash, url_for, session
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import create_engine
from werkzeug import secure_filename
from datetime import datetime


from .forms import CandidateRegistrationForm, LogInForm, TestForm
from models import CandidateDetail, Questions, UserQuestionSet, QuestionSet, Questions
from config import Config
from api_server import bcrypt, db

candidate = Blueprint('candidate', __name__)


@candidate.route("/registration", methods=['GET', 'POST'])
def registration():
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
        return redirect(url_for('candidate.login'))
    return render_template('candidate_registration.html', form=form)


@candidate.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('candidate.start_test'))

    form = LogInForm()
    if form.validate_on_submit():
        user = CandidateDetail.query.filter_by(email_id=form.email_id.data.strip()).first()
        if candidate and bcrypt.check_password_hash(user.password, form.password.data.strip()):
            login_user(user, form.remember.data)
            session["login_id"] = form.email_id.data.strip()
            flash('Login Successful!!', 'success')
            return redirect(request.args.get('next') or url_for('candidate.start_test'))
        else:
            flash('Invalid Email Id or Password', 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@candidate.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('candidate.login'))


@login_required
@candidate.route("/start_test")
def start_test():
    if not current_user.is_authenticated:
        return redirect(url_for('candidate.login'))

    user = UserQuestionSet.query.filter_by(login_id=session['login_id']).first()
    if not user:
        flash('Test is Not assigned', 'success')
        return render_template('start_test.html', id=current_user.id, user=user)
    if user.status == 0:
        user.date_modified = datetime.now()
        user.start_time = datetime.now()
        user.status = 1
        db.session.commit()

    return render_template('start_test.html', id=current_user.id, user=user)


@login_required
@candidate.route("/test/<sequence_no>", methods=['GET', 'POST'])
@candidate.route("/test", methods=['GET', 'POST'])
def test(sequence_no=None):
    if not sequence_no:
        sequence_no = 1

    sequence_no = int(sequence_no)
    form = TestForm()
    user_question_set = UserQuestionSet.query.filter_by(login_id=session["login_id"]).first()

    if not user_question_set:
        flash('Sorry You Have No Assigned Test', 'success')
        return redirect(url_for('candidate.start_test'))

    questions_set = QuestionSet.query.filter_by(sequence_no=sequence_no,
                                                user_que_set_id=user_question_set.id).first()
    if not questions_set and sequence_no == 1:
        flash('Sorry You Have No Assigned Test', 'success')
        return redirect(url_for('candidate.start_test'))

    if not questions_set:
        return redirect(url_for('candidate.candidate_result'))

    question = Questions.query.filter_by(id=questions_set.question_id).first()
    form.options.choices = [('A', question.option_a), ('B', question.option_b), ('C', question.option_c), ('D', question.option_d)]

    if request.method == "GET":
        if questions_set.status == 1 and questions_set.chosen_answer:
            form.options.data = questions_set.chosen_answer

    if form.validate_on_submit():
        questions_set.chosen_answer = form.options.data
        db.session.commit()
        if questions_set.is_last:
            questions_set.status = 2
            user_question_set.status = 2
            db.session.commit()
            return redirect(url_for('candidate.candidate_result'))
        else:
            questions_set.status = 1
            db.session.commit()
            return redirect(url_for('candidate.test', sequence_no=sequence_no + 1))

    return render_template('test.html', form=form, question=question, questions_set=questions_set)


@login_required
@candidate.route("/candidate_result")
def candidate_result():
    if not current_user.is_authenticated:
        return redirect(url_for('candidate.login'))

    login_id = session['login_id']
    marks = result()
    record = UserQuestionSet.query.filter_by(login_id=login_id).first()
    record.end_time = datetime.now()
    record.marks = marks
    record.status = 3
    record.result_status = 1
    db.session.commit()

    return render_template('result.html', login_id=login_id, marks=marks)


def result():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn:
        query_string = "select count(chosen_answer) from question_set_tbl where chosen_answer in (select answer from questions_tbl);"
        records = conn.execute(query_string)
        for record in records:
            marks = record[0]
    return marks