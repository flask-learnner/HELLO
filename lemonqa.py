from flask import Flask, render_template, g, redirect, url_for, session, request
from sqlalchemy import or_

import config

from models import User, Question, Answer
from exts import db
from decorate import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    key = request.values.get('key', '')
    if key == '':
        questions = Question.query.order_by('-creat_time').all()
    else:
        questions = Question.query.join(User).filter(
            or_(Question.title.like('%{0}%'.format(key)), Question.content.like('%{0}%'.format(key)),
                User.username.like('%{0}%'.format(key)), User.telephone.like('%{0}%'.format(key)))
        ).order_by(
            '-creat_time').all()
    context = {
        'key': key,
        'questions': questions
    }
    return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return '手机号码或密码输入错误，请确认后再登录！'


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return '该手机号码已被注册，请更换手机号 ！'
        else:
            if password1 != password2:
                return '两次密码输入不一致，请核对后再输入！'
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()

                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session('user_id')
    session.clear()
    return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        user_id = session.get('user_id')
        print(user_id)
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>/')
@login_required
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()

    return render_template('detail.html', question=question_model)


@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {'user': None}


@app.before_first_request
def crate_tables():
    db.create_all()


@app.before_request
def session_user():
    if hasattr(g, 'user_id'):
        user_id = g.user_id
        session['user_id'] = user_id


if __name__ == '__main__':
    app.run()
