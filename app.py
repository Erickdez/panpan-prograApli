from flask import Flask, render_template, request, redirect, session
from logic.client_logic import ClientLogic
from logic.admin_logic import AdminLogic
import bcrypt

app = Flask(__name__)
app.secret_key = "Bad1secret2key3!+"


@app.route("/")
def home():
    return render_template("index.html")


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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        logic = ClientLogic()
        clientEmail = request.form["clientemail"]
        passwd = request.form["passwd"]
        clientDict = logic.getClientByEmail(clientEmail)

        if clientDict == []:
            logic = AdminLogic()
            adminEmail = request.form["clientemail"]
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
    if session.get("loggedIn"):
        session.pop("login_email")
        session.pop("login_name")
        session.pop("loggedIn")
        return redirect("login")
    else:
        return redirect("login")


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


if __name__ == "__main__":
    app.run(debug=True)
