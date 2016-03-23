# -*- coding: utf-8 -*-

from learning_journal.models import Entry, DBSession


def test_list_route(dbtransaction, app):
    """Test if model initialized with correct vals."""
    response = app.get('/')
    assert response.status_code == 200


def test_list_view(dbtransaction, dummy_request):
    """Test list view function.

    Add 11 random entries to the database and make sure they all appear.
    """
    from learning_journal.views import list_view
    import random
    string = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split()
    for times in range(12):
        random.shuffle(string)
        new_model = Entry(title=" ".join(string), text="_".join(string))
        DBSession.add(new_model)
        DBSession.flush()
        response_dict = list_view(dummy_request)
        assert response_dict['content'].get(new_model.id
                                            ).title == new_model.title


def test_login_route(app):
    """Test if model initialized with correct vals."""
    response = app.get('/login')
    assert response.status_code == 200


def test_login_view(app):
    """Test if login view contains form."""
    response = app.get('/login')
    expected = """<form action="" method="post">
<span>thatonelegend login: <input autofocus="" name="username"/></span><br/>
<span>password: <input name="password" type="password"/></span><br/>
<input type="submit">
</input></form>"""
    assert expected == str(response.html.find("form"))


def test_login_correctly(app, dummy_request):
    """Test if login POST works correctly."""
    response = app.post("/login", {
                                    "username": "norton",
                                    "password": "password"
                                  })
    assert response.status_code == 302


def test_login_incorrectly(app, dummy_request):
    """Test if login POST works correctly."""
    response = app.post("/login",
                        {"username": "norton", "password": "woops!"},
                        status=401
                        )
    assert response.status_code == 401


def test_login_incorrectly_view(app, dummy_request):
    """Test if login POST return html works correctly."""
    response = app.post("/login",
                        {"username": "norton", "password": "woops!"},
                        status=401
                        )
    assert ("<span class=\"red\">"
            "Your login was incorrect, please try again!"
            "</span>") in response.text


def test_create_route(app):
    """Test if permissions block anonymous users."""
    response = app.get('/create', status=403)
    assert response.status_code == 403


def test_edit_route(dbtransaction, app):
    """Test if permissions block anonymous users."""
    new_model = Entry(title="Norton", text="waffles")
    DBSession.add(new_model)
    DBSession.flush()
    response = app.get('/edit/{}'.format(new_model.id), status=403)
    assert response.status_code == 403


def test_logout_route(dbtransaction, app):
    """Test if model initialized with correct vals."""
    response = app.get('/logout')
    assert response.location.split('/')[-1] == 'login'


def test_post_login_auth_tkt_present(app):
    """Test to ensure that the auth ticket is there."""
    data = {'username': 'norton', 'password': 'password'}
    response = app.post('/login', data)
    headers = response.headers
    cookies_set = headers.getall('Set-Cookie')
    assert cookies_set
    for cookie in cookies_set:
        if cookie.startswith('auth_tkt'):
            break
    else:
        assert False


def test_detail_view(dbtransaction, dummy_request):
    """Test detail view function."""
    from learning_journal.views import detail_view
    new_model = Entry(title="Norton", text="waffles")
    DBSession.add(new_model)
    DBSession.flush()
    dummy_request.matchdict = {'entry_id': new_model.id}
    response_dict = detail_view(dummy_request)
    assert response_dict['entry'].markdown_text == '<p>waffles</p>'


def test_authenticated_create_route(app):
    """Test if permissions allow admin."""
    data = {'username': 'norton', 'password': 'password'}
    response = app.post('/login', data)
    assert response.status_code == 302
    create = app.get('/create')
    assert create.status_code == 200


def test_authenticated_edit_route(app):
    """Test if permissions allow admin."""
    data = {'username': 'norton', 'password': 'password'}
    app.post('/login', data)
    app.get('/create')
    new_model = Entry(title="Norton", text="waffles")
    DBSession.add(new_model)
    DBSession.flush()
    edit = app.get('/edit/1')
    assert edit.status_code == 200
