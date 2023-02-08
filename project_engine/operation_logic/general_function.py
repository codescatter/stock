### import required libraries
from project_engine.operation_logic.fetched_data import ScrapData
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
from project_engine.db_connector.db_queries import DatabaseQuery
from project_engine.project_constants import db_constants
from project_engine.project_constants.constants import secure_type, pred_count, cleanned_file_name, ml_model_filename, confusion_matrix_filename, classification_df_filename


# That function should be find email using regex pattern while website content
def finding_email(raw_data):
    """
        That function was finding data from given website link
    """

    try:
        all_keys_raw = list(raw_data.keys())
        phrases = raw_data[all_keys_raw[0]]
        for num, key in enumerate(raw_data.keys()):
            if num > 0:
                phrases = phrases + " " + raw_data[key]

        all_email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', phrases)

        # That function should be find zipcode entity
        all_zipcode = re.findall(r"[0-9]{6}(?:-[0-9]{4})?|[0-9]{5}(?:-[0-9]{4})?|[0-9]{5}-[0-9]{4}(?:-[0-9]{4})?", phrases)

        # That function should be find phone-number entity
        all_phone = re.findall("\+?[1-9]{0,2}[-\.\s]?[0-9]{3}[-\.\s]?[0-9]{3}[-\.\s]?[0-9]{4}", phrases)

        # That function should be find date entity
        all_date = re.findall("\d{1,2}\W\d{1,2}\W\d{2,4}", phrases)

        return all_email, all_zipcode, all_phone, all_date

    except Exception as e:
        print(e)


def add_admin_data(table_name):
    try:
        db_payload = {
            "query_type": "SELECT_OPERATION",
            "query_string": db_constants.GET_ALL_COLUMNS_NAME.format(table_name=table_name)
        }

        all_columns_name = DatabaseQuery.execute_query(json_obj=db_payload)

        new_col_list = []
        all_col_name = [var[0] for var in all_columns_name]
        if "id" == all_col_name[0]:
            count = 2
            while len(new_col_list) != len(all_columns_name) - 1:
                for add_res in all_columns_name:
                    if add_res[1] == count and add_res[0] not in ["id"]:
                        new_col_list.append(add_res[0])
                        count += 1
        else:
            count = 1
            while len(new_col_list) != len(all_columns_name):
                for add_res in all_columns_name:
                    if add_res[1] == count and add_res[0] not in ["id"]:
                        new_col_list.append(add_res[0])
                        count += 1


        if request.method == "POST":
            new_data_list = []
            for own_col in new_col_list:
                own_col_value = request.form[own_col]
                new_data_list.append(own_col_value)

            new_col_list1 = tuple(new_col_list)
            cre_format = str(new_col_list1)
            cre_format = cre_format.replace("'", "")

            db_payload = {
                "query_type": "INSERT_OPERATION",
                "query_string": db_constants.ADD_ALL_ADMIN_DATA.format(nlp_database_name="dev_db_main",
                                                                       table_name=table_name,
                                                                       all_columns_name=cre_format,
                                                                       all_columns_value=tuple(new_data_list)),
            }


            DatabaseQuery.execute_query(json_obj=db_payload)
            flash("Data added successfully!!!")

            db_payload = {
                "query_type": "SELECT_OPERATION",
                "query_string": db_constants.GET_DATA.format(table_name=table_name)
            }


            all_response = DatabaseQuery.execute_query(json_obj=db_payload)
            return all_response, new_col_list
        else:
            db_payload = {
                "query_type": "SELECT_OPERATION",
                "query_string": db_constants.GET_DATA.format(table_name=table_name)
            }

            all_response = DatabaseQuery.execute_query(json_obj=db_payload)
            return all_response, new_col_list

    except Exception as e:
        print(e)


def get_dash_permission_name():
    try:
        db_payload = {
            "query_type": "SELECT_OPERATION",
            "query_string": db_constants.GET_DASH_USER_DATA.format(table_name="dashboard_user_Role", username=session.get("username", ""))
        }

        all_response = DatabaseQuery.execute_query(json_obj=db_payload)

        session["dash_permission"] = all_response

    except Exception as e:
        print(e)


def get_prod_permission_name():
    try:
        db_payload = {
            "query_type": "SELECT_OPERATION",
            "query_string": db_constants.GET_PROD_USER_DATA.format(table_name="customer_user_role",
                                                                   username=session.get("username", ""))
        }

        all_response = DatabaseQuery.execute_query(json_obj=db_payload)

        session["prod_permission"] = all_response

    except Exception as e:
        print(e)


