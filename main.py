### import required libraries
# from project_engine.operation_logic.machine_learning_process import Build_ML_Model

import re
from datetime import datetime
import random
import pandas as pd
from pathlib import Path

from flask import (Response, flash, redirect, render_template, request,
                   send_from_directory, session, url_for)
from flask_mail import Mail, Message
import os
from project_engine import app, yaml_data, mail
from project_engine.operation_logic.general_function import finding_email, add_admin_data, get_prod_permission_name, get_dash_permission_name
from project_engine.db_connector.db_queries import DatabaseQuery
from project_engine.project_constants import db_constants
from project_engine.project_constants.constants import secure_type, pred_count, cleanned_file_name, ml_model_filename, confusion_matrix_filename, classification_df_filename, file_path


# # That is home page like scrapping tool and scrape the data into given website urls
# @app.route("/", methods=["GET","POST"])
# def home():
#     """
#     That route can show landing page while user can login
#     """
#
#     session["host"] = yaml_data["app"]["host"]
#     session["port"] = yaml_data["app"]["port"]
#     return render_template("home.html")

#
# @app.route("/home", methods=["GET","POST"])
# def home():
#     """
#     That function can show all scraped data
#     """
#
#     try:
#         if request.method == "POST":
#             main_item = request.form["main_item"]
#             main_item_wei = request.form["main_item_wei"]
#             sub_item = request.form["sub_item"]
#             sub_item_wei = request.form["sub_item_wei"]
#             sub_item_pri_kg = request.form["sub_item_pri_kg"]
#             sub_item_pri_total = request.form["sub_item_pri_total"]
#
#             created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")
#
#             db_payload = {
#                     "query_type": "INSERT_OPERATION",
#                     "query_string": db_constants.ADD_CONTENT_DATA.format(nlp_database_name="dev_db_main",
#                                                                    table_name="content_extracter"),
#                     "query_parameter": (username, first_name, last_name, given_url, content, created_on, updated_on)
#                 }
#
#                 DatabaseQuery.execute_query(json_obj=db_payload)
#
#                 db_payload = {
#                     "query_type": "SELECT_OPERATION",
#                     "query_string": db_constants.GET_CONTENT_SCRAPPER_DATA.format(table_name="content_extracter",
#                                                                                   username=username)
#                 }
#
#                 all_response = DatabaseQuery.execute_query(json_obj=db_payload)
#
#                 flash("Your Process Can Be Completed")
#                 return render_template("content_scrapper.html", all_response=set(all_response), count=len(set(all_response)), flag=True)
#             else:
#                 return render_template("content_scrapper.html", all_response=set(all_response), count=len(set(all_response)), flag=True)
#         else:
#             flash("username is not register! please first login....")
#             return render_template("content_scrapper.html", count=0, flag=False)
#
#     except Exception as e:
#         print(e)
#         flash("Sorry for that issue....Please try again!")
#         return redirect(url_for('scrape_content', _external=True, _scheme=secure_type))

# That route should be show scrapped email data into perticular page.
@app.route("/scrape_email", methods=["GET","POST"])
def scrape_email():
    """
    That funcation can show all scraped data
    """

    try:

        username = session.get("username", "")
        if username:
            db_payload = {
                "query_type": "SELECT_OPERATION",
                "query_string": db_constants.GET_EMAIL_SCRAPPER_DATA.format(table_name="email_extracter",
                                                                       username=username)
            }

            all_response = DatabaseQuery.execute_query(json_obj=db_payload)

            if request.method == "POST":
                first_name = request.form["first_name"]
                last_name = request.form["last_name"]
                given_url = request.form["given_url"]

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
                    "query_parameter": (username, first_name, last_name, given_url, all_email, created_on, updated_on)
                }

                DatabaseQuery.execute_query(json_obj=db_payload)

                db_payload = {
                    "query_type": "SELECT_OPERATION",
                    "query_string": db_constants.GET_EMAIL_SCRAPPER_DATA.format(table_name="email_extracter",
                                                                                  username=username)
                }

                all_response = DatabaseQuery.execute_query(json_obj=db_payload)

                flash("Your Process Can Be Completed")
                return render_template("email_scrapper.html", all_response=set(all_response), count=len(set(all_response)), flag=True)
            else:
                return render_template("email_scrapper.html", all_response=set(all_response), count=len(set(all_response)), flag=True)
        else:
            flash("username is not register! please first login....")
            return render_template("email_scrapper.html", count=0, flag=False)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('scrape_email', _external=True, _scheme=secure_type))

