{% extends "mail_templated/base.tpl" %}

{% block subject %}
Account Verification
{% endblock %}

{% block html %}
{{ token }}
{% endblock %}
