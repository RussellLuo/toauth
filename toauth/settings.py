#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .models import User
from .sessions import Session

# user orm class
USER = User

# dict-like session engine
SESSION = Session

# session key of user
SESSION_KEY = 'auth_user_id'

# cookie key of session
COOKIE_KEY = 'auth_session_id'
