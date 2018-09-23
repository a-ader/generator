from textwrap import dedent

from zmei_generator.extras.admin import AdminExtra, AdminInlineConfig
from zmei_generator.parser.parser import parse_string
from zmei_generator.parser.populate import populate_collection_set


def _(code):
    tree = parse_string(dedent(code))

    return populate_collection_set(tree, 'example')


def test_admin_empty():
    cs = _("""
    
        #boo
        ----------
        abc
        cda
        
        @admin
    
    """)

    boo = cs.collections['boo']

    assert isinstance(boo.admin, AdminExtra)
    assert cs.admin is True


def test_admin_one_line():
    cs = _("""
    
        #boo
        ----------
        abc
        cda
        
        @admin(list: *)
    
    """)

    boo = cs.collections['boo']

    assert isinstance(boo.admin, AdminExtra)
    assert cs.admin is True
    assert [x.name for x in boo.admin.admin_list] == ['abc', 'cda']


def test_admin_with_parent():
    cs = _("""
    
        #foo
        ----------
        a
    
        #foo->boo
        ----------
        b
        c
        
        @admin(list: *)
    
    """)

    boo = cs.collections['boo']

    assert isinstance(boo.admin, AdminExtra)
    assert cs.admin is True
    assert [x.name for x in boo.admin.admin_list] == ['a', 'b', 'c']


def test_admin_with_parent_local_only():
    cs = _("""
    
        #foo
        ----------
        a
    
        #foo->boo
        ----------
        b
        c
        
        @admin(list: .*)
    
    """)

    boo = cs.collections['boo']

    assert isinstance(boo.admin, AdminExtra)
    assert cs.admin is True
    assert [x.name for x in boo.admin.admin_list] == ['b', 'c']

    
def test_admin_plain_list():
    cs = _("""
    
        #boo
        ----------
        weight
        size_x
        size_y
        color_front
        color_back
        
        @admin(
            list: weight, size_x, size_y, color_front
        )
    
    """)

    boo = cs.collections['boo']

    assert isinstance(boo.admin, AdminExtra)
    assert cs.admin is True
    assert [x.name for x in boo.admin.admin_list] == ['weight', 'size_x', 'size_y', 'color_front']


def test_admin_exclude():
    cs = _("""
    
        #boo
        ----------
        weight
        size_x
        size_y
        color_front
        color_back
        
        @admin(
            list: *, ^color_front
        )
    
    """)

    boo = cs.collections['boo']

    assert isinstance(boo.admin, AdminExtra)
    assert cs.admin is True
    assert [x.name for x in boo.admin.admin_list] == ['weight', 'size_x', 'size_y', 'color_back']


def test_admin_exclude_wildcard():
    cs = _("""
    
        #boo
        ----------
        weight
        size_x
        size_y
        color_front
        color_back
        
        @admin(
            list: *, ^color_*
        )
    
    """)

    boo = cs.collections['boo']

    assert isinstance(boo.admin, AdminExtra)
    assert cs.admin is True
    assert [x.name for x in boo.admin.admin_list] == ['weight', 'size_x', 'size_y']


def test_admin_include_wildcard():
    cs = _("""
    
        #boo
        ----------
        weight
        size_x
        size_y
        color_front
        color_back
        
        @admin(
            list: weight, size_*
        )
    
    """)

    boo = cs.collections['boo']

    assert isinstance(boo.admin, AdminExtra)
    assert cs.admin is True
    assert [x.name for x in boo.admin.admin_list] == ['weight', 'size_x', 'size_y']


def test_admin_list():
    cs = _("""
    
        #boo
        ----------
        abc
        cda
        
        @admin(
            list: *
            read_only: *
            list_editable: *
            list_filter: *
            list_search: *
            fields: *
        )
    
    """)

    boo = cs.collections['boo']

    assert isinstance(boo.admin, AdminExtra)
    assert cs.admin is True
    assert [x.name for x in boo.admin.admin_list] == ['abc', 'cda']
    assert [x.name for x in boo.admin.read_only] == ['abc', 'cda']
    assert [x.name for x in boo.admin.list_editable] == ['abc', 'cda']
    assert [x.name for x in boo.admin.list_filter] == ['abc', 'cda']
    assert [x.name for x in boo.admin.list_search] == ['abc', 'cda']
    assert [x.name for x in boo.admin.fields] == ['abc', 'cda']


def test_admin_tabs_all():
    cs = _("""

        #boo
        ----------
        a
        b
        c

        @admin(
            tabs: foo(*)
        )

    """)

    boo = cs.collections['boo']

    assert boo.admin.tabs == ['foo']
    assert boo.admin.tab_names == {'foo': 'Foo'}
    assert boo.admin.tab_fields == {
        'a': 'foo',
        'b': 'foo',
        'c': 'foo',
    }

