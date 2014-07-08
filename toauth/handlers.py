#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from .database import DB
from .settings import (
    USER, SESSION, SESSION_KEY, COOKIE_KEY
)


class AuthHandlerMixin(object):

    @property
    def db(self):
        if not hasattr(self.application, 'db'):
            self.application.db = DB
        return self.application.db

    @property
    def session(self):
        if not hasattr(self.application, 'session'):
            session_id = self.get_secure_cookie(COOKIE_KEY)
            self.application.session = SESSION(self.db, session_id)
        return self.application.session

    def authenticate(self, username, password):
        """Authenticates against `username` and `password`."""
        try:
            user = self.db.query(USER).filter(USER.username == username).one()
            if user.check_password(password):
                return user
            else:
                return None
        except (NoResultFound, MultipleResultsFound):
            return None

    def register(self, **kwargs):
        """Create an user.

        If `next_url` is specified, redirect to it at last.
        """
        next_url = kwargs.pop('next_url', None)
        password = kwargs.pop('password')

        user = USER(**kwargs)
        user.set_password(password)
        self.db.add(user)
        self.db.commit()

        if next_url:
            self.redirect(next_url)

    def login(self, user, next_url=None):
        """Persist a user id and send session id as a cookie.

        This way a user doesn't have to reauthenticate on every request.
        If `next_url` is specified, redirect to it at last.
        """
        self.session[SESSION_KEY] = user.id
        self.session.save()

        self.set_secure_cookie(COOKIE_KEY, self.session.id)
        if next_url:
            self.redirect(next_url)

    def logout(self, next_url=None):
        """Removes the authenticated user's ID and clear cookies.

        If `next_url` is specified, redirect to it at last.
        """
        self.session.pop(SESSION_KEY, None)
        self.session.save()

        self.clear_cookie(COOKIE_KEY)
        if next_url:
            self.redirect(next_url)

    def get_current_user(self):
        if SESSION_KEY in self.session:
            user_id = self.session[SESSION_KEY]
            user = self.db.query(USER).filter(USER.id == user_id).first()
            return user
        return None
