from flask import Flask, jsonify,  render_template
from flask_restful import Api
from flask_cors import CORS

import app_config as config


def create_app(config_name):
    """Create a flask application with certain configuration"""

    app = Flask(__name__)
    api = Api(app)
    CORS(app)

    app.config.from_object(config.configurations[config_name])
    """This ensures that the urls /login and /login/ are recognized as same
    without considering the trailing slash """
    app.url_map.strict_slashes = False

    with app.app_context():
        from app.resources.products import MenuResource
        from app.resources.orders import OrderResource
        from app.resources.addresses import AddressResource
        from app.resources.users import LoginResource, SignUpResource
    api.add_resource(MenuResource, "/api/v1/menu", "/api/v1/menu/<int:product_id>")
    api.add_resource(OrderResource, "/api/v1/orders",
                     "/api/v1/orders/<int:order_id>")
    api.add_resource(AddressResource, "/api/v1/addresses",
                     "/api/v1/addresses/<int:address_id>")
    api.add_resource(LoginResource, "/api/v1/auth/login")
    api.add_resource(SignUpResource, "/api/v1/auth/signup")

    @app.errorhandler(404)
    def error_404(e):
        return jsonify({"code": "404", "message": "Not found"}), 200

    @app.errorhandler(500)
    def error_500(e):
        return jsonify(
            {"code": "503", "message": "We have some trouble"
                                       "processing your request"
                                       " please try again later"}), 500

    @app.errorhandler(405)
    def error_405(e):
        return jsonify({"code": "405", "message": "We dont allow"
                                                  " the request method",
                        "ok": False}), 200

    @app.route("/")
    def home():
        return render_template("index.html")

    return app
