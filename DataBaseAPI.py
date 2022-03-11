from flask import flash
from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, BLOB, select, \
    insert, BINARY, update, Float, Date, Time, between
from flask_sqlalchemy import SQLAlchemy
import datetime
import pymysql
from werkzeug.security import check_password_hash

pymysql.install_as_MySQLdb()
now = datetime.datetime.now()


class DataBaseAPI:
    def __init__(self, app):
        self.__engine = SQLAlchemy(app).engine
        self.__connection = self.__engine.connect()
        self.__metadata = MetaData()
        self.setupTables()

    def setupTables(self):
        self.__users_table = Table('users', self.__metadata,
                                   Column('id', Integer(), primary_key=True, autoincrement=True),
                                   Column('username', Text(), primary_key=False, nullable=False),
                                   Column('firstname', Text(), primary_key=False, nullable=False),
                                   Column('psw', Text(), primary_key=False, nullable=False),
                                   Column('time', Text(), primary_key=False, nullable=False),
                                   )
        self.__exibit_table = Table('exibit', self.__metadata,
                                    Column('exId', Integer(), primary_key=True, autoincrement=True),
                                    Column('exName', Text(), primary_key=False, nullable=False),
                                    Column('exIdroom', Integer(), primary_key=False, nullable=False),
                                    Column('z1', Text(), primary_key=False, nullable=False),
                                    Column('z2', Text(), primary_key=False, nullable=False),
                                    Column('z3', Text(), primary_key=False, nullable=False),
                                    Column('z4', Text(), primary_key=False, nullable=False),
                                    Column('z5', Text(), primary_key=False, nullable=False),
                                    Column('z6', Text(), primary_key=False, nullable=False),
                                    Column('z7', Text(), primary_key=False, nullable=False),
                                    Column('z8', Text(), primary_key=False, nullable=False),
                                    )
        self.__path_table = Table('path', self.__metadata,
                                  Column('phId', Text(), primary_key=True),
                                  Column('phFull', Text(), primary_key=False, nullable=False),
                                  )
        self.__records_table = Table('records', self.__metadata,
                                     Column('id', Integer(), primary_key=True, autoincrement=True),
                                     Column('time', Text(), primary_key=False, nullable=False),
                                     Column('exibitId', Integer(), primary_key=False, nullable=False),
                                     Column('timeSpentInFrontSec', Integer(), primary_key=False, nullable=False),
                                     Column('visualFeedback', Integer(), primary_key=False, nullable=False),
                                     Column('description', Integer(), primary_key=False, nullable=False),
                                     Column('completeness', Integer(), primary_key=False, nullable=False),
                                     )
        self.__blob_table = Table('blob', self.__metadata,
                                     Column('blobs', BLOB(), primary_key=False, nullable=False),
                                     )
        self.__metadata.create_all(self.__engine)

    def addUser(self, username, firstname, hpsw):
        try:
            select_query_username = select([self.__users_table]).where(
                self.__users_table.c.username == username
            )
            check_username = self.__connection.execute(select_query_username).rowcount <= 0
            if not check_username:
                flash("Пользователь с таким логином уже существует")
                return False
            timestamp = now.strftime("%d-%m-%Y %H:%M")
            insert_query = insert(self.__users_table).values(
                username=username,
                firstname=firstname,
                psw=hpsw,
                time=timestamp
            )
            self.__connection.execute(insert_query)
        except BaseException as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False
        return True

    def getUser(self, user_id):
        try:
            select_query = select([self.__users_table]).where(
                self.__users_table.c.id == user_id
            )
            select_result = self.__connection.execute(select_query).fetchone()
            if select_result is None:
                flash("Пользователь не найден", category='alert alert-danger')
                return False
            # if select_result["psw"] != hpsw:
            #    flash("Попытка взлома: ошибка при сверении хэшей паролей")
            #    return False
            output = dict(select_result)
            # del output["psw"]
            return output
        except BaseException as e:
            print("Ошибка получения данных из БД " + str(e))
            return False
        return True

    def getUserByUsername(self, username):
        try:
            select_query = select([self.__users_table]).where(
                self.__users_table.c.username == username
            )
            select_result = self.__connection.execute(select_query).fetchone()
            if select_result is None:
                flash("Пользователь не найден", category='alert alert-danger')
                return False
            # if select_result["psw"] != hpsw:
            #    flash("Попытка взлома: ошибка при сверении хэшей паролей")
            #    return False
            output = dict(select_result)
            # del output["psw"]
            return output
        except BaseException as e:
            print("Ошибка получения данных из БД " + str(e))
            return False
        return True


    def addFeedback(self, username, email, text):
        try:
            timestamp = now.strftime("%d-%m-%Y %H:%M")
            insert_query = insert(self.__feedback_table).values(
                username=username,
                email=email,
                text=text,
                time=timestamp
            )
            self.__connection.execute(insert_query)
        except BaseException as e:
            print("Ошибка отправки сообщения " + str(e))
            return False
        return True

    def getUserData(self):
        try:
            select_query = select([self.__user_data_table])
            select_result = self.__connection.execute(select_query)
            if select_result is None:
                flash("Пользователь не найден", category='alert alert-danger')
                return False
            return select_result
        except BaseException as e:
            print("Ошибка добавления записи" + str(e))
            return False
        return True

    def getPathData(self):
        try:
            select_query = select([self.__path_table])
            select_result = self.__connection.execute(select_query)
            if select_result is None:
                flash("Пользователь не найден", category='alert alert-danger')
                return False
            return select_result
        except BaseException as e:
            print("Ошибка добавления записи" + str(e))
            return False
        return True

    def getRecordData(self):
        try:
            select_query = select([self.__records_table]).order_by(self.__records_table.c.time.desc())
            select_result = self.__connection.execute(select_query)
            if select_result is None:
                flash("Пользователь не найден", category='alert alert-danger')
                return False
            return select_result
        except BaseException as e:
            print("Ошибка добавления записи" + str(e))
            return False
        return True

    def getExibitData(self):
        try:
            select_query = select([self.__exibit_table])
            select_result = self.__connection.execute(select_query)
            if select_result is None:
                flash("Пользователь не найден", category='alert alert-danger')
                return False
            return select_result
        except BaseException as e:
            print("Ошибка добавления записи" + str(e))
            return False
        return True

    def getBLOBData(self):
        try:
            select_query = select([self.__blob_table])
            select_result = self.__connection.execute(select_query)
            if select_result is None:
                flash("Пользователь не найден", category='alert alert-danger')
                return False
            return select_result
        except BaseException as e:
            print("Ошибка добавления записи" + str(e))
            return False
        return True