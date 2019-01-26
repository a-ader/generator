from textwrap import dedent

from zmei_generator.contrib.drf.extras.model.api import ApiModelExtra
from zmei_generator.contrib.drf.extras.model.rest import RestModelExtra, RestSerializerConfig
from zmei_generator.parser.parser import ZmeiParser


def _(code):
    parser = ZmeiParser()
    parser.parse_string(dedent(code))
    return parser.populate_application('example')


def test_rest_empty():
    app = _("""
    
        #boo
        ----------
        abc
        cda
        
        @rest
    
    """)

    boo = app.models['boo']

    assert isinstance(boo.rest, RestModelExtra)
    assert isinstance(boo.rest_conf['_'], RestSerializerConfig)

    assert app.rest is True
    assert boo.rest in app.extras

    assert boo.rest_conf['_'].serializer_name == boo.class_name
    assert boo.rest_conf['_'].parent_field is None


def test_rest_descriminator():
    app = _("""
    
        #boo
        ----------
        abc
        cda
        
        @rest.foo
    
    """)

    boo = app.models['boo']

    assert isinstance(boo.rest, RestModelExtra)
    assert isinstance(boo.rest_conf['foo'], RestSerializerConfig)

    assert app.rest is True
    assert boo.rest in app.extras

    assert boo.rest_conf['foo'].serializer_name == boo.class_name + 'Foo'


def test_rest_discriminator_multiple():
    app = _("""
    
        #boo
        ----------
        abc
        cda
        
        @rest
        @rest.foo
    
    """)

    boo = app.models['boo']

    assert boo.rest_conf['_'].serializer_name == boo.class_name
    assert boo.rest_conf['foo'].serializer_name == boo.class_name + 'Foo'


def test_rest_fields_field_names():
    app = _("""
    
        #boo
        ----------
        abc
        cda
        
        @rest(
            fields: *
        )   
        @rest.boo
        @rest.one(
            fields: cda
        )
    
    """)

    boo = app.models['boo']

    assert boo.rest_conf['_'].descriptor == '_'
    assert boo.rest_conf['_'].descriptor_suffix == ''
    assert boo.rest_conf['_'].model == boo

    assert boo.rest_conf['boo'].descriptor == 'boo'
    assert boo.rest_conf['boo'].descriptor_suffix == '_boo'
    assert boo.rest_conf['boo'].model == boo

    assert boo.rest_conf['one'].descriptor == 'one'
    assert boo.rest_conf['one'].descriptor_suffix == '_one'
    assert boo.rest_conf['boo'].model == boo

    assert [x.name for x in boo.rest_conf['_'].fields] == ['abc', 'cda']
    assert [x.name for x in boo.rest_conf['boo'].fields] == ['abc', 'cda']
    assert [x.name for x in boo.rest_conf['one'].fields] == ['cda']

    print(boo.rest_conf['_'].field_names)
    print(boo.rest_conf['boo'].field_names)
    print(boo.rest_conf['one'].field_names)

    assert boo.rest_conf['_'].field_names == ['id', 'abc', 'cda']
    assert boo.rest_conf['boo'].field_names == ['id', 'abc', 'cda']
    assert boo.rest_conf['one'].field_names == ['id', 'cda']


def test_rest_fields_read_only():
    app = _("""

        #boo
        ----------
        abc
        cda
        efg

        @rest(
            fields: *
            read_only: *, ^abc
        )   
        @rest.default(
            fields: *
        )

    """)

    boo = app.models['boo']

    assert [x.name for x in boo.rest_conf['_'].fields] == ['abc', 'cda', 'efg']
    assert boo.rest_conf['_'].read_only_fields == ['cda', 'efg']


def test_rest_fields_simple():
    app = _("""
    
        #boo
        ----------
        cat
        dog
        bird
        
        @rest(
            fields: *
        )
    
    """)

    boo = app.models['boo']

    assert boo.rest_conf['_'].field_names == ['id', 'cat', 'dog', 'bird']


def test_rest_i18n():
    app = _("""

        #boo
        ----------
        abc
        cda

        @rest.yes(
            i18n: true
        )
        @rest.no(
            i18n: false
        )
        @rest.default()

    """)

    boo = app.models['boo']

    assert boo.rest_conf['yes'].i18n is True
    assert boo.rest_conf['no'].i18n is False
    assert boo.rest_conf['default'].i18n is False


def test_rest_mode():
    app = _("""

        #boo
        ----------
        abc
        cda

        @rest.r(
            fields: * [r]
        )
        @rest.rw(
            fields: * [rw]
        )
        @rest.w(
            fields: * [w]
        )
        @rest.default()

    """)

    boo = app.models['boo']

    assert boo.rest_conf['r'].rest_mode == 'r'
    assert boo.rest_conf['rw'].rest_mode == 'rw'
    assert boo.rest_conf['w'].rest_mode == 'w'
    assert boo.rest_conf['default'].rest_mode == 'r'


def test_user_field():
    app = _("""

        #boo
        ----------
        abc
        cda

        @rest.yes(
            user_field: abc
        )
        @rest.default()

    """)

    boo = app.models['boo']

    assert boo.rest_conf['default'].user_field is None
    assert boo.rest_conf['yes'].user_field == 'abc'


