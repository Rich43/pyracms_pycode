from colander import MappingSchema, SchemaNode, String
from deform.widget import TextAreaWidget, TextInputWidget

class EditAlbumSchema(MappingSchema):
    display_name = SchemaNode(String(), widget=TextInputWidget(size=40))
    description = SchemaNode(String(), widget=TextAreaWidget(cols=90, rows=20))

class EditObjectSchema(MappingSchema):
    display_name = SchemaNode(String(), widget=TextInputWidget(size=40))
    code = SchemaNode(String(), widget=TextAreaWidget(cols=80, rows=100))
