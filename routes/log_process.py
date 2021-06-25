from flask import request, render_template, redirect, session
from logic.client_logic import ClientLogic
from logic.admin_logic import AdminLogic
import bcrypt

class LogProcessRoutes():
    @staticmethod
    def configure_routes(app):

        @app.route("/login", methods=["GET", "POST"])
        def login():
            if request.method == "GET":
                return render_template("login.html")
            elif request.method == "POST":
                logic = ClientLogic()
                clientEmail = request.form["email"]
                passwd = request.form["passwd"]
                clientDict = logic.getClientByEmail(clientEmail)

                if clientDict == []:
                    logic = AdminLogic()
                    adminEmail = request.form["email"]
                    passwd = request.form["passwd"]
                    adminDict = logic.getAdminByEmail(clientEmail)
                    salt = adminDict["salt"].encode("utf-8")
                    hashPasswd = bcrypt.hashpw(passwd.encode("utf-8"), salt)
                    dbPasswd = adminDict["password"].encode("utf-8")
                else:
                    salt = clientDict["salt"].encode("utf-8")
                    hashPasswd = bcrypt.hashpw(passwd.encode("utf-8"), salt)
                    dbPasswd = clientDict["password"].encode("utf-8")

                if hashPasswd == dbPasswd:
                    if clientDict == []:
                        session["login_email_admin"] = clientEmail
                        session["loggedIn"] = True
                        return redirect("dashboardAdmin")
                    else:
                        session["login_email_client"] = clientEmail
                        session["loggedIn"] = True
                        return redirect("dashboard")
                else:
                    return redirect("login")

        @app.route("/logout")
        def logout():
            if session.get("loggedIn") and session.get("login_email_client") is not None:
                session.pop("login_email_client")
                session.pop("loggedIn")
                return redirect("login")
            elif session.get("loggedIn") and session.get("login_email_admin") is not None:
                session.pop("login_email_admin")
                session.pop("loggedIn")
                return redirect("login")
            else:
                return redirect("login")