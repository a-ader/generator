from textwrap import dedent

import pytest

from zmei_generator.contrib.admin.extras.application.suit import SuitAppExtra
from zmei_generator.parser.errors import TabsSuitRequiredValidationError
from zmei_generator.parser.parser import ZmeiParser


def _(code):
    parser = ZmeiParser()
    parser.parse_string(dedent(code))
    return parser.populate_application('example')


def test_suit():
    app = _("""
        @suit
    """)

    assert 'django-suit' in app.get_required_deps()
    assert 'suit' in app.get_required_apps()
    assert isinstance(app.suit, SuitAppExtra)


def test_app_name():
    app = _("""
        @suit("hoho!")
    """)

    assert app.suit.app_name == 'hoho!'


def test_admin_tabs_no_suit():

    with pytest.raises(TabsSuitRequiredValidationError):
        _("""
            #boo
            -----
            a
    
            @admin(tabs: lala(a))
        """)