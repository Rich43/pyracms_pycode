from pyracms.lib.menulib import MenuLib
from pyracms.models import DBSession, Base
from pyramid.paster import get_appsettings, setup_logging
from ..lib.pycodelib import PyCodeLib
from sqlalchemy import engine_from_config
import os
import sys
import transaction

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        p = PyCodeLib()
        album = p.create_album("Dummy Album", "This is a test")
        for i in range(5):
            album.objects.append(p.create_object("Dummy Code %s" % i,
                                                 "print('hello world')"))

        m = MenuLib()
        group = m.show_group("admin_area")
        m.add_menu_item_route("Add Code Album", "pycode_create_album", 40,
                              group, 'group:admin')