# That route should be show scrapped email data into perticular page.
@app.route("/scrape_zipcode", methods=["GET","POST"])
def scrape_zipcode():
    """
    That funcation can show all scraped data
    """
    try:

        username = session.get("username", "")
        if username:
            db_payload = {
                "query_type": "SELECT_OPERATION",
                "query_string": db_constants.GET_ZIPCODE_SCRAPPER_DATA.format(table_name="zipcode_extracter",
                                                                       username=username)
            }

            all_response = DatabaseQuery.execute_query(json_obj=db_payload)

            if request.method == "POST":
                first_name = request.form["first_name"]
                last_name = request.form["last_name"]
                given_url = request.form["given_url"]

                obj = ScrapData(given_url)
                all_data = obj.get_all_data()
                raw_data = all_data['data']['raw_data']
                all_email, all_zipcode, all_phone, all_date = finding_email(raw_data)

                all_email, all_zipcode, all_phone, all_date = set(all_email), set(all_zipcode), set(all_phone), set(all_date)
                created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

                db_payload = {
                    "query_type": "INSERT_OPERATION",
                    "query_string": db_constants.ADD_ZIPCODE_DATA.format(nlp_database_name="dev_db_main",
                                                                   table_name="zipcode_extracter"),
                    "query_parameter": (username, first_name, last_name, given_url, all_zipcode, created_on, updated_on)
                }

                DatabaseQuery.execute_query(json_obj=db_payload)

                db_payload = {
                    "query_type": "SELECT_OPERATION",
                    "query_string": db_constants.GET_ZIPCODE_SCRAPPER_DATA.format(table_name="zipcode_extracter",
                                                                                  username=username)
                }

                all_response = DatabaseQuery.execute_query(json_obj=db_payload)

                flash("Your Process Can Be Completed")
                return render_template("zipcode_scrapper.html", all_response=set(all_response), count=len(set(all_response)), flag=True)
            else:
                return render_template("zipcode_scrapper.html", all_response=set(all_response), count=len(set(all_response)), flag=True)
        else:
            flash("username is not register! please first login....")
            return render_template("zipcode_scrapper.html", count=0, flag=False)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('scrape_zipcode', _external=True, _scheme=secure_type))

# That route should be show scrapped email data into perticular page.
@app.route("/scrape_phone", methods=["GET","POST"])
def scrape_phone():
    """
    That funcation can show all scraped data
    """
    try:

        username = session.get("username", "")
        if username:
            db_payload = {
                "query_type": "SELECT_OPERATION",
                "query_string": db_constants.GET_PHONE_SCRAPPER_DATA.format(table_name="phone_extracter",
                                                                       username=username)
            }

            all_response = DatabaseQuery.execute_query(json_obj=db_payload)

            if request.method == "POST":
                first_name = request.form["first_name"]
                last_name = request.form["last_name"]
                given_url = request.form["given_url"]

                obj = ScrapData(given_url)
                all_data = obj.get_all_data()
                raw_data = all_data['data']['raw_data']
                all_email, all_zipcode, all_phone, all_date = finding_email(raw_data)

                all_email, all_zipcode, all_phone, all_date = set(all_email), set(all_zipcode), set(all_phone), set(all_date)
                created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

                db_payload = {
                    "query_type": "INSERT_OPERATION",
                    "query_string": db_constants.ADD_PHONE_DATA.format(nlp_database_name="dev_db_main",
                                                                   table_name="phone_extracter"),
                    "query_parameter": (username, first_name, last_name, given_url, all_phone, created_on, updated_on)
                }

                DatabaseQuery.execute_query(json_obj=db_payload)

                db_payload = {
                    "query_type": "SELECT_OPERATION",
                    "query_string": db_constants.GET_PHONE_SCRAPPER_DATA.format(table_name="phone_extracter",
                                                                                  username=username)
                }

                all_response = DatabaseQuery.execute_query(json_obj=db_payload)

                flash("Your Process Can Be Completed")
                return render_template("phone_scrapper.html", all_response=set(all_response), count=len(set(all_response)), flag=True)
            else:
                return render_template("phone_scrapper.html", all_response=set(all_response), count=len(set(all_response)), flag=True)
        else:
            flash("username is not register! please first login....")
            return render_template("phone_scrapper.html", count=0, flag=False)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('scrape_phone', _external=True, _scheme=secure_type))


