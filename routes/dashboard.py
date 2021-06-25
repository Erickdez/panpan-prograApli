from flask import session, render_template, redirect

class DashboardRoutes():
    @staticmethod
    def configure_routes(app):

        @app.route("/dashboard")
        def dashboard():
            if session.get("loggedIn"):
                email = session.get("login_email_client")
                return render_template("dashboard.html", email=email)
            else:
                return redirect("login")


        @app.route("/dashboardAdmin")
        def dashboardAdmin():
            if session.get("loggedIn"):
                email = session.get("login_email_admin")
                return render_template("dashboardAdmin.html", email=email)
            else:
                return redirect("login")