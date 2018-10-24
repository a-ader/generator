from textwrap import dedent

from zmei_generator.extras.model.admin import AdminExtra, AdminInlineConfig
from zmei_generator.parser.parser import parse_string
from zmei_generator.parser.populate import populate_collection_set


def _(code):
    tree = parse_string(dedent(code))

    return populate_collection_set(tree, 'example')


def test_tree_simple():
    cs = _("""
    
        #boo
        ----------
        abc
        cda
        
        @tree
    
    """)

    boo = cs.collections['boo']

    assert boo.tree is True

    assert 'django-mptt' in cs.deps
    assert 'django-polymorphic-tree' in cs.deps
    assert 'mptt' in cs.apps
    assert 'polymorphic_tree' in cs.apps
    assert 'polymorphic' in cs.apps



def test_tree_poly():
    cs = _("""
    
        #boo
        ----------
        abc
        cda
        
        @tree(+polymorphic_list)
    
    """)

    boo = cs.collections['boo']

    assert boo.tree is True
    assert boo.tree_polymorphic_list is True

    assert 'django-mptt' in cs.deps
    assert 'django-polymorphic-tree' in cs.deps
    assert 'mptt' in cs.apps
    assert 'polymorphic_tree' in cs.apps
    assert 'polymorphic' in cs.apps
