def includeme(config):
    """ Activate the forum; usually called via
    ``config.include('pyracms_forum')`` instead of being invoked
    directly. """
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("pyracms_pycode:templates")
    config.add_route('pycode_show', '/pycode/{a_id:\d+}')
    config.add_route('pycode_show_2', '/pycode/{a_id:\d+}/{o_id:\d+}')
    config.add_route('pycode_create_object', '/pycode/create_code/{a_id:\d+}')
    config.add_route('pycode_delete_object', '/pycode/delete_code/{'
                                             'a_id:\d+}/{o_id:\d+}')
    config.add_route('pycode_create_album', '/pycode/create_album')
    config.add_route('pycode_update_album', '/pycode/update_album/{a_id:\d+}')
    config.add_route('pycode_delete_album', '/pycode/delete_album/{a_id:\d+}')
    config.scan("pyracms_pycode.views")
