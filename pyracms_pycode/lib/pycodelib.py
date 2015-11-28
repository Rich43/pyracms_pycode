from sqlalchemy.orm.exc import NoResultFound

from ..models import CodeAlbum, CodeObject
from pyracms.models import DBSession

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
        DBSession.flush()
        return object

    def show_object(self, o_id):
        try:
            return DBSession.query(CodeObject).filter_by(id=o_id).one()
        except NoResultFound:
            return None

    def delete_object(self, o_id):
        DBSession.delete(self.show_object(o_id))