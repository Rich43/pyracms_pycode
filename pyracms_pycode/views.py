from pyracms.lib.helperlib import rapid_deform, redirect

from pyracms_pycode.deform_schemas.pycode import (EditObjectSchema,
                                                  EditAlbumSchema,
                                                  CodeUploadSchema)
from .lib.pycodelib import PyCodeLib
from pyramid.view import view_config
from io import StringIO
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from os.path import splitext, split
import sys
import zipfile

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
    result_2 = {}
    if request.has_permission("group:admin"):
        def code_upload_submit(context, request, deserialized, bind_params):
            file_obj = deserialized.get('python_code_file')
            if file_obj:
                album = p.show_album(a_id)
                if file_obj['mimetype'] == 'text/x-python':
                    title = splitext(file_obj['filename'])[0]
                    data = file_obj['fp'].read().decode()
                    album.objects.append(p.create_object(title, data))

                if file_obj['mimetype'] == 'application/zip':
                    zip = zipfile.ZipFile(file_obj['fp'])
                    for file_name in zip.namelist():
                        path_split = splitext(file_name)
                        if path_split[1].lower() == ".py":
                            title = split(path_split[0])[-1]
                            data = zip.open(file_name).read().decode()
                            album.objects.append(p.create_object(title, data))

            return redirect(request, "pycode_show", a_id=a_id)
        rap_def = rapid_deform(context, request, CodeUploadSchema,
                               code_upload_submit, form_name='code_upload',
                               submit_name='upload file')
        if isinstance(rap_def, dict):
            result_2.update(rap_def)
        else:
            return rap_def
    if o_id:
        object = p.show_object(o_id)
        try:
            buffer = StringIO()
            sys.stdout = buffer
            exec(object.code)
            sys.stdout = sys.__stdout__
            result = buffer.getvalue()
        except Exception as e:
            excepton = e
        def object_update_submit(context, request, deserialized, bind_params):
            if (request.has_permission("group:admin") and
                    deserialized.get('display_name') and
                    deserialized.get('code')):
                object = bind_params['object']
                object.display_name = deserialized['display_name']
                object.code = deserialized['code']
            return redirect(request, "pycode_show_2", a_id=a_id, o_id=o_id)
        rap_def = rapid_deform(context, request, EditObjectSchema,
                               object_update_submit, object=object,
                               display_name=object.display_name,
                               code=object.code)
        if isinstance(rap_def, dict):
            result_2.update(rap_def)
        else:
            return rap_def
    result_2.update({'album': p.show_album(a_id), 'object': object,
                     'result': result, 'exception': excepton,
                     'highlight': code_format})
    return result_2

@view_config(route_name='pycode_create_object', permission="group:admin")
def create_object(context, request):
    a_id = request.matchdict.get('a_id')
    p = PyCodeLib()
    album = p.show_album(a_id)
    album.objects.append(p.create_object("Untitled code",
                                         "print('hello world')"))
    return redirect(request, "pycode_show", a_id=a_id)

@view_config(route_name='pycode_delete_object', permission="group:admin")
def delete_object(context, request):
    a_id = request.matchdict.get('a_id')
    o_id = request.matchdict.get('o_id')
    p = PyCodeLib()
    p.delete_object(o_id)
    return redirect(request, "pycode_show", a_id=a_id)

@view_config(route_name='pycode_create_album', renderer='deform.jinja2',
             permission="group:admin")
@view_config(route_name='pycode_update_album', renderer='deform.jinja2',
             permission="group:admin")
def create_update_album(context, request):
    a_id = request.matchdict.get('a_id')
    display_name, description = ("", "")
    p = PyCodeLib()
    if a_id:
        album = p.show_album(a_id)
        display_name = album.display_name
        description = album.description

    def crupdate_album_submit(context, request, deserialized, bind_params):
        if not a_id:
            album = p.create_album(deserialized['display_name'],
                                   deserialized['description'])
        else:
            album = p.show_album(a_id)
            album.display_name = deserialized['display_name']
            album.description = deserialized['description']
        return redirect(request, "pycode_show", a_id=album.id)
    result = rapid_deform(context, request, EditAlbumSchema,
                          crupdate_album_submit, a_id=a_id,
                          display_name=display_name, description=description)
    if isinstance(result, dict):
        word = "Create"
        if a_id: word = "Update"
        message = "%s Album" % word
        result.update({"title": message, "header": message})
    return result

@view_config(route_name='pycode_delete_album', permission="group:admin")
def delete_album(context, request):
    a_id = request.matchdict.get('a_id')
    p = PyCodeLib()
    p.delete_album(a_id)
    return redirect(request, "home")