def test_admin_tabs_all_but_some():
    cs = _("""

        #boo
        ----------
        a
        b
        c
        d

        @admin(
            tabs: foo(*), lolo(b, d)
        )

    """)

    boo = cs.collections['boo']

    assert boo.admin.tabs == ['foo', 'lolo']
    assert boo.admin.tab_names == {'foo': 'Foo', 'lolo': 'Lolo'}
    assert boo.admin.tab_fields == {
        'a': 'foo',
        'b': 'lolo',
        'c': 'foo',
        'd': 'lolo',
    }


def test_admin_tabs_verbose_name():
    cs = _("""

        #boo
        ----------
        a
        b
        c

        @admin(
            tabs: foo "Фу"(*)
        )

    """)

    boo = cs.collections['boo']

    assert boo.admin.tabs == ['foo']
    assert boo.admin.tab_names == {'foo': 'Фу'}
    assert boo.admin.tab_fields == {
        'a': 'foo',
        'b': 'foo',
        'c': 'foo',
    }


def test_admin_tabs_left_to_general():
    cs = _("""

        #boo
        ----------
        a
        b
        c

        @admin(
            tabs: foo(b,c)
        )

    """)

    boo = cs.collections['boo']

    assert boo.admin.tabs == ['general', 'foo']
    assert boo.admin.tab_names == {'general': 'General', 'foo': 'Foo'}
    assert boo.admin.tab_fields == {
        'a': 'general',
        'b': 'foo',
        'c': 'foo',
    }


def test_admin_tabs_with_fields():
    cs = _("""

    #car
    -------
    nr
    mark
    model
    weight: int
    crashed: bool(true)
    painted: bool

    @admin(
        tabs: main(*), options(crashed, painted)
        fields: *, ^weight
    )

    """)

    boo = cs.collections['car']

    assert boo.admin.tabs == ['main', 'options']
    assert boo.admin.tab_fields == {
        'nr': 'main',
        'mark': 'main',
        'model': 'main',
        'crashed': 'options',
        'painted': 'options',
    }


def test_admin_inline_simple():
    cs = _("""
    
    #foo
    -------
    a
    b
    
    @admin(
        inline: lala
    )
    
    #bar
    --------
    rel: one(#foo -> lala)
    c
    d
    
    """)

    foo = cs.collections['foo']
    bar = cs.collections['bar']

    assert len(foo.admin.inlines) == 1
    inline = foo.admin.inlines[0]

    assert isinstance(inline, AdminInlineConfig)
    assert inline.extra_count == 0
    assert inline.collection == foo
    assert inline.target_collection == bar
    assert inline.inline_type == 'tabular'
    assert inline.inline_name == 'lala'
    assert inline.source_field_name == 'rel'
    assert inline.field_names == ['c', 'd']


def test_admin_inline_details():
    cs = _("""
    
    #foo
    -------
    a
    b
    
    @admin(
        inline: lala(
            type: stacked
            extra: 300
            fields: *, ^c
        )
    )
    
    #bar
    --------
    rel: one(#foo -> lala)
    c
    d
    
    """)

    foo = cs.collections['foo']
    bar = cs.collections['bar']

    assert len(foo.admin.inlines) == 1
    inline = foo.admin.inlines[0]

    assert isinstance(inline, AdminInlineConfig)
    assert inline.extra_count == 300
    assert inline.inline_type == 'stacked'
    assert inline.field_names == ['d']


def test_admin_inline_tab():
    cs = _("""
    
    #foo
    -------
    a
    b
    
    @admin(
        inline: lala(
            type: stacked
            extra: 300
            fields: *, ^c
        )
        tabs: main(*), other(lala)
    )
    
    #bar
    --------
    rel: one(#foo -> lala)
    c
    d
    
    """)

    foo = cs.collections['foo']
    bar = cs.collections['bar']

    assert len(foo.admin.inlines) == 1
    inline = foo.admin.inlines[0]
    assert inline.tab == 'other'

    assert foo.admin.tabs == ['main', 'other']
    assert foo.admin.tab_fields == {
        'a': 'main',
        'b': 'main',
        'lala': 'other',
    }


def test_admin_js_css():
    cs = _("""

    #foo
    -------
    a

    @admin(
        css: "foo.css", "another/boo.css"
        js: 
            "foo.js", 
            "another/boo.js"
    )

    """)

    foo = cs.collections['foo']

    assert foo.admin.css == [
        "foo.css", "another/boo.css"
    ]
    assert foo.admin.js == [
        "foo.js", "another/boo.js"
    ]