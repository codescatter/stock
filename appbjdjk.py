### import required libraries
from project_engine.operation_logic.fetched_data import ScrapData
from project_engine.operation_logic.link_extractor import crawl
# from project_engine.operation_logic.machine_learning_process import Build_ML_Model

import re
from datetime import datetime
import random
from pathlib import Path

from flask import (Response, flash, redirect, render_template, request,
                   send_from_directory, session, url_for)
from flask_mail import Mail, Message
import os
from project_engine import app, yaml_data, mail
from project_engine.operation_logic.general_function import finding_email, add_admin_data, get_prod_permission_name, get_dash_permission_name
from project_engine.db_connector.db_queries import DatabaseQuery
from project_engine.project_constants import db_constants
from project_engine.project_constants.constants import secure_type, pred_count, cleanned_file_name, ml_model_filename, confusion_matrix_filename, classification_df_filename

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


# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/", methods=["GET","POST"])
def home():
    """
    That route can show landing page while user can login
    """

    session["host"] = yaml_data["app"]["host"]
    session["port"] = yaml_data["app"]["port"]
    return render_template("home.html")


# That is route for sending forget mail for user
@app.route("/sending_forget_mail", methods=["GET","POST"])
def sending_forget_mail():
    """
    That function was sending forget mail while user can forget password
    """

    try:
        if request.method=="POST":
            username = request.form["username"]
            email = request.form["email"]

            db_payload = {
                "query_type": "SELECT_OPERATION",
                "query_string": db_constants.GET_DATA.format(table_name="register_user")
            }

            all_response = DatabaseQuery.execute_query(json_obj=db_payload)

            if all_response:
                all_username = [data[5] for data in all_response]
                if username in all_username:
                    session["email"] = email
                    msg = Message('Forget_Password',
                                  sender='hgadhiya8980@gmail.com',
                                  recipients=[email]
                                  )
                    msg.body = 'Hello user\nChange Password\nclick that link https://{0}:{1}/forget_password'.format(session["host"], session["port"])
                    mail.send(msg)
                    return redirect(url_for('sending_forget_mail', _external=True, _scheme=secure_type))
                else:
                    flash("That {0} is not availble First you can register!!".format(username))
                    return redirect(url_for('sending_forget_mail', _external=True, _scheme=secure_type))
        else:
            return render_template("sending_forget_mail.html")

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('sending_forget_mail', _external=True, _scheme=secure_type))

# That is route for show all pricing plan
@app.route("/pricing", methods=["GET","POST"])
def pricing():
    """
        That route can show all product plans....
    """
    return render_template("pricing.html")

# That is route for update pricing plan data
@app.route("/product_form", methods=["GET","POST"])
def product_form():
    """
    That function can add data for product plan subscripation and send a mail admin
    """

    try:
        if request.method=="POST":
            email = request.form["email"]
            phone = request.form["phone"]
            product_selection = request.form["product_selection"]
            username = session.get("username", [])

            if username:
                db_payload = {
                    "query_type": "SELECT_OPERATION",
                    "query_string": db_constants.GET_DATA.format(table_name="register_user")
                }

                all_response = DatabaseQuery.execute_query(json_obj=db_payload)

                all_username = [data[5] for data in all_response]
                if username in all_username:
                    created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")
                    db_payload = {
                        "query_type": "INSERT_OPERATION",
                        "query_string": db_constants.ADD_PRODUCT_PLAN_DATA.format(nlp_database_name="dev_db_main",
                                                                              table_name="product_user_plan"),
                        "query_parameter": (username, email, phone, product_selection, created_on, updated_on)
                    }

                    DatabaseQuery.execute_query(json_obj=db_payload)

            else:
                flash("Username is not availble! Please try out after login...")
                return redirect(url_for('product_form', _external=True, _scheme=secure_type))
        else:
            return render_template("product_form.html")

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('product_form', _external=True, _scheme=secure_type))

