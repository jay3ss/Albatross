import pytest

from albatross.core import forms


def test_new_author_form():
    form = forms.NewAuthorForm()
    assert form


def test_create_author_form_valid_data():
    assert forms.CreateAuthorForm(name="A. Name")


def test_create_author_form_invalid_data():
    with pytest.raises(ValueError):
        forms.CreateAuthorForm(name="")
