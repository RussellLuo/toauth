#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

import tornado.web
import tornado.httpserver

from toauth import AuthHandlerMixin, login_required


class BaseHandler(AuthHandlerMixin, tornado.web.RequestHandler):
    pass


class Index(BaseHandler):
    def get(self):
        self.render('index.html')


class Admin(BaseHandler):
    @login_required(login_url='/login')
    def get(self):
        self.render('admin.html')


class Register(BaseHandler):
    def get(self):
        self.render('register.html')

    def post(self):
        username = self.get_argument('username')
        email = self.get_argument('email')
        password = self.get_argument('password')
        self.register(username=username, password=password,
                      email=email, next_url='/')


class Login(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        next_url = self.get_argument('next')
        user = self.authenticate(username, password)
        if user:
            self.login(user, next_url=next_url)
        else:
            self.redirect('/register')


class Logout(BaseHandler):
    def get(self):
        self.logout(next_url='/')


def main():
    handlers = [
        (r'/', Index),
        (r'/admin', Admin),
        (r'/register', Register),
        (r'/login', Login),
        (r'/logout', Logout),
    ]
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        cookie_secret='__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__',
        login_url='/login',
    )
    application = tornado.web.Application(handlers, **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    from toauth.database import syncdb
    syncdb()

    main()
