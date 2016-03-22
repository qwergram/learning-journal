# -*- coding: utf-8 -*-

from learning_journal.models import Entry, DBSession


def test_list_route(dbtransaction, app):
    """Test if model initialized with correct vals."""
    response = app.get('/')
    assert response.status_code == 200


def test_list_view(dbtransaction, dummy_request):
    """Test list view function."""
    from learning_journal.views import list_view
    new_model = Entry(title="Norton", text="waffles")
    second_model = Entry(title="Norton2", text="pancakes")
    DBSession.add(new_model)
    DBSession.add(second_model)
    DBSession.flush()
    response_dict = list_view(dummy_request)
    assert response_dict['content'].get(new_model.id).title == new_model.title


def test_create_route(dbtransaction, app):
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


def test_login_route(dbtransaction, app):
    """Test if model initialized with correct vals."""
    response = app.get('/login')
    assert response.status_code == 200


def test_logout_route(dbtransaction, app):
    """Test if model initialized with correct vals."""
    response = app.get('/logout')
    assert response.location.split('/')[-1] == 'login'


def test_detail_view(dbtransaction, dummy_request):
    """Test detail view function."""
    from learning_journal.views import detail_view
    new_model = Entry(title="Norton", text="waffles")
    DBSession.add(new_model)
    DBSession.flush()
    dummy_request.matchdict = {'entry_id': new_model.id}
    response_dict = detail_view(dummy_request)
    assert response_dict['entry'].markdown_text == '<p>waffles</p>'
