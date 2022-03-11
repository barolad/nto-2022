import datetime
from flask import Flask, render_template, request, session, url_for, flash, redirect, abort, g, make_response
from DataBaseAPI import DataBaseAPI
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from UserLogin import UserLogin
import pyautogui
from tkinter import *
import tkinter as tk
import random
from functools import reduce

app = Flask(__name__)
app.config['SECRET_KEY'] = 'isaktimurov'
app.debug = True
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db?check_same_thread=False'
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
    return render_template('index.html', title='Добро пожаловать')


@app.route('/menu', methods=["POST", "GET"])
def menu():
    pyautogui.screenshot('screensht.png')
    return render_template('menu.html', title='Меню')


@app.route('/budka', methods=["POST", "GET"])
def budka():
    UserLogin().takescreen()
    return render_template('budkanew.html', title='Фотобудка', id='targets/12.png')


@app.route('/galery', methods=["POST", "GET"])
def galery():
    return render_template('galereya.html', title='Галерея')


@app.route('/gid', methods=["POST", "GET"])
def gid():
    data=1
    # data = dbase.getData()
    # if data:
    #     for category in data:
    #         print(category[2])
    return render_template('gid.html', title='AR-гид', list=data)


@app.route('/marshrut', methods=["POST", "GET"])
def marshrut():
    start = request.args.getlist("action")
    prom=''
    all_m=[]
    data=dbase.getPathData()
    arg = int(start[0][1:])-1
    if data:
        for i in data:
            all_m.append(i[1])
    prom=str(all_m[arg])
    print(prom)
    print(prom)
    start=list('0'+prom)
    Exibits=[]
    data = dbase.getExibitData()
    if data:
        for i in data:
            Exibits.append(i)
    return render_template('m2.html', title='Остаток с учетом инфляции', Exibits=Exibits, prom=prom, list=start, lena=len(start))


@app.route('/marshrutsostav', methods=["POST", "GET"])
def marshrutsostav():
    start = request.args.getlist("expo")
    number = str(''.join(map(str, start)))
    start = list('0' + number)
    Exibits=[]
    data = dbase.getExibitData()
    if data:
        for i in data:
            Exibits.append(i)
    return render_template('m2.html', title='Остаток с учетом инфляции', Exibits=Exibits, prom=number, list=start, lena=len(start))

@app.route('/marshrutgenerate', methods=["POST", "GET"])
def marshrutgenerate():
    alf=[1,2,3,4,5,6,7,8]
    random.shuffle(alf)
    alf = str(''.join(map(str, alf)))
    start = list('0' + alf)
    Exibits=[]
    data = dbase.getExibitData()
    if data:
        for i in data:
            Exibits.append(i)
    return render_template('m2.html', title='Остаток с учетом инфляции', Exibits=Exibits, prom=alf, list=start, lena=len(start))

@app.route('/portal', methods=["POST", "GET"])
def portal():
    return render_template('portal.html', title='Портал')


@app.route('/stats', methods=["POST", "GET"])
def stats():
    data1=dbase.getExibitData()
    P=[]
    for k in data1:
        P.append(k[1])
    data = dbase.getRecordData()
    O=[]
    count1=0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    count7 = 0
    count8 = 0
    love1=0
    love2 = 0
    love3 = 0
    love4 = 0
    love5 = 0
    love6 = 0
    love7 = 0
    love8 = 0
    for i in data:
        O.append(i)
    O=O[::-1]
    date=(str(datetime.datetime.now())[:-7])
    # print(date)
    datedate=date[:-9]
    # dateti=dateti.split(':')
    # dateti=str(dateti[0]+dateti[1])
    # print(datedate)
    # print(dateti)
    # print(datedate+dateti)
    for k in range(0,len(O)):
        print("EHF")
        if date>O[k][1] and datedate==str(O[k][1][:-9]):
            print(O[k][1])
            if O[k][2]==1:
               count1+=1
               love1+=O[k][4]+O[k][5]+O[k][6]
            elif O[k][2]==2:
                count2 += 1
                love2 += O[k][4] + O[k][5] + O[k][6]
            elif O[k][2]==3:
                count3 += 1
                love3 += O[k][4] + O[k][5] + O[k][6]
            elif O[k][2]==4:
                count4 += 1
                love4 += O[k][4] + O[k][5] + O[k][6]
            elif O[k][2]==5:
                count5 += 1
                love5 += O[k][4] + O[k][5] + O[k][6]
            elif O[k][2]==6:
                count6 += 1
                love6 += O[k][4] + O[k][5] + O[k][6]
            elif O[k][2]==7:
                count7 += 1
                love7 += O[k][4] + O[k][5] + O[k][6]
            elif O[k][2]==8:
                count8 += 1
                love8 += O[k][4] + O[k][5] + O[k][6]
    vsego=count1+count2+count3+count4+count5+count6+count7+count8
    I=[count1,count2,count3,count4,count5,count6,count7,count8]
    print(I)
    if count1!=0:
        love1=love1//count1 //3
    if count2 != 0:
        love2 = love2 // count2 //3
    if count3 != 0:
        love3 = love3 // count3 //3
    if count4 != 0:
        love4 = love4 // count4 //3
    if count5 != 0:
        love5 = love5 // count5 //3
    if count6 != 0:
        love6 = love6 // count6 //3
    if count7 != 0:
        love7 = love7 // count7 //3
    if count8 != 0:
        love8 = love8 // count8 //3
    L=[love1,love2,love3,love4,love5,love6,love7,love8]
    ROMA=[]

    for z in range(0,len(O)):
        print(O[z][4],O[z][5],O[z][6])

    for p in range(0,8):
        itog = {}
        itog["io"]=I[p]
        itog['no']=P[p]
        itog['lo']=L[p]
        ROMA.append(itog)
    print(ROMA)
    start = request.args.getlist("action")
    if start[0]=='po_u':
        ROMA=sorted(ROMA, key=lambda x: x['io'])
    elif start[0]=='po_v':
        ROMA = sorted(ROMA, key=lambda x: x['io'])
        ROMA=ROMA[::-1]
    elif start[0]=='lo_u':
        ROMA = sorted(ROMA, key=lambda x: x['lo'])
    elif start[0] == 'lo_v':
        ROMA = sorted(ROMA, key=lambda x: x['lo'])
        ROMA = ROMA[::-1]
    else:
        ROMA=ROMA
    print(start)
    return render_template('stats.html', title='Статистика', ROMA=ROMA, I=I, P=P, vsego=vsego)


