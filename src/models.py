from api_server import db
from api_server import login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return CandidateDetail.query.get(int(user_id))


class BaseModel():
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class CandidateDetail(db.Model, UserMixin):
    __tablename__ = 'candidate_details_tbl'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(256), nullable=False)
    email_id = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    mobile_no = db.Column(db.String(10), nullable=False)
    state = db.Column(db.String(256), nullable=False)
    city = db.Column(db.String(256), nullable=False)
    ssc_board = db.Column(db.String(256), nullable=False)
    ssc_marks = db.Column(db.Integer)
    hsc_board = db.Column(db.String(256), nullable=False)
    hsc_marks = db.Column(db.Integer)
    ug_degree = db.Column(db.String(256), nullable=False)
    ug_college = db.Column(db.String(256), nullable=False)
    ug_university = db.Column(db.String(256), nullable=False)
    ug_marks = db.Column(db.Integer)
    pg_degree = db.Column(db.String(256), nullable=True)
    pg_college = db.Column(db.String(256), nullable=True)
    pg_university = db.Column(db.String(256), nullable=True)
    pg_marks = db.Column(db.Integer, default=None)
    skill = db.Column(db.String(256), nullable=True)
    linked_link = db.Column(db.String(256), nullable=True)
    skype_id = db.Column(db.String(256), nullable=True)
    resume_remark = db.Column(db.String(256), nullable=True)
    resume = db.Column(db.String(256), nullable=False)
    enable = db.Column(db.Boolean, nullable=False, default=False)


class AdminDetail(db.Model, UserMixin):
    __tablename__ = 'admin_details_tbl'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(256), nullable=False)
    mobile_no = db.Column(db.String(10), nullable=False)
    email_id = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=False)


class Questions(db.Model, UserMixin):
    __tablename__ = 'questions_tbl'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(256), nullable=False)
    code = db.Column(db.String(256), nullable=True)
    option_a = db.Column(db.String(256), nullable=False)
    option_b = db.Column(db.String(256), nullable=False)
    option_c = db.Column(db.String(256), nullable=False)
    option_d = db.Column(db.String(256), nullable=False)
    answer = db.Column(db.String(256), nullable=False)
    difficulty_level = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(256), nullable=False)


class UserQuestionSet(db.Model, BaseModel, UserMixin):
    __tablename__ = 'User_question_set_tbl'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login_id = db.Column(db.String(256), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.String(256), nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.String(256), nullable=False, default=datetime.utcnow)
    marks = db.Column(db.Integer, nullable=False, default=0)
    result_status = db.Column(db.Integer, nullable=False, default=0)
    # option_d = db.Column(db.String(256), nullable=False)
    # answer = db.Column(db.String(256), nullable=False)
    # type = db.Column(db.Integer, nullable=False)
    # difficulty_level = db.Column(db.String(256), nullable=False)


class QuestionSet(db.Model, UserMixin):
    __tablename__ = 'question_set_tbl'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_que_set_id = db.Column(db.Integer, db.ForeignKey(UserQuestionSet.__tablename__+'.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(Questions.__tablename__+'.id'), nullable=False)
    answer = db.Column(db.String(256), nullable=False)
    chosen_answer = db.Column(db.String(256), nullable=False)
    sequence_no = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    is_last = db.Column(db.Boolean, nullable=False, default=False)