# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from elasticsearch_dsl.connections import connections
from flask import Flask, render_template
from flask_jsglue import JSGlue

from flaskexpenses import public, user, transactions
from flaskexpenses.assets import assets
from flaskexpenses.extensions import bcrypt, cache, csrf_protect, db, debug_toolbar, login_manager, migrate
from flaskexpenses.settings import ProdConfig
from flaskexpenses.transactions.models import Trx


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    
    connections.create_connection(hosts=[config_object.ELASTICSEARCH], timeout=20)
    Trx.init()
    
    return app


def register_extensions(app):
    """Register Flask extensions."""
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    
    jsglue = JSGlue()
    jsglue.init_app(app)
    
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(transactions.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
