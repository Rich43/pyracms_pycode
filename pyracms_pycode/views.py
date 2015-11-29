from .lib.pycodelib import PyCodeLib
from pyramid.view import view_config

@view_config(route_name='show_album', renderer='gallery/pycode.jinja2')
def show_album(context, request):
    g = PyCodeLib()
    a_id = request.matchdict.get('a_id')
    return {'album': g.show_album(a_id)}