from flask import render_template

class MainRoutes():
    @staticmethod
    def configure_routes(app):

        @app.route("/")
        def home():
            return render_template("index.html")
