from flask.ext.assets import Environment, Bundle, ManageAssets
import yipit_static_assets


__all__ = 'manager',


class AssetsManager(object):

    def __init__(self, app):
        self.app = app
        self.env = Environment(app)
        self.env.url = app.static_url_path
        self.env.load_path.append(self.env.get_directory())
        self.env.load_path.append(yipit_static_assets.STATIC_ROOT)
        self.env.set_directory(None)

    def create_bundles(self):
        """Create static bundles and bind them to the `app`

        We are using flask-assets to manage our static stuff, so we just
        need to create named bundles that includes our css and js files.

        Currently, we have just two bundles: `main_css` and `main_js`.
        """
        self.env.register(
            'main_css',
                Bundle('components/bootstrap/css/bootstrap.css'),
                Bundle('sass/screen.scss', filters='compass,cssrewrite'),
            output='css/main.css', depends='sass/_*.scss',
        )

        self.env.register(
            'main_js',
            Bundle('components/bootstrap/js/bootstrap.js'),

            # Yipit specific stuff
            Bundle('js/yipit/index.js'),
        )

    def create_assets_command(self, manager):
        """Create the `assets` command in Flask-Script
        """
        manager.add_command('assets', ManageAssets(self.env))
