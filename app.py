from datetime import datetime
import random

from flask import (Response, flash, redirect, render_template, request,
                   send_from_directory, session, url_for)
from project_engine import app, yaml_data, mail

secure_type="http"


@app.route("/", methods=["GET", "POST"])
def home():
    """
    That function was register for new user
    """

    try:
        return render_template("index.html")

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return render_template("index.html")

# That is route for register page and save customer data
@app.route("/register", methods=["GET","POST"])
def register():
    """
    That function was register for new user
    """

    try:
        if request.method=="POST":
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]
            address = request.form["address"]
            username = request.form["username"]
            pwd = request.form["pwd"]
            re_pwd = request.form["re_pwd"]

            if pwd == re_pwd:
                db_payload = {
                    "query_type": "SELECT_OPERATION",
                    "query_string": db_constants.GET_DATA.format(table_name="register_user")
                }

                all_response = DatabaseQuery.execute_query(json_obj=db_payload)

                all_username = [data[5] for data in all_response]
                if username in all_username:
                    flash("Username is already availble!!!! Please try with another username....")
                    return redirect(url_for('register', _external=True, _scheme=secure_type))
                else:
                    session["dash_permission"] = ["default"]
                    session["prod_permission"] = "Starter"
                    session["username"] = username
                    created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

                    db_payload = {
                        "query_type": "INSERT_OPERATION",
                        "query_string": db_constants.ADD_CUSTOMER_DATA.format(nlp_database_name="dev_db_main",
                                                                           table_name="register_user"),
                        "query_parameter": (name, email, phone, address, username, pwd, session.get("dash_permission",""), session.get("prod_permission",""), created_on, updated_on)
                    }

                    DatabaseQuery.execute_query(json_obj=db_payload)

                    db_payload = {
                        "query_type": "INSERT_OPERATION",
                        "query_string": db_constants.ADD_DASHBOARD_USER_DATA.format(table_name="dashboard_user_role"),
                        "query_parameter": (username, "default")
                    }

                    DatabaseQuery.execute_query(json_obj=db_payload)

                    db_payload = {
                        "query_type": "INSERT_OPERATION",
                        "query_string": db_constants.ADD_CUSTOMER_USER_DATA.format(table_name="customer_user_role"),
                        "query_parameter": (username, "Starter")
                    }

                    DatabaseQuery.execute_query(json_obj=db_payload)

                    flash("You are successfully register......Enjoy with that product...")
                    # msg = Message('Successfully Register',
                    #     sender='harshitgadhiya8980@gmail.com',
                    #     recipients=[email]
                    # )
                    #
                    # msg.body = f'Hello {username}!\nYou have successfully register.'
                    # mail.send(msg)
                    return redirect(url_for('home', _external=True, _scheme=secure_type))
            else:
                flash("Password doesn't match!!")
                return redirect(url_for('register', _external=True, _scheme=secure_type))
        else:
            return render_template("register.html")

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('register', _external=True, _scheme=secure_type))

# That function should be login into that product
@app.route("/login", methods=["GET","POST"])
def login():
    """
    That route can use login user
    """

    try:
        if request.method=="POST":
            username = request.form["username"]
            pwd = request.form["pwd"]

            db_payload = {
                "query_type": "SELECT_OPERATION",
                "query_string": db_constants.GET_DATA.format(table_name="register_user")
            }

            all_response = DatabaseQuery.execute_query(json_obj=db_payload)

            all_username = [[data[5], data[6]] for data in all_response]
            if [username,pwd] in all_username:
                session["username"] = username

                get_prod_permission_name()
                get_dash_permission_name()
                flash("Successfully Login")
                return redirect(url_for('home', _external=True, _scheme=secure_type))
            else:
                flash("Your credentials doesn't match! Please enter correct Username and password...")
                return redirect(url_for('login', _external=True, _scheme=secure_type))
        else:
            return render_template("login.html")

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('login', _external=True, _scheme=secure_type))



# That is route for sending forget mail for user
@app.route("/forget_password", methods=["GET","POST"])
def forget_password():
    """
    That function was sending forget mail while user can forget password
    """

    try:
        if request.method=="POST":
            main=main
        else:
            return render_template("forgot-password.html")

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('forget_password', _external=True, _scheme=secure_type))





if __name__ == "__main__":
    # db.create_all()
    app.run(
        host=yaml_data['app']['host'],
        port=yaml_data['app']['port'],
        debug=yaml_data['app']['debug'])

