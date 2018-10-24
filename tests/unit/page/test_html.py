from textwrap import dedent

import pytest
from zmei_generator.parser.parser import parse_string
from zmei_generator.parser.populate import populate_collection_set


def _(code):
    tree = parse_string(dedent(code))

    return populate_collection_set(tree, 'example')


def test_page_html():
    cs = _("""

        [boo]
        @html {
            <h1>test</h1>
        }
        
        #foo
        ------
        lala
    """)

    assert len(cs.pages) == 1

    boo = cs.pages['boo']

    assert boo.name == 'boo'
    assert boo.blocks['content'][0].source == "<h1>test</h1>"
    assert boo.react is False
    assert boo.extra_bases == ['ZmeiDataViewMixin']



def test_page_html_area():
    cs = _("""

        [boo]
        @html.foo {
            <h1>test</h1>
        }
        
        #foo
        ------
        lala
    """)

    assert len(cs.pages) == 1

    boo = cs.pages['boo']

    assert boo.name == 'boo'
    assert boo.blocks['foo'][0].source == "<h1>test</h1>"
    assert boo.react is False
    assert boo.extra_bases == ['ZmeiDataViewMixin']
