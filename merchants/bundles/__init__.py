from flask.ext.assets import Environment, Bundle


def create_bundles(app):
    """Create static bundles and bind them to the `app`

    We are using flask-assets to manage our static stuff, so we just
    need to create named bundles that includes our css and js files.

    Currently, we have just two bundles: `main_css` and `main_js`.
    """
    assets = Environment(app)
    assets.url = app.static_url_path

    assets.register(
        'main_css',
        Bundle(
            'screen.scss',
            filters='compass,cssrewrite',
            output='screen.css'),
        Bundle('components/bootstrap/css/bootstrap.css',
               'components/bootstrap/css/bootstrap-responsive.css'))

    assets.register(
        'main_js',
        Bundle('components/bootstrap/js/bootstrap.js'))
