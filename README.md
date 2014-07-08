toauth
======

A simple authentication system for Tornado.


1. Run the demo
---------------

1) run server:

    $ cd toauth
    $ export PYTHONPATH=.
    $ python demo/auth.py

2) access in browser:

    http://127.0.0.1:8888/

2. Customization
----------------

You can customize the authentication system by editing `settings.py`.

Open `settings.py` to see the default settings:

    # user orm class
    USER = User

    # dict-like session engine
    SESSION = Session

    # session key of user
    SESSION_KEY = 'auth_user_id'

    # cookie key of session
    COOKIE_KEY = 'auth_session_id'
