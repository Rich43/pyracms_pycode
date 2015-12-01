from colander import MappingSchema, SchemaNode, String, Schema
from deform import FileData
from deform.widget import TextAreaWidget, TextInputWidget, FileUploadWidget


class EditAlbumSchema(MappingSchema):
    display_name = SchemaNode(String(), widget=TextInputWidget(size=40))
    description = SchemaNode(String(), widget=TextAreaWidget(cols=90, rows=20))

class EditObjectSchema(MappingSchema):
    display_name = SchemaNode(String(), widget=TextInputWidget(size=40))
    code = SchemaNode(String(), widget=TextAreaWidget(cols=80, rows=25))

class MemoryTmpStore(dict):
    """ Instances of this class implement the
    :class:`deform.interfaces.FileUploadTempStore` interface"""
    def preview_url(self, uid):
        return None

tmpstore = MemoryTmpStore()

class CodeUploadSchema(Schema):
    python_code_file = SchemaNode(FileData(), widget=FileUploadWidget(tmpstore))