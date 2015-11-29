from .lib.pycodelib import PyCodeLib
from pyramid.view import view_config

@view_config(route_name='show', renderer='pycode/pycode.jinja2')
@view_config(route_name='show_2', renderer='pycode/pycode.jinja2')
def show(context, request):
    g = PyCodeLib()
    a_id = request.matchdict.get('a_id')
    o_id = request.matchdict.get('o_id')
    object = None
    if o_id:
        object = g.show_object(o_id)
    return {'album': g.show_album(a_id), 'object': object}