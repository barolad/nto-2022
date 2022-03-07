import datetime
from flask import Flask, render_template, request, session, url_for, flash, redirect, abort, g, make_response
from DataBaseAPI import DataBaseAPI
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from UserLogin import UserLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'isaktimurov'
app.debug = True
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db?check_same_thread=False'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Вы не авторизованы!"
login_manager.login_message_category = "alert alert-danger"

dbase = DataBaseAPI(app)


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


@app.route('/', methods=["POST", "GET"])
def index():
    return render_template('index.html', title='Главная страница')


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = dbase.getUserByUsername(request.form['username'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(url_for('index'))

        flash("Неверная пара логин/пароль", category='alert alert-danger')

    return render_template('login.html', title='Вход в приложение')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        if request.form['psw'] == request.form['psw2']:
            phash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['username'], request.form['firstname'], phash)
            if res:
                flash('Вы успешно зарегистрированы!', category='alert alert-success')
                return redirect(url_for('index'))
            else:
                flash('Ошибка при добавлении в базу данных.', category='alert alert-danger')
        else:
            flash('Неверно заполнены поля.', category='alert alert-danger')
    return render_template('registration.html', title='Регистрация')


@app.route('/test', methods=['POST', 'GET'])
@login_required
def test():
    dbase.getData(int(current_user.get_id()))
    return render_template('test.html', title='TEST', list=dbase.getData(current_user.get_id()))


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли из аккаунта!", category='alert alert-success')
    return redirect(url_for('login'))


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
