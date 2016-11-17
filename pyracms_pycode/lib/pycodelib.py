from sqlalchemy.orm.exc import NoResultFound

from ..models import CodeAlbum, CodeObject
from pyracms.models import DBSession
import re

def sort_nicely(l): 
    """Sort the given list in the way that humans expect. """ 
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = (lambda key: [ convert(c) 
                    for c in re.split('([0-9]+)', key[1]) ])
    return sorted(l, key=alphanum_key)

class PyCodeLib:
    def create_album(self, display_name, description):
        album = CodeAlbum()
        album.display_name = display_name
        album.description = description
        DBSession.add(album)
        DBSession.flush()
        return album

    def show_album(self, a_id):
        try:
            return DBSession.query(CodeAlbum).filter_by(id=a_id).one()
        except NoResultFound:
            return None

    def delete_album(self, a_id):
        DBSession.delete(self.show_album(a_id))

    def create_object(self, display_name, code):
        object = CodeObject()
        object.display_name = display_name
        object.code = code
        DBSession.add(object)
        return object

    def show_object(self, o_id):
        try:
            return DBSession.query(CodeObject).filter_by(id=o_id).one()
        except NoResultFound:
            return None

    def delete_object(self, o_id):
        DBSession.delete(self.show_object(o_id))

    def list_objects(self, a_id):
        album = self.show_album(a_id)
        sort_objs = [[object.id, object.display_name] 
                      for object in album.objects]
        sort_objs = sort_nicely(sort_objs)
        return sort_objs