# That route should be show scrapped email data into perticular page.
@app.route("/scrape_seolink", methods=["GET","POST"])
def scrape_seolink():
    """
    That funcation can show all scraped data
    """
    try:

        username = session.get("username", "")
        if username:
            db_payload = {
                "query_type": "SELECT_OPERATION",
                "query_string": db_constants.GET_SEO_LINK_SCRAPPER_DATA.format(table_name="seolink_extracter",
                                                                       username=username)
            }

            all_response = DatabaseQuery.execute_query(json_obj=db_payload)

            if request.method == "POST":
                first_name = request.form["first_name"]
                last_name = request.form["last_name"]
                given_url = request.form["given_url"]

                links, internal_urls, external_urls = crawl(given_url)
                created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

                db_payload = {
                    "query_type": "INSERT_OPERATION",
                    "query_string": db_constants.ADD_SEO_LINK_DATA.format(nlp_database_name="dev_db_main",
                                                                   table_name="seolink_extracter"),
                    "query_parameter": (username, first_name, last_name, given_url, external_urls, created_on, updated_on)
                }

                DatabaseQuery.execute_query(json_obj=db_payload)

                db_payload = {
                    "query_type": "SELECT_OPERATION",
                    "query_string": db_constants.GET_SEO_LINK_SCRAPPER_DATA.format(table_name="seolink_extracter",
                                                                                  username=username)
                }

                all_response = DatabaseQuery.execute_query(json_obj=db_payload)

                flash("Your Process Can Be Completed")
                return render_template("seolink_scrapper.html", all_response=set(all_response), count=len(set(all_response)), flag=True)
            else:
                return render_template("seolink_scrapper.html", all_response=set(all_response), count=len(set(all_response)), flag=True)
        else:
            flash("username is not register! please first login....")
            return render_template("seolink_scrapper.html", count=0, flag=False)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('scrape_seolink', _external=True, _scheme=secure_type))


# That route should be show scrapped email data into perticular page.
@app.route("/full_scrapping_tool_data", methods=["GET","POST"])
def full_scrapping_tool_data():
    """
    That funcation can show all scraped data
    """
    try:

        username = session.get("username", "")
        if username:
            db_payload = {
                "query_type": "SELECT_OPERATION",
                "query_string": db_constants.GET_SCRAPPER_DATA.format(table_name="full_scrapping_tool",
                                                                       username=username)
            }

            all_response = DatabaseQuery.execute_query(json_obj=db_payload)

            if request.method == "POST":
                first_name = request.form["first_name"]
                last_name = request.form["last_name"]
                given_url = request.form["given_url"]

                links, internal_urls, external_urls = crawl(given_url)

                obj = ScrapData(given_url)
                all_data = obj.get_all_data()
                raw_data = all_data['data']['raw_data']
                all_email, all_zipcode, all_phone, all_date = finding_email(raw_data)

                all_email, all_zipcode, all_phone, all_date = set(all_email), set(all_zipcode), set(all_phone), set(all_date)
                created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

                db_payload = {
                    "query_type": "INSERT_OPERATION",
                    "query_string": db_constants.ADD_SCRAPPER_DATA.format(nlp_database_name="dev_db_main",
                                                                   table_name="full_scrapping_tool"),
                    "query_parameter": (username, first_name, last_name, given_url, all_email, all_phone, all_zipcode, external_urls, created_on, updated_on)
                }

                DatabaseQuery.execute_query(json_obj=db_payload)

                db_payload = {
                    "query_type": "SELECT_OPERATION",
                    "query_string": db_constants.GET_SCRAPPER_DATA.format(table_name="full_scrapping_tool",
                                                                                  username=username)
                }

                all_response = DatabaseQuery.execute_query(json_obj=db_payload)

                flash("Your Process Can Be Completed")
                return render_template("full_scrapping_tool.html", all_response=set(all_response), count=len(set(all_response)), flag=True)
            else:
                return render_template("full_scrapping_tool.html", all_response=set(all_response), count=len(set(all_response)), flag=True)
        else:
            flash("username is not register! please first login....")
            return render_template("full_scrapping_tool.html", count=0, flag=False)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('full_scrapping_tool_data', _external=True, _scheme=secure_type))

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
                    flash("Data Added Successfully....")
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

        dup_all_response = [own_res[0:-2] for own_res in all_response]
        all_response = tuple(dup_all_response)

        credit_value = 0
        debit_value = 0
        calu_credit_data = [own_res[6] for own_res in all_response if own_res[4]=="Credited"]
        calu_debit_data = [own_res[6] for own_res in all_response if own_res[4]=="Debited"]

        for deb in calu_debit_data:
            debit_value+=int(deb)

        for cre in calu_credit_data:
            credit_value+=int(cre)

        total = credit_value-debit_value

        return render_template("khatabook.html", all_response=all_response, debit_value=debit_value, total=str(total), credit_value=credit_value, count=len(all_response), flag=True)

