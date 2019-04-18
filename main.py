from microconfig import init


def test():
    init()

# from webserver.form import form
# from webserver import redirect, route, render_template, runserver
#
# from machine import Pin
#
# d2 = Pin(4, Pin.OUT)
#
#
# @route('/')
# def get_index(request, response):
#     response.content = render_template('page.html')
#
#
# @route('/on')
# def get_on(request, response):
#     d2.value(1)
#     response.content = 'on' + redirect('/')
#
#
# @route('/off')
# def get_on(request, response):
#     d2.value(0)
#     response.content = 'off' + redirect('/')
#
#
# @form('/form', dict(
#     name=dict(type='text'),
#     password=dict(type='password'),
# ), 'form.html')
# def handle_form(data):
#     print('form', data)
