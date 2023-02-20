{% extends "mail_templated/base.tpl" %}

{% block subject %}
Account Verification
{% endblock %}

{% block html %}
<form action="http://127.0.0.1:8000/accounts/api/v1/activation/confirm/{{ token }}/" method="get">
    <input type="submit" value="Confirm">
</form>
{% endblock %}