# That is route for sending forget mail for user
@app.route("/help", methods=["GET","POST"])
def help():
    try:
        if request.method=="POST":
            query = request.form["query"]
            username = session.get("username", "")

            db_payload = {
                "query_type": "SELECT_OPERATION",
                "query_string": db_constants.GET_DATA.format(table_name="register_user")
            }

            all_response = DatabaseQuery.execute_query(json_obj=db_payload)

            if all_response:
                all_username = [data[5] for data in all_response]
                created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")
                if username in all_username:

                    db_payload = {
                        "query_type": "INSERT_OPERATION",
                        "query_string": db_constants.ADD_HELP_DATA.format(table_name="help_form"),
                        "query_parameter": (username, query, created_on, updated_on)
                    }

                    DatabaseQuery.execute_query(json_obj=db_payload)
                    flash("Data Added Successfully....")
                    return render_template("help_form.html")
                else:
                    flash("This user is not availble! Please first login....")
                    return render_template("help_form.html")
        else:
            return render_template("help_form.html")

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return render_template("help_form.html")

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
                    flash("Data Added successfully!....")
                    return render_template("product_form.html")
            else:
                flash("Username is not availble! Please try out after login...")
                return render_template("product_form.html")
        else:
            return render_template("product_form.html")

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('product_form', _external=True, _scheme=secure_type))


# That route should be show scrapped email data into perticular page.
@app.route("/stock_market_tips", methods=["GET","POST"])
def stock_market_tips():
    try:
        table_name = "stock_market_tips"

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")

    finally:
        db_payload = {
            "query_type": "SELECT_OPERATION",
            "query_string": db_constants.GET_DATA.format(table_name="stock_market_tips")
        }

        all_response = DatabaseQuery.execute_query(json_obj=db_payload)
        all_response = all_response[::-1]

        getting_page = []
        for own_page in all_response:
            tip_name = own_page[2]
            descri = own_page[5]
            sen = tip_name + "---" + descri
            sen = sen.replace("/", "---")
            sen = sen.replace("\\\\", "---")
            getting_page.append(sen)

        all_response = [[own_res, num] for num, own_res in enumerate(all_response)]

        return render_template("stock_market_tips.html", all_response=all_response, getting_page=getting_page)


# That route should be show scrapped email data into perticular page.
@app.route("/stock_market_tips/<tip>", methods=["GET","POST"])
def own_tips(tip):
    try:
        spliting_word = tip.split("---")
        tip_name = spliting_word[0]
        all_word = spliting_word[1:]
        image_path = all_word[0]
        for own_word in all_word[1:]:
            image_path = image_path+"/"+own_word

        db_payload = {
            "query_type": "SELECT_OPERATION",
            "query_string": db_constants.GET_STOCK_MARKET_DATA.format(table_name="stock_market_tips", tip_name=tip_name,
                                                                      file_path=image_path)
        }

        all_response = DatabaseQuery.execute_query(json_obj=db_payload)
        all_response = list(all_response)
        image_url = list(all_response[0])
        index = image_url[5].index("/static/")
        image_url[5] = image_url[5][index:]
        all_response[0] = tuple(image_url)
        all_response = tuple(all_response)

        return render_template("own_tips.html", all_response=all_response)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("stock_market_tips.html")