def test_query():
    app = _("""

        #boo
        ----------
        abc
        cda

        @rest.yes(
            query := filter(a=123)
        )
        @rest.default()

    """)

    boo = app.models['boo']

    assert boo.rest_conf['default'].query == 'all()'
    assert boo.rest_conf['yes'].query == 'filter(a=123)'


def test_on_create():
    app = _("""

        #boo
        ----------
        abc
        cda

        @rest.yes(
            on_create {
                3 + 3 = 4
            }
        )

        @rest.inline(
            on_create := some()
        )
        @rest.default()

    """)

    boo = app.models['boo']

    assert boo.rest_conf['default'].on_create == ''
    assert boo.rest_conf['yes'].on_create == '3 + 3 = 4'
    assert boo.rest_conf['inline'].on_create == 'some()'


def test_filter_in():
        app = _("""

            #boo
            ----------
            abc
            cda

            @rest.yes(
                filter_in {
                    3 + 3 = 4
                }
            )

            @rest.inline(
                filter_in := some()
            )
            @rest.default()

        """)

        boo = app.models['boo']

        assert boo.rest_conf['default'].filter_in == ''
        assert boo.rest_conf['yes'].filter_in == '3 + 3 = 4'
        assert boo.rest_conf['inline'].filter_in == 'some()'


def test_filter_out():
        app = _("""

            #boo
            ----------
            abc
            cda

            @rest.yes(
                filter_out {
                    3 + 3 = 4
                }
            )

            @rest.inline(
                filter_out := some()
            )
            @rest.default()

        """)

        boo = app.models['boo']

        assert boo.rest_conf['default'].filter_out == ''
        assert boo.rest_conf['yes'].filter_out == '3 + 3 = 4'
        assert boo.rest_conf['inline'].filter_out == 'some()'


def test_auth():
    app = _("""
    
        #my_token
        -----------
        lala

        #boo
        ----------
        abc
        cda

        @rest.yes(
            auth(basic,session,token: #my_token)
        )
        @rest.default()

    """)

    boo = app.models['boo']

    assert boo.rest_conf['default'].auth_method_classes == []
    assert boo.rest_conf['default'].auth_methods == {}

    assert boo.rest_conf['yes'].auth_method_classes == [
        'BasicAuthentication', 'SessionAuthentication', 'BooYesTokenAuthentication']

    assert boo.rest_conf['yes'].auth_methods == {
        'basic': {},
        'session': {},
        'token': {'model': 'MyToken'},
    }


def test_inline():
    app = _("""

        #other
        -----------
        lala1
        lala2
        lala3

        #boo
        ----------
        abc: one(#other)
        cda

        @rest(
            inline: abc(
                fields: *, ^lala2
            )
        )
    """)

    boo = app.models['boo']

    assert 'abc' in boo.rest_conf['_'].inlines
    assert len(boo.rest_conf['_'].extra_serializers) == 1

    assert [x.name for x in boo.rest_conf['_'].extra_serializers[0].fields] == ['lala1', 'lala3']

def test_inline_default():
    app = _("""

        #other
        -----------
        lala1
        lala2
        lala3

        #boo
        ----------
        abc: one(#other)
        cda

        @rest(
            inline: abc()
        )
    """)

    boo = app.models['boo']

    assert 'abc' in boo.rest_conf['_'].inlines
    assert len(boo.rest_conf['_'].extra_serializers) == 1

    assert [x.name for x in boo.rest_conf['_'].extra_serializers[0].fields] == ['lala1', 'lala2', 'lala3']


def test_annotate():
    app = _("""
    
        #item
        ---------
        lala

        #boo
        ----------
        items: many(#item)

        @rest(
            annotate: count items as item_count
        )
    """)

    boo = app.models['boo']

    assert boo.rest_conf['_'].field_names == ['id', 'item_count', 'items']


def test_publish_default():
    app = _("""
    
        #boo
        ----------
        foo
        
        @api
        @rest
    """)

    boo = app.models['boo']

    assert app.api is True
    assert isinstance(boo.api, ApiModelExtra)

    assert list(boo.published_apis.keys()) == ['_']


def test_publish_by_name():
    app = _("""
    
        #boo
        ----------
        foo
        
        @api(foo, boo)
        @rest
        @rest.foo
        @rest.boo
    """)

    boo = app.models['boo']

    assert app.api is True
    assert isinstance(boo.api, ApiModelExtra)

    assert list(boo.published_apis.keys()) == ['foo', 'boo']


def test_publish_default_one():
    app = _("""
    
        #boo
        ----------
        foo
        
        @api
        @rest
        @rest.foo
        @rest.boo
    """)

    boo = app.models['boo']

    assert app.api is True
    assert isinstance(boo.api, ApiModelExtra)

    assert list(boo.published_apis.keys()) == ['_']


def test_publish_all():
    app = _("""
    
        #boo
        ----------
        foo
        
        @api(*)
        @rest
        @rest.foo
        @rest.boo
    """)

    boo = app.models['boo']

    assert app.api is True
    assert isinstance(boo.api, ApiModelExtra)

    assert list(boo.published_apis.keys()) == ['_', 'foo', 'boo']
