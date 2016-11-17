from datetime import datetime
from pyracms.models import Base, User
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.expression import desc
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime, Boolean

class CodeObject(Base):
    __tablename__ = 'codeobject'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)
    display_name = Column(Unicode(128), index=True, nullable=False)
    code = Column(UnicodeText, default='')
    result = Column(UnicodeText, default='')
    render = Column(Boolean, default=True)
    created = Column(DateTime, default=datetime.now)
    album_id = Column(Integer, ForeignKey('codealbum.id'), nullable=False)
    album = relationship("CodeAlbum")

class CodeAlbum(Base):
    __tablename__ = 'codealbum'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)
    display_name = Column(Unicode(128), index=True, nullable=False)
    description = Column(UnicodeText, default='')
    created = Column(DateTime, default=datetime.now)
    objects = relationship(CodeObject, cascade="all, delete, delete-orphan",
                           lazy="dynamic", order_by=CodeObject.display_name)