# @app.route("/download_report/<response>", methods=['POST', 'GET'])
# def download_report(response):
#     try:
#         response = eval(response)
#
#         df = pd.DataFrame(response)
#         df.to_csv("download_report.csv")
#
#         file_path = r"C:/Users/admin/PycharmProjects/pythonProject/"
#
#         # file name for false prediction report generation
#         file_name = "download_report.csv"
#
#         try:
#             return send_from_directory(directory=file_path, filename=file_name)
#         except Exception as e:
#             print(e)
#             flash("File Not Found", category='error')
#
#             return redirect(url_for('home',  _external=True, _scheme=secure_type))
#
#     except Exception as e:
#         print(e)
#         flash("File Not Found", category='error')
#
#         return redirect(url_for('home', _external=True, _scheme=secure_type))














# all admin page



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
            return render_template("admin/admin_login.html")

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/admin_login.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/admin_home", methods=["GET","POST"])
def admin_home():
    """
    That route can show landing page while user can login
    """

    return render_template("admin/admin_home.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/delete_record/<id>", methods=["GET","POST"])
def delete_record(id):
    """
    That route can show landing page while user can login
    """
    spliting = id.split("+++")
    data_value = spliting[0]
    data_value1 = spliting[1]
    table_name = spliting[2]
    col_name = spliting[3]
    col_name1 = spliting[4]


    db_payload = {
        "query_type": "DELETE_OPERATION",
        "query_string": db_constants.DELETE_DATA.format(table_name=table_name, col_name=col_name, col_value=data_value, col_name1=col_name1, col_value1=data_value1)
    }

    DatabaseQuery.execute_query(json_obj=db_payload)

    if "stock_market_tips" in table_name:
        table_name = "stock_market_tips_data"

    return redirect(url_for(table_name, _external=True, _scheme=secure_type))

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/customer_user_role", methods=["GET","POST"])
def customer_user_role():
    """
    That route can show landing page while user can login
    """
    try:
        table_name = "customer_user_role"
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("admin/customer_user_role.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/customer_user_role.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/product_user_plan", methods=["GET","POST"])
def product_user_plan():
    """
    That route can show landing page while user can login
    """
    try:
        table_name = "product_user_plan"
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("admin/product_user_plan.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/product_user_plan.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/admin_user", methods=["GET","POST"])
def admin_user():
    """
    That route can show landing page while user can login
    """
    try:
        table_name = 'admin_user'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("admin/admin_user.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/admin_user.html")


# That is home page like scrapping tool and scrape the data into given website urls
# @app.route("/content_extracter", methods=["GET","POST"])
# def content_extracter():
#     """
#     That route can show landing page while user can login
#     """
#
#     try:
#         table_name = 'content_extracter'
#         all_response, new_col_list = add_admin_data(table_name)
#
#         return render_template("content_extracter.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)
#
#     except Exception as e:
#         print(e)
#         flash("Sorry for that issue....Please try again!")
#         return render_template("content_extracter.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/dashboard_permission", methods=["GET","POST"])
def dashboard_permission():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'dashboard_permission'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("admin/dashboard_permission.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/dashboard_permission.html")


# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/dashboard_user_role", methods=["GET","POST"])
def dashboard_user_role():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'dashboard_user_role'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("admin/dashboard_user_role.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/dashboard_user_role.html")


# That is home page like scrapping tool and scrape the data into given website urls
# @app.route("/dev_link_extract", methods=["GET","POST"])
# def dev_link_extract():
#     """
#     That route can show landing page while user can login
#     """
#
#     try:
#         table_name = 'dev_link_extract'
#         all_response, new_col_list = add_admin_data(table_name)
#
#         return render_template("dev_link_extract.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)
#
#     except Exception as e:
#         print(e)
#         flash("Sorry for that issue....Please try again!")
#         return render_template("dev_link_extract.html")


