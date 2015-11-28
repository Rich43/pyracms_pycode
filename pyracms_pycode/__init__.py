def includeme(config):
    """ Activate the forum; usually called via
    ``config.include('pyracms_forum')`` instead of being invoked
    directly. """
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("pyracms_pycode:templates")
    config.scan("pyracms_pycode.views")