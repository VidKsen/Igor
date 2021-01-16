from flask import render_template, redirect, flash, url_for, request, session
from app import app
from app.my_forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import db, models
from app.my_forms import RegistrationForm, CreateTest, AddQuestion, GoTest, AnswerForms
from app.models import User, Test, Question, Answers, UserAnswers, UserResults

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    tests = models.Test.query.all()
    results = models.UserResults.query.filter_by(u_res = current_user.id).all()
    print(results)
    form = GoTest()
    if form.validate_on_submit():
        session['number'] = 0
        session['test'] = form.tests.data
        session['length'] = len(models.Question.query.filter_by(test=form.tests.data).all())
        return redirect(url_for('answerpage'))
    return render_template('index.html', title='Home', tests=tests, results=results, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
            firstname=form.firstname.data, lastname=form.lastname.data,
            patronumic=form.patronumic.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/newtest', methods=['GET', 'POST'])
@login_required
def newtest():
    form = CreateTest()
    if form.validate_on_submit():
        test = Test(name=form.testname.data)
        db.session.add(test)
        db.session.commit()
        flash('Test was create!')
        return redirect(url_for('addquestion'))
    return render_template('newtest.html', title='Create Test', form=form)

@app.route('/addquestion', methods=['GET', 'POST'])
@login_required
def addquestion():
    form = AddQuestion()
    if form.validate_on_submit():
        t_id = Test.query.filter_by(name=form.test.data).first().id
        question = Question(body=form.body.data, test=t_id)
        db.session.add(question)
        db.session.commit()
        q_id = question.id
        answer1 = Answers(body=form.answer_name1.data, value=form.value_answer1.data, quest=q_id)
        answer2 = Answers(body=form.answer_name2.data, value=form.value_answer2.data, quest=q_id)
        answer3 = Answers(body=form.answer_name3.data, value=form.value_answer3.data, quest=q_id)
        answer4 = Answers(body=form.answer_name4.data, value=form.value_answer4.data, quest=q_id)
        db.session.add(answer1)
        db.session.add(answer2)
        db.session.add(answer3)
        db.session.add(answer4)
        db.session.commit()
        flash('Question was add')
        return redirect(url_for('addquestion'))
    return render_template('addquestion.html', title='Add Question', form=form)

@app.route('/testlist')
def testlist():
    t_id = 1
    testname = models.Test.query.filter_by(id = t_id).first().name
    questions = models.Question.query.filter_by(test = t_id)
    return render_template('testlist.html', title='Just do it, motherfuker!', questions=questions, testname=testname)

@app.route('/answerpage', methods=['GET', 'POST'])
@login_required
def answerpage():
    form = AnswerForms()
    i = session.get('number')
    L = session.get('length')
    if form.validate_on_submit():
        session['number'] = session.get('number') + 1
        questions = models.Question.query.filter_by(test=session.get('test')).all()
        question = questions[i]
        answers = models.Answers.query.filter_by(quest=question.id).all()
        for a in UserAnswers.query.filter_by(question = question.id).all():
            db.session.delete(a)
            db.session.commit()
        if (form.Answer1.data == 1):
            u_answer = UserAnswers(user = current_user.id,
                question = question.id, answers = answers[0].id)
            db.session.add(u_answer)
            db.session.commit()
        if (form.Answer2.data == 1):
            u_answer = UserAnswers(user = current_user.id,
                question = question.id, answers = answers[1].id)
            db.session.add(u_answer)
            db.session.commit()
        if (form.Answer3.data == 1):
            u_answer = UserAnswers(user = current_user.id,
                question = question.id, answers = answers[2].id)
            db.session.add(u_answer)
            db.session.commit()
        if (form.Answer4.data == 1):
            u_answer = UserAnswers(user = current_user.id,
                question = question.id, answers = answers[3].id)
            db.session.add(u_answer)
            db.session.commit()
        return redirect(url_for('answerpage'))
    if i != L:
        questions = models.Question.query.filter_by(test=session.get('test')).all()
        question = questions[i]
        answers = models.Answers.query.filter_by(quest=question.id).all()
        return render_template('answerpage.html', title='Question',
            form=form, questions=questions, question=question,
            answers=answers, i=i, L=L)
    else:
        sum = 0
        sum_u = 0
        sum_r = 0
        questions = models.Question.query.filter_by(test=session.get('test')).all()
        for q in questions:
            answers = models.Answers.query.filter_by(quest=q.id).all()
            user_answers = models.UserAnswers.query.filter_by(user=current_user.id,
                        question = q.id).all()
            sum_u += len(user_answers)
            for a in answers:
                if (a.value == 1):
                    sum += 1
                    user_a = models.UserAnswers.query.filter_by(user=current_user.id,
                        answers = a.id).first()
                    if (user_a != None):
                        sum_r += 1
        result = (2*sum_r - sum_u)
        if (result < 0):
            result = 0
        ur = models.UserResults.query.filter_by(t_res = questions[0].test).first()
        print(ur)
        if ur != None:
            db.session.delete(ur)
            db.session.commit()
        ur_new = UserResults(u_res = current_user.id, t_res = questions[0].test,
            result = round(result, 2), max = sum, right = sum_r, error = sum_u - sum_r)
        db.session.add(ur_new)
        db.session.commit()
        return render_template('answerpage.html', title='Result', result = round(result, 2),
            max = sum, right = sum_r, error = sum_u - sum_r)