# That is home page like scrapping tool and scrape the data into given website urls

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/email_extracter", methods=["GET","POST"])
def email_extracter():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'email_extracter'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("admin/email_extracter.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/email_extracter.html")


@app.route("/full_scrapping_tool", methods=["GET","POST"])
def full_scrapping_tool():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'full_scrapping_tool'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("admin/full_scrapping_tool.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/full_scrapping_tool.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/help_form", methods=["GET","POST"])
def help_form():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'help_form'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("admin/help_form.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/help_form.html")


# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/stock_market_tips_data", methods=["GET","POST"])
def stock_market_tips_data():
    """
    That route can show landing page while user can login
    """
    try:
        supported_image_format = ["jpg", "png", "svg", "jpeg"]
        if request.method=="POST":
            username = request.form["username"]
            tip = request.form["tip"]
            short_des = request.form["short_des"]
            descripation = request.form["descripation"]
            file = request.files["file"]
            filename = file.filename

            spliting_main = filename.split(".")
            if spliting_main[-1] not in supported_image_format:
                flash("please enter valid image format")
                return render_template("admin/stock_market_tips_manage.html")

            filename = filename.replace("/", "")
            filename = filename.replace("(", "")
            filename = filename.replace(")", "")
            filename = filename.replace("-", "")
            filename = filename.replace("#", "")


            file_path = os.path.join("C:/Users/admin/PycharmProjects/pythonProject/project_engine/static/uploaded_data/images/", filename)
            file.save(file_path)

            file_path = file_path.replace(r"\\", "/")

            db_payload = {
                "query_type": "INSERT_OPERATION",
                "query_string": db_constants.ADD_TIPS_DATA.format(table_name="stock_market_tips"),
                "query_parameter": (username, tip, short_des, descripation, file_path)
            }

            DatabaseQuery.execute_query(json_obj=db_payload)

            db_payload = {
                "query_type": "SELECT_OPERATION",
                "query_string": db_constants.GET_DATA.format(table_name="register_user")
            }

            all_response = DatabaseQuery.execute_query(json_obj=db_payload)

            for own_res in all_response:
                mail.send_message("Stock Market Tips",
                                  sender="hgadhiya8980@gmail.com",
                                  recipients=[own_res[2]],
                                  body='New stock market tips availble into dashboard page.....')

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")

    finally:
        db_payload = {
            "query_type": "SELECT_OPERATION",
            "query_string": db_constants.GET_DATA.format(table_name="stock_market_tips")
        }

        all_response = DatabaseQuery.execute_query(json_obj=db_payload)

        return render_template("admin/stock_market_tips_manage.html", all_response=all_response, count=len(all_response), flag=True)


# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/khatabook_data", methods=["GET","POST"])
def khatabook_data():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'khatabook_data'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("admin/khatabook_data.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/khatabook_data.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/model_train_info", methods=["GET","POST"])
def model_train_info():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'model_train_info'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("admin/model_train_info.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/model_train_info.html")


# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/phone_extracter", methods=["GET","POST"])
def phone_extracter():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'phone_extracter'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("admin/phone_extracter.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/phone_extracter.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/zipcode_extracter", methods=["GET","POST"])
def zipcode_extracter():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'zipcode_extracter'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("admin/zipcode_extracter.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/zipcode_extracter.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/product_permission", methods=["GET","POST"])
def product_permission():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'product_permission'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("admin/product_permission.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/product_permission.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/register_user", methods=["GET","POST"])
def register_user():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'register_user'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("admin/register_user.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/register_user.html")

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/seolink_extracter", methods=["GET","POST"])
def seolink_extracter():
    """
    That route can show landing page while user can login
    """

    try:
        table_name = 'seolink_extracter'
        all_response, new_col_list = add_admin_data(table_name)

        return render_template("admin/seolink_extracter.html", all_response=all_response, table_name=table_name, new_col_list=new_col_list, count=len(all_response), flag=True)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/seolink_extracter.html")



if __name__ == "__main__":
    # db.create_all()
    app.run(
        host=yaml_data['app']['host'],
        port=yaml_data['app']['port'],
        debug=yaml_data['app']['debug'])