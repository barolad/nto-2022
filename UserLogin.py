from flask_login import UserMixin
from flask import url_for
from flask import Flask, render_template, request, session, url_for, flash, redirect, abort, g, make_response

app = Flask(__name__)

class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

    def getName(self):
        return self.__user['username'] if self.__user else "Без имени"

    def getFirstName(self):
        return self.__user['firstname'] if self.__user else "Ингиборга"