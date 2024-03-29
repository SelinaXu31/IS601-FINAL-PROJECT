from flask import current_app as app
from flask_assets import Bundle


def compile_static_assets(assets):
    main_style_bundle = Bundle(
        'src/less/*.less',
        'main_bp/homepage.less',
        filters='less,cssmin',
        output='dist/css/landing.css',
        extra={'rel': 'stylesheet/css'}
    )
    main_js_bundle = Bundle(
        'src/js/main.js',
        filters='jsmin',
        output='dist/js/main.min.js'
    )

    admin_style_bundle = Bundle(
        'src/less/*.less',
        'admin_bp/admin.less',
        filters='less,cssmin',
        output='dist/css/account.css',
        extra={'rel': 'stylesheet/css'}
    )
    assets.register('main_styles', main_style_bundle)
    assets.register('main_js', main_js_bundle)
    assets.register('admin_styles', admin_style_bundle)
    if app.config['FLASK_ENV'] == 'development':
        main_style_bundle.build()
        main_js_bundle.build()
        admin_style_bundle.build()