# That is route for otp sending mail for user
@app.route("/otp_sending", methods=["GET","POST"])
def otp_sending():
    """
    That funcation was sending a otp for user
    """

    try:
        otp = random.randint(100000, 999999)
        session["otp"] = otp
        msg = Message("OTP Received",
                      sender='hgadhiya8980@gmail.com',
                      recipients=[session.get("email", "")])
        msg.body = 'Hello {0}\nYour OTP is {1}\nThis OTP is valid only 10 miniuts....'.format(session["username"], otp)
        mail.send(msg)
        return redirect(url_for('forget_password', _external=True, _scheme=secure_type))

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('forget_password', _external=True, _scheme=secure_type))


# That is route for otp verification and sending new_password created link
@app.route("/forget_password", methods=["GET","POST"])
def forget_password():
    """
    That funcation can use otp_verification and new_password set link generate
    """

    try:
        if request.method=="POST":
            get_otp = request.form["otp"]

            send_otp = session.get("otp", "")
            if get_otp == send_otp:
                return redirect(url_for('change_password', _external=True, _scheme=secure_type))
            else:
                flash("OTP is wrong. Please enter correct otp")
                return redirect(url_for('forget_password', _external=True, _scheme=secure_type))
        else:
            return render_template("forget_password.html")

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('forget_password', _external=True, _scheme=secure_type))


# That is route for new_password generation
@app.route("/change_password", methods=["GET","POST"])
def change_password():
    """
    That function was create a new password and update that data
    """
    try:
        if request.method=="POST":
            new_pwd = request.form["new_pwd"]
            re_new_pwd = request.form["re_new_pwd"]
            username = session.get("username","")

            db_payload = {
                "query_type": "SELECT_OPERATION",
                "query_string": db_constants.GET_DATA.format(table_name="register_user")
            }

            all_response = DatabaseQuery.execute_query(json_obj=db_payload)

            user_data = [data for data in all_response if username == data[5]]
            if new_pwd == re_new_pwd:
                user_data[6] = new_pwd

                # update data on 'response_*' table
                db_payload = {
                    "query_type": "UPDATE_OPERATION",
                    "query_string": db_constants.UPDATE_USER_PASSWORD.format(database_name="register_user"),
                    "query_parameter": [new_pwd, username]
                }

                DatabaseQuery.execute_query(json_obj=db_payload)

                return redirect(url_for('login', _external=True, _scheme=secure_type))
            else:
                flash("Password doesn't match!!")
                return redirect(url_for('change_password', _external=True, _scheme=secure_type))
        else:
            return render_template("new_password.html")

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('change_password', _external=True, _scheme=secure_type))


# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/email_scrapper", methods=["GET","POST"])
def email_scrapper():
    """
    That route can show landing page while user can login
    """
    return render_template("email_scrapper.html")

