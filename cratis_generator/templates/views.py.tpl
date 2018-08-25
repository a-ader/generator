{{ imports }}
{{ collection_set.page_imports }}

if '_' not in locals():
    _ = lambda s: s

{% for cname, col in collections %}
{% for rest_conf in col.published_apis.values() %}

{% if rest_conf.auth_methods.token %}
class {{ col.class_name }}TokenAuthentication(TokenAuthentication):
    model = {{ rest_conf.auth_methods.token.model }}
{% endif %}

class {{ rest_conf.serializer_name }}ViewSet({{ rest_conf.rest_class[1] }}):
    """
    {{ col.class_name }} API
    """

    filter_fields = ['{{ rest_conf.field_names|join("','") }}']
    serializer_class = {{ rest_conf.serializer_name }}Serializer
    permission_classes = [{% if rest_conf.auth_methods %}IsAuthenticated{% else %}AllowAny{% endif %}]
    authentication_classes = [{{ rest_conf.auth_method_classes|join(', ') }}]

    def get_queryset(self):
        return {{ col.class_name }}.objects.{{ rest_conf.query }}{% if rest_conf.user_field %}.filter({{ rest_conf.user_field }}=self.request.user){% endif %}{% if rest_conf.annotations %}.annotate({{ rest_conf.annotations|join(", ") }}){% endif %}
{% endfor %}
{% endfor %}
{%- if collection_set.react %}
rs = ZmeiReactServer()
rs.load(settings.BASE_DIR + '/app/static/react/{{ collection_set.app_name }}_server.bundle.js')
{% endif -%}
{% for page in pages %}
class {{ page.view_name }}({% if page.extra_bases %}{{ page.extra_bases|join(", ") }}, {% endif %}{{ page.parent_view_name }}):
    {% if page.options %}{% for key, option in page.options.items() %}{{ key }} = {{ option }}
    {% endfor %}{% endif %}{% if page.react %}
    react_server = rs
    react_components = {{ page.react_component_names|repr }}
    {% endif %}{% if page.methods %}{% for key, method_code in page.methods.items() %}
    def {{ key }}(self, *args, **kwargs):
        {{ page.render_method_expr(method_code)|indent(8) }}
    {% endfor %}{% endif -%}
    {%- if page.has_sitemap %}
    @classmethod
    def get_sitemap(cls):
        return {{ page.sitemap_expr.render_python_code() }}
    {% endif %}
    {{ page.render_template_name_expr()|indent(4) }}
    {% set code=page.render_page_code() %}{% if code or page.page_item_names %}
    def get_data(self, url, request, inherited):
        {%- if page.parent_name %}
        data = super().get_data(url, request, inherited)
        {% else %}
        data = {}
        {% endif %}
        {%- if code %}{{ code|indent(8) }}{% endif %}
        {%- if page.page_item_names %}
        data.update({ {% for key in (page.page_item_names) %}'{{ key }}': {{ key }}{% if not loop.last %}, {% endif %}{% endfor %} })
        {% endif %}
        return data
    {% endif %}

    {% if page.allow_post %}
    post = {{ page.parent_view_name }}.get
    {% endif %}
{% if page.name == 'global' %}
def global_context(request):
    return GlobalView(request=request, kwargs={}, args=[]).get_context_data()
{% endif %}

{% if page.handlers %}
from django.conf import urls
{% for handler_code in page.handlers %}
from django.conf.urls import handler{{ handler_code }}
handler_{{ handler_code }}_view = {{ page.view_name }}.as_view()
setattr(urls, 'handler{{ handler_code }}', '{{ collection_set.app_name }}.views.handler_{{ handler_code }}_view')
{% endfor %}
{% endif %}

{% endfor %}