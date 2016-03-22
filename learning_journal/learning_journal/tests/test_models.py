# -*- coding: utf-8 -*-

from learning_journal.models import Entry, DBSession


def test_create_mymodel_entry():
    """Test creation of model."""
    new_model = Entry(title="Norton", text="waffles")
    assert new_model.id is None
    DBSession.add(new_model)
    DBSession.flush()
    assert new_model.id is not None
    assert new_model.text == 'waffles'
    assert new_model.title == 'Norton'
    assert new_model.created is not None

def test_delete_mymodel_entry(loadeddb):
    import pdb; pdb.set_trace()
