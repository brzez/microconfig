"""
usage:
@form(form, path)
def action(data):
    # handle data
"""
from modules.webserver import server, render_template


def render_input(id_attr, name, data, value):
    return '<input id="{id_attr}" type="{type}" name="{name}" value="{value}"/>'.format(
        id_attr=id_attr,
        type=data.get('type', 'text'),
        name=name,
        value=value
    )


def render_label(id_attr, name):
    return '<label for="{}">{}</label>'.format(id_attr, name)


def render_form(form_definition, data=None):
    data = data if data else dict()

    content = '<form method="post">'
    for name in form_definition:
        id_attr = 'form_{}'.format(name)
        content += '<div>'
        content += render_label(id_attr, name)
        content += render_input(id_attr, name, form_definition[name], data.get(name, ''))
        content += '</div>'
    content += '<input type="submit">'
    content += '</form>'

    return content


def form(path, form_definition, template=None):
    def wrap(f):
        def handle_get(request, response):
            content = render_form(form_definition, request.data)

            if template:
                content = render_template(template, form=content)
            elif callable(template):
                content = template(content, request, response)

            response.content = content


        def handle_post(request, response):
            f(request.data)
            handle_get(request, response)

        server.router.register(path, 'get', handle_get)
        server.router.register(path, 'post', handle_post)

    return wrap