# That is logout route and clear the current session
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    That funcation was logout session and clear user session
    """

    try:
        # clear the session when user logout
        session.clear()
        return render_template("login.html")

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('login', _external=True, _scheme=secure_type))


# That route should be show scrapped email data into perticular page.
# @app.route("/ml_tools", methods=["GET","POST"])
# def ml_tools():
#     try:
#         if request.method=="POST":
#             file = request.files["csv_file"]
#             filename = file.filename
#             print("@@ Input posted = ", filename)
#
#             output_dir = Path(r'/project_engine/data/')
#             if not output_dir.exists():
#                 output_dir.mkdir()
#
#             file_path = os.path.join("/project_engine/data/", filename)
#             file.save(file_path)
#             session["file_path"] = file_path
#
#             all_columns = Build_ML_Model().method_pred(file_path)
#             return render_template("ml_selection_form.html", all_columns=all_columns)
#         else:
#             return render_template("ml_form.html")
#
#     except Exception as e:
#         flash("Sorry for that issue....Please try again!")
#         return redirect(url_for('ml_tools', _external=True, _scheme=secure_type))

# @app.route("/download_report", methods=['POST', 'GET'])
# def download_report():
#     try:
#         csv_file_path = session.get("cleanned_data_path", "")
#         if csv_file_path:
#             file_name = csv_file_path.split("/")[-1]
#             index = csv_file_path.index(file_name)
#             file_path =
#
#         # getting the required details from session
#         smart_bot_key = session.get('key', "")
#         smart_bot_name = session.get('smart_bot_name', "")
#
#         # getting all info about client
#         db_payload = {
#             "query_type": "SELECT_OPERATION",
#             "query_string": db_constants.GET_SPECIFIC_SMART_BOT_DETAILS.format(df_agent_id=smart_bot_key,
#                                                                                main_database_name=main_database_name)
#         }
#
#         response = DatabaseQuery.execute_query(json_obj=db_payload)
#         response = response if len(response) == 0 else response[0]
#
#         if len(response) != 0:
#             specific_version = json.loads(response[6]).get('specific_version')
#
#             if specific_version == 'False':
#                 model_version = '2'
#             else:
#                 model_version = json.loads(response[6]).get("model_version")
#
#             # getting the model path
#             db_payload = {
#                 "query_type": "SELECT_OPERATION",
#                 "query_string": db_constants.GET_MODAL_PATH.format(smart_bot_key=smart_bot_key)
#             }
#
#             model_path = DatabaseQuery.execute_query(json_obj=db_payload)[0][4]
#
#             file_path = model_path + "/" + smart_bot_name + "/" + model_version + "/"
#
#             # file name for false prediction report generation
#             file_name = "false_prediction_" + model_version
#
#             data = pandas.read_csv(r'{}{}'.format(file_path,file_name), sep =',')
#             data.to_csv(f"{file_path}{file_name}.csv")
#
#             new_file_name = f"{file_name}.csv"
#             try:
#                 return send_from_directory(directory=file_path, filename=new_file_name)
#             except Exception as e:
#                 logger.log_exception(msg=str(e), exc_info=True)
#                 flash("File Not Found", category='error')
#                 df_id = session.get('key')
#                 cache_dict = app_cache.get(key=yaml_data['cache_key'])
#                 if cache_dict is not None:
#                     client_name = 'nlp_' + cache_dict[df_id]['dialogflow_details']['smart_bot_key']
#                 else:
#                     client_name = 'nlp_' + model_train_info.query.filter(
#                         model_train_info.df_agent_id == df_id).first().smart_bot_key
#
#                 return redirect(url_for('main', client=client_name, _external=True, _scheme=secure_type))
#
#         else:
#             df_id = session.get('key')
#             cache_dict = app_cache.get(key=yaml_data['cache_key'])
#             if cache_dict is not None:
#                 client_name = 'nlp_' + cache_dict[df_id]['dialogflow_details']['smart_bot_key']
#             else:
#                 client_name = 'nlp_' + model_train_info.query.filter(
#                     model_train_info.df_agent_id == df_id).first().smart_bot_key
#
#             flash("Record Download Successfully")
#             return redirect(url_for('main', client=client_name, _external=True, _scheme=secure_type))
#
#     except Exception as e:
#         flash("Sorry for that issue....Please try again!")
#         return redirect(url_for('login', _external=True, _scheme=secure_type))


# That route should be show scrapped email data into perticular page.
# @app.route("/ml_model", methods=["GET","POST"])
# def ml_model():
#     try:
#         if request.method == "POST":
#             column_name = request.form["column_name"]
#             dc_method = request.form["dc_method"]
#             ohe_method = request.form["ohe_method"]
#             fs_method = request.form["fs_method"]
#             ml_model_selection = request.form["ml_model_selection"]
#             file_path = session.get('column_name', '')
#
#             if file_path:
#                 Build_ML_Model().create_ml_model(file_path, column_name, dc_method, ohe_method, ml_model_selection, fs_method)
#
#     except Exception as e:
#         flash("Sorry for that issue....Please try again!")
#         return redirect(url_for('ml_tools', _external=True, _scheme=secure_type))

# That is route for sending forget mail for user
@app.route("/khatabook", methods=["GET","POST"])
def khatabook():
    try:
        if request.method=="POST":
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            buy_selection = request.form["buy_selection"]
            pay_method = request.form["pay_method"]
            amount = request.form["amount"]
            reason = request.form["reason"]
            date = request.form["date"]
            username = session.get("username", "")

            db_payload = {
                "query_type": "SELECT_OPERATION",
                "query_string": db_constants.GET_DATA.format(table_name="register_user")
            }

            all_response = DatabaseQuery.execute_query(json_obj=db_payload)

            if all_response:
                all_username = [data[5] for data in all_response]
                if username in all_username:

                    db_payload = {
                        "query_type": "INSERT_OPERATION",
                        "query_string": db_constants.ADD_KHATABOOK_DATA.format(table_name="khatabook_data"),
                        "query_parameter": (username, first_name, last_name, buy_selection, pay_method, amount, reason, date)
                    }

                    DatabaseQuery.execute_query(json_obj=db_payload)
                else:
                    flash("This user is not availble! Please first login....")
                    return redirect(url_for('khatabook', _external=True, _scheme=secure_type))

    except Exception as e:
        flash("Sorry for that issue....Please try again!")

    finally:
        db_payload = {
            "query_type": "SELECT_OPERATION",
            "query_string": db_constants.GET_KHATABOOK_DATA.format(table_name="khatabook_data", username=session.get("username", ""))
        }

        all_response = DatabaseQuery.execute_query(json_obj=db_payload)

        credit_value = 0
        debit_value = 0
        calu_credit_data = [own_res[6] for own_res in all_response if own_res[4]=="Credited"]
        calu_debit_data = [own_res[6] for own_res in all_response if own_res[4]=="Debited"]

        for deb in calu_debit_data:
            debit_value+=int(deb)

        for cre in calu_credit_data:
            credit_value+=int(cre)

        return render_template("khatabook.html", all_response=all_response, debit_value=debit_value, credit_value=credit_value, count=len(all_response), flag=True)


# That route should be show scrapped email data into perticular page.
@app.route("/scrape_gmail", methods=["GET","POST"])
def scrape_gmail():
    """
    That funcation can show all scraped data
    """

    try:
        if request.method == "POST":
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            given_url = request.form["given_url"]

            spliting = given_url.split("https://")
            temp = spliting[-1].split("/")
            given_url = "https://" + temp[0] + "/"

            db_payload = {
                "query_type": "SELECT_OPERATION",
                "query_string": db_constants.GET_DATA.format(table_name="email_extracter")
            }

            all_response = DatabaseQuery.execute_query(json_obj=db_payload)
            all_data = [[data[1],data[2],data[3]] for data in all_response]
            if [first_name, last_name, given_url] in all_data:
                all_email = [data[4] for data in all_response if given_url == data[3]]
                return render_template("email_scrapper.html", all_email=all_email, count=len(all_email), flag=True)
            else:
                obj = ScrapData(given_url)
                all_data = obj.get_all_data()
                raw_data = all_data['data']['raw_data']
                all_email, all_zipcode, all_phone, all_date = finding_email(raw_data)

                all_email, all_zipcode, all_phone, all_date = set(all_email), set(all_zipcode), set(all_phone), set(all_date)
                created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

                db_payload = {
                    "query_type": "INSERT_OPERATION",
                    "query_string": db_constants.ADD_EMAIL_DATA.format(nlp_database_name="dev_db_main",
                                                                   table_name="email_extracter"),
                    "query_parameter": (first_name, last_name, given_url, all_email, created_on, updated_on)
                }

                DatabaseQuery.execute_query(json_obj=db_payload)

                flash("Your Process Can Be Completed")
                return render_template("email_scrapper.html", all_email=all_email, count=len(all_email), flag=True)

        else:
            return render_template("email_scrapper.html", count=0, flag=False)

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('scrape_gmail', _external=True, _scheme=secure_type))

# That route should be show scrapped email data into perticular page.
@app.route("/tip_tap", methods=["GET","POST"])
def tip_tap():
    try:
        table_name = "tips_tap"

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")

    finally:
        db_payload = {
            "query_type": "SELECT_OPERATION",
            "query_string": db_constants.GET_DATA.format(table_name="tips_tap")
        }

        all_response = DatabaseQuery.execute_query(json_obj=db_payload)
        all_response = all_response[::-1]
        return render_template("tip_tap.html", all_response=all_response)


# That route should be show scrapped email data into perticular page.
@app.route("/scrape_phone", methods=["GET","POST"])
def scrape_phone():
    """
    That funcation can show all scraped data
    """

    try:
        if request.method == "POST":
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            given_url = request.form["given_url"]

            spliting = given_url.split("https://")
            temp = spliting[-1].split("/")
            given_url = "https://" + temp[0]

            db_payload = {
                "query_type": "SELECT_OPERATION",
                "query_string": db_constants.GET_DATA.format(table_name="phone_extracter")
            }

            all_response = DatabaseQuery.execute_query(json_obj=db_payload)
            all_data = [[data[1],data[2],data[3]] for data in all_response]
            if [first_name, last_name, given_url] in all_data:
                all_phone = [data[4] for data in all_response if given_url == data[3]]
                return render_template("phone_scrapper.html", all_phone=all_phone, count=len(all_phone), flag=True)
            else:
                obj = ScrapData(given_url)
                all_data = obj.get_all_data()
                raw_data = all_data['data']['raw_data']
                all_email, all_zipcode, all_phone, all_date = finding_email(raw_data)

                all_email, all_zipcode, all_phone, all_date = set(all_email), set(all_zipcode), set(all_phone), set(all_date)
                created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

                db_payload = {
                    "query_type": "INSERT_OPERATION",
                    "query_string": db_constants.ADD_EMAIL_DATA.format(nlp_database_name="dev_db_main",
                                                                   table_name="phone_extracter"),
                    "query_parameter": (first_name, last_name, given_url, all_email, created_on, updated_on)
                }

                DatabaseQuery.execute_query(json_obj=db_payload)

                flash("Your Process Can Be Completed")
                return render_template("phone_scrapper.html", all_phone=all_phone, count=len(all_phone), flag=True)

        else:
            return render_template("email_scrapper.html", count=0, flag=False)

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('scrape_gmail', _external=True, _scheme=secure_type))










# Admin Panel Section

# That function should be login into that product
@app.route("/admin_login", methods=["GET","POST"])
def admin_login():
    """
    That route can use login user
    """

    try:
        if request.method=="POST":
            username = request.form["username"]
            pwd = request.form["pwd"]

            db_payload = {
                "query_type": "SELECT_OPERATION",
                "query_string": db_constants.GET_DATA.format(table_name="admin_user")
            }

            all_response = DatabaseQuery.execute_query(json_obj=db_payload)

            all_username = [[data[1], data[2]] for data in all_response]
            if [username,pwd] in all_username:
                session["admin_username"] = username
                flash("Successfully Login")
                return redirect(url_for('admin_home', _external=True, _scheme=secure_type))
            else:
                flash("Your credentials doesn't match! Please enter correct Username and password...")
                return redirect(url_for('admin_login', _external=True, _scheme=secure_type))
        else:
            return render_template("admin_login.html")

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('admin_login', _external=True, _scheme=secure_type))

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/admin_home", methods=["GET","POST"])
def admin_home():
    """
    That route can show landing page while user can login
    """

    return render_template("admin_home.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/customer_user_role", methods=["GET","POST"])
def customer_user_role():
    """
    That route can show landing page while user can login
    """
    try:
        table_name = "customer_user_role"
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("customer_user_role.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("customer_user_role.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/admin_user", methods=["GET","POST"])
def admin_user():
    """
    That route can show landing page while user can login
    """
    try:
        table_name = 'admin_user'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("admin_user.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin_user.html")


# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/content_extracter", methods=["GET","POST"])
def content_extracter():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'content_extracter'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("content_extracter.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("content_extracter.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/dashboard_permission", methods=["GET","POST"])
def dashboard_permission():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'dashboard_permission'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("dashboard_permission.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("dashboard_permission.html")


# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/dashboard_user_role", methods=["GET","POST"])
def dashboard_user_role():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'dashboard_user_role'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("dashboard_user_role.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("dashboard_user_role.html")


# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/dev_link_extract", methods=["GET","POST"])
def dev_link_extract():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'dev_link_extract'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("dev_link_extract.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("dev_link_extract.html")


# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/dev_seo_link_extract", methods=["GET","POST"])
def dev_seo_link_extract():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'dev_seo_link_extract'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("dev_seo_link_extract.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("dev_seo_link_extract.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/tips_tap", methods=["GET","POST"])
def tips_tap():
    """
    That route can show landing page while user can login
    """
    try:
        if request.method=="POST":
            username = request.form["username"]
            tip = request.form["tip"]
            short_des = request.form["short_des"]
            descripation = request.form["descripation"]
            file = request.files["file"]
            filename = file.filename

            file_path = os.path.join("C:/Users/admin/PycharmProjects/pythonProject/project_engine/static/uploaded_data/images", filename)
            file.save(file_path)


            db_payload = {
                "query_type": "INSERT_OPERATION",
                "query_string": db_constants.ADD_TIPS_DATA.format(table_name="tips_tap"),
                "query_parameter": (username, tip, short_des, descripation, file_path)
            }

            DatabaseQuery.execute_query(json_obj=db_payload)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")

    finally:
        db_payload = {
            "query_type": "SELECT_OPERATION",
            "query_string": db_constants.GET_DATA.format(table_name="tips_tap")
        }

        all_response = DatabaseQuery.execute_query(json_obj=db_payload)



        return render_template("tips_tap.html", all_response=all_response, count=len(all_response), flag=True)

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/email_extracter", methods=["GET","POST"])
def email_extracter():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'email_extracter'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("email_extracter.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("email_extracter.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/khatabook_data", methods=["GET","POST"])
def khatabook_data():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'khatabook_data'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("khatabook_data.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("khatabook_data.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/model_train_info", methods=["GET","POST"])
def model_train_info():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'model_train_info'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("model_train_info.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("model_train_info.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/phone_extracter", methods=["GET","POST"])
def phone_extracter():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'phone_extracter'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("phone_extracter.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("phone_extracter.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/product_permission", methods=["GET","POST"])
def product_permission():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'product_permission'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("product_permission.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("product_permission.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/register_user", methods=["GET","POST"])
def register_user():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'register_user'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("register_user.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("register_user.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/seolink_extracter", methods=["GET","POST"])
def seolink_extracter():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'seolink_extracter'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("seolink_extracter.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("seolink_extracter.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/stock_market_tips", methods=["GET","POST"])
def stock_market_tips():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'stock_market_tips'
        all_response, new_col_list = add_admin_data(table_name)

        db_payload1 = {
            "query_type": "SELECT_OPERATION",
            "query_string": db_constants.GET_DATA.format(table_name="register_user")
        }

        all_user_data = DatabaseQuery.execute_query(json_obj=db_payload1)

        all_email_data = [em[2] for em in all_user_data]




        return render_template("stock_market_tips_manage.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("stock_market_tips_manage.html")




if __name__ == "__main__":
    # db.create_all()
    app.run(
        host=yaml_data['app']['host'],
        port=yaml_data['app']['port'],
        debug=yaml_data['app']['debug'])



