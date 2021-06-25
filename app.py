from flask import Flask, render_template, request, redirect, session
from routes.main import MainRoutes
from routes.register import RegisterRoutes
from routes.log_process import LogProcessRoutes
from routes.dashboard import DashboardRoutes
import bcrypt

app = Flask(__name__)
app.secret_key = "Bad1secret2key3!+"


MainRoutes.configure_routes(app)
RegisterRoutes.configure_routes(app)
LogProcessRoutes.configure_routes(app)
DashboardRoutes.configure_routes(app)


if __name__ == "__main__":
    app.run(debug=True)
