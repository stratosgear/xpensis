# -*- coding: utf-8 -*-
"""Application assets."""
from flask_assets import Bundle, Environment

css = Bundle(
    'libs/bootstrap/dist/css/bootstrap.css',
    'libs/select2/dist/css/select2.min.css',
    'libs/font-awesome4/css/font-awesome.min.css',
    'libs/bootstrap-select2/select2-bootstrap.css',
    'libs/eonasdan-bootstrap-datetimepicker/build/css/bootstrap-datetimepicker.min.css',
    'css/style.css',
    filters='cssmin',
    output='public/css/common.css'
)

js = Bundle(
    'libs/jQuery/dist/jquery.js',
    'libs/bootstrap/dist/js/bootstrap.js',
    'libs/select2/dist/js/select2.full.min.js',
    'libs/moment/min/moment.min.js',
    'libs/eonasdan-bootstrap-datetimepicker/build/js/bootstrap-datetimepicker.min.js',
    'js/plugins.js',
    filters='jsmin',
    output='public/js/common.js'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)

