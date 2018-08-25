{{ imports }}

{% for cname, col in collections %}
{% for rest_conf in col.rest_conf.values() %}
{% include 'serializer.py.tpl' %}
{% endfor %}
{% endfor %}

index = {
{%- for cname, col in collections %}
    {{ col.class_name }}: {
        {%- for name, rest_conf in col.rest_conf.items() %}
        '{{ name }}': {{ rest_conf.serializer_name }}Serializer,
        {%- endfor %}
    },
{% endfor -%}
}

