from flask import request, render_template, redirect
from logic.client_logic import ClientLogic
import bcrypt

class RegisterRoutes():
    @staticmethod
    def configure_routes(app):

        @app.route("/register", methods=["GET", "POST"])
        def register():
            if request.method == "GET":
                return render_template("register.html")
            elif request.method == "POST":
                logic = ClientLogic()
                clientName = request.form["clientname"]
                clientEmail = request.form["clientemail"]
                clientCel = request.form["clientcel"]
                passwd = request.form["passwd"]
                confpasswd = request.form["confpasswd"]
                if passwd == confpasswd:
                    salt = bcrypt.gensalt(rounds=14)
                    strSalt = salt.decode("utf-8")
                    encPasswd = passwd.encode("utf-8")
                    hashPasswd = bcrypt.hashpw(encPasswd, salt)
                    strPasswd = hashPasswd.decode("utf-8")
                    rows = logic.insertClient(clientName, clientEmail, clientCel,strPasswd, strSalt)
                    return redirect("login")
                else:
                    return redirect("register")