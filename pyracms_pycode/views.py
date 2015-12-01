from pyracms.lib.helperlib import rapid_deform, redirect

from pyracms_pycode.deform_schemas.pycode import EditObjectSchema
from .lib.pycodelib import PyCodeLib
from pyramid.view import view_config
from io import StringIO
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import sys


def code_format(code):
    return highlight(code, PythonLexer(), HtmlFormatter(noclasses=True))

@view_config(route_name='pycode_show', renderer='pycode/pycode.jinja2')
@view_config(route_name='pycode_show_2', renderer='pycode/pycode.jinja2')
def show(context, request):
    p = PyCodeLib()
    a_id = request.matchdict.get('a_id')
    o_id = request.matchdict.get('o_id')
    object = None
    excepton = None
    result = ""
    if o_id:
        object = p.show_object(o_id)
        try:
            buffer = StringIO()
            sys.stdout = buffer
            eval(object.code)
            sys.stdout = sys.__stdout__
            result = buffer.getvalue()
        except Exception as e:
            excepton = e
    def object_update_submit(context, request, deserialized, bind_params):
        return redirect(request, "show_2", a_id=a_id, o_id=o_id)
    result_2 = rapid_deform(context, request, EditObjectSchema,
                            object_update_submit, object=object)
    result_2.update({'album': p.show_album(a_id), 'object': object, 'result':
                     result, 'exception': excepton, 'highlight': code_format})
    return result_2

@view_config(route_name='pycode_create', permission="group:admin")
def create_object(context, request):
    a_id = request.matchdict.get('a_id')
    p = PyCodeLib()
    p.create_object("Untitled code", "print('hello world')")
    return redirect(request, "show", a_id=a_id)

@view_config(route_name='pycode_delete_object', permission="group:admin")
def delete_object(context, request):
    a_id = request.matchdict.get('a_id')
    o_id = request.matchdict.get('o_id')
    p = PyCodeLib()
    p.delete_object(o_id)
    return redirect(request, "show", a_id=a_id)

@view_config(route_name='pycode_delete_album', permission="group:admin")
def delete_album(context, request):
    a_id = request.matchdict.get('a_id')
    p = PyCodeLib()
    p.delete_album(a_id)
    return redirect(request, "home")