@app.route("/statsadm", methods=["POST", "GET"])
@login_required
def statsadm():
    data = dbase.getRecordData()
    M=[]
    t1,t2,t3,t4,t5,t6,t7,t8=[],[],[],[],[],[],[],[]
    v1,d1,c1,v2,d2,c2,v3,d3,c3,v4,d4,c4,v5,d5,c5,v6,d6,c6,v7,d7,c7,v8,d8,c8=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
    for i in data:
        M.append(i)
    for k in range(0,len(M)):
        if M[k][2]==1:
            t1.append(M[k][3])
            v1.append(M[k][4])
            d1.append(M[k][5])
            c1.append(M[k][6])
        elif M[k][2]==2:
            t2.append(M[k][3])
            v2.append(M[k][4])
            d2.append(M[k][5])
            c2.append(M[k][6])
        elif M[k][2]==3:
            t3.append(M[k][3])
            v3.append(M[k][4])
            d3.append(M[k][5])
            c3.append(M[k][6])
        elif M[k][2]==4:
            t4.append(M[k][3])
            v4.append(M[k][4])
            d4.append(M[k][5])
            c4.append(M[k][6])
        elif M[k][2]==5:
            t5.append(M[k][3])
            v5.append(M[k][4])
            d5.append(M[k][5])
            c5.append(M[k][6])
        elif M[k][2]==6:
            t6.append(M[k][3])
            v6.append(M[k][4])
            d6.append(M[k][5])
            c6.append(M[k][6])
        elif M[k][2]==7:
            t7.append(M[k][3])
            v7.append(M[k][4])
            d7.append(M[k][5])
            c7.append(M[k][6])
        elif M[k][2]==8:
            t8.append(M[k][3])
            v8.append(M[k][4])
            d8.append(M[k][5])
            c8.append(M[k][6])
    print(t1)
    lent=len(t1)
    maxit1=max(t1)
    maxit2=max(t2)
    maxit3 = max(t3)
    maxit4 = max(t4)
    maxit5 = max(t5)
    maxit6 = max(t6)
    maxit7 = max(t7)
    maxit8 = max(t8)
    mini1=min(t1)
    mini2 = min(t2)
    mini3 = min(t3)
    mini4 = min(t4)
    mini5 = min(t5)
    mini6 = min(t6)
    mini7 = min(t7)
    mini8 = min(t8)
    sred1 = reduce(lambda x, y: x + y, t1) /lent
    sred2 = reduce(lambda x, y: x + y, t2) / lent
    sred3 = reduce(lambda x, y: x + y, t3) / lent
    sred4 = reduce(lambda x, y: x + y, t4) / lent
    sred5 = reduce(lambda x, y: x + y, t5) / lent
    sred6 = reduce(lambda x, y: x + y, t6) / lent
    sred7 = reduce(lambda x, y: x + y, t7) / lent
    sred8 = reduce(lambda x, y: x + y, t8) / lent
    ITma=[maxit1,maxit2,maxit3,maxit4,maxit5,maxit6,maxit7,maxit8]
    ITmi=[mini1,mini2,mini3,mini4,mini5,mini6,mini7,mini8]
    ITsr=[sred1,sred2,sred3,sred4,sred5,sred6,sred7,sred8]
    V=[v1,v2,v3,v4,v5,v6,v7,v8]
    D=[d1,d2,d3,d4,d5,d6,d7,d8]
    C=[c1,c2,c3,c4,c5,c6,c7,c8]
    print(C,D,V)
    return render_template('statsadm.html', title='Статистика администратора',  ITma=ITma, ITmi=ITmi, ITsr=ITsr, V=V, D=D, C=C)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('menu'))

    if request.method == "POST":
        user = dbase.getUserByUsername(request.form['username'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(url_for('menu'))

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
                return redirect(url_for('login'))
            else:
                flash('Ошибка при добавлении в базу данных.', category='alert alert-danger')
        else:
            flash('Неверно заполнены поля.', category='alert alert-danger')
    return render_template('registration.html', title='Регистрация')


@app.route('/portals', methods=["POST", "GET"])
def portals():
    return render_template('portals.html', title='AR-Гид: На маршруте')


@app.route('/3droom', methods=["POST", "GET"])
def trideroom():
    return render_template('3droom.html', title='Портал')


@app.route('/360room', methods=["POST", "GET"])
def tristaroom():
    return render_template('360room.html', title='Портал')

@app.route('/m2', methods=["POST", "GET"])
def m2():
    return render_template('m2.html', title='AR-Гид: На маршруте')

@app.route('/mask1', methods=["POST", "GET"])
def mask1():
    return render_template('mask1.html', title='AR-Гид: На маршруте')

@app.route('/mask2', methods=["POST", "GET"])
def mask2():
    return render_template('mask2.html', title='AR-Гид: На маршруте')

@app.route('/mask3', methods=["POST", "GET"])
def mask3():
    return render_template('mask3.html', title='AR-Гид: На маршруте')


@app.route('/obrmarshrut', methods=["POST", "GET"])
def obrmarshrut():
    start = request.args.getlist("action")
    romaloh = request.args.getlist("yoyo")
    if len(start) == 0:
        start = request.args.getlist("expo")
    else:
        all_m = []
        data = dbase.getPathData()
        arg = int(start[0][1:]) - 1
        if data:
            for i in data:
                all_m.append(i[1])
        prom = str(all_m[arg])
        start = list('0' + prom)

    Exibits = []
    data = dbase.getExibitData()
    if data:
        for i in data:
            Exibits.append(i)

    print(Exibits)
    print(start)
    print(romaloh)
    return render_template('m2.html', title='Остаток с учетом инфляции', romaloh=romaloh, Exibits=Exibits, prom=prom,
                           list=start, lena=len(start))


@app.route('/m4', methods=["POST", "GET"])
def m4():
    return render_template('m4.html', title='AR-Гид: На маршруте')


@app.route('/m5', methods=["POST", "GET"])
def m5():
    return render_template('m5.html', title='AR-Гид: На маршруте')


@app.route('/test', methods=['POST', 'GET'])
def test():
    return render_template('test.html', title='TEST')

@app.route('/BLOBS', methods=['POST', 'GET'])
def BLOBS():
    data = dbase.getBLOBData()
    O=[]
    for i in data:
        print(str(i)[1:-2])
        O.append(i)
    Om=(str(O[0])[1:-2])
    h = make_response(Om)
    h.headers['Content-Type'] = "image/jpg"
    return h


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли из аккаунта!", category='alert alert-success')
    return redirect(url_for('login'))


@app.route('/exp1', methods=["POST", "GET"])
def exp1():
    return render_template('exp1.html', title='AR-Гид: На маршруте')


@app.route('/exp2', methods=["POST", "GET"])
def exp2():
    return render_template('exp2.html', title='AR-Гид: На маршруте')


@app.route('/exp3', methods=["POST", "GET"])
def exp3():
    return render_template('exp3.html', title='AR-Гид: На маршруте')


@app.route('/exp4', methods=["POST", "GET"])
def exp4():
    return render_template('exp4.html', title='AR-Гид: На маршруте')


@app.route('/exp5', methods=["POST", "GET"])
def exp5():
    return render_template('exp5.html', title='AR-Гид: На маршруте')


@app.route('/exp6', methods=["POST", "GET"])
def exp6():
    return render_template('exp6.html', title='AR-Гид: На маршруте')


@app.route('/exp7', methods=["POST", "GET"])
def exp7():
    return render_template('exp7.html', title='AR-Гид: На маршруте')


@app.route('/exp8', methods=["POST", "GET"])
def exp8():
    return render_template('exp8.html', title='AR-Гид: На маршруте')


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html'), 404


if __name__ == '__main__':
    app.run(host='192.168.1.69', port=5000, debug=True, ssl_context='adhoc')
