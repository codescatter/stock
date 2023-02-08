# select queries
GET_PERMISSION_NAMES = "SELECT permission_name FROM {table_name} WHERE id={permission_id}"
GET_DATA = "select * from {table_name}"
GET_KHATABOOK_DATA = "select * from {table_name} where username='{username}'"
GET_CONTENT_SCRAPPER_DATA = "select * from {table_name} where username='{username}'"
GET_EMAIL_SCRAPPER_DATA = "select * from {table_name} where username='{username}'"
GET_PHONE_SCRAPPER_DATA = "select * from {table_name} where username='{username}'"
GET_SEO_LINK_SCRAPPER_DATA = "select * from {table_name} where username='{username}'"
GET_ZIPCODE_SCRAPPER_DATA = "select * from {table_name} where username='{username}'"
GET_SCRAPPER_DATA = "select * from {table_name} where username='{username}'"
GET_STOCK_MARKET_DATA = "select * from {table_name} where tip='{tip_name}' and file_path='{file_path}'"


GET_DASH_USER_DATA = "select * from {table_name} where username='{username}'"
GET_PROD_USER_DATA = "select * from {table_name} where username='{username}'"
GET_ALL_COLUMNS_NAME = "SELECT COLUMN_NAME, ORDINAL_POSITION FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}' AND table_schema = 'dev_db_main'"

# update queries
UPDATE_USER_PASSWORD = "update {database_name} set pwd=%s where username=%s"
UPDATE_CUSTOMER_TABLE = "UPDATE {table_name} SET prod_permission=%s WHERE username=%s"
UPDATE_CLIENT_INFO = "UPDATE {database_name}.smart_bot_handler SET sb_specific_configuration=%s WHERE smart_bot_id=%s"

# insert queries for all scrapping tool
ADD_SCRAPPER_DATA = "insert into {nlp_database_name}.{table_name}(username, first_name, last_name, website, predicated_email,predicated_phone,predicated_zipcode,predicated_seolink, created_on, updated_on) values (%s, %s, %s, %s, %s, %s, %s %s, %s, %s)"
ADD_CONTENT_DATA = "insert into {nlp_database_name}.{table_name}(username, first_name, last_name, website, predicated_content, created_on, updated_on) values (%s, %s, %s, %s, %s, %s, %s)"
ADD_ZIPCODE_DATA = "insert into {nlp_database_name}.{table_name}(username, first_name, last_name, website, predicated_zipcode, created_on, updated_on) values (%s, %s, %s, %s, %s, %s, %s)"
ADD_PHONE_DATA = "insert into {nlp_database_name}.{table_name}(username, first_name, last_name, website, predicated_phone, created_on, updated_on) values (%s, %s, %s, %s, %s, %s, %s)"
ADD_SEO_LINK_DATA = "insert into {nlp_database_name}.{table_name}(username, first_name, last_name, website, predicated_seolink, created_on, updated_on) values (%s, %s, %s, %s, %s, %s, %s)"
ADD_EMAIL_DATA = "insert into {nlp_database_name}.{table_name}(username, first_name, last_name, website, predicated_email, created_on, updated_on) values (%s, %s, %s, %s, %s, %s, %s)"
ADD_HELP_DATA = "insert into {table_name}(username, query, created_on, updated_on) values (%s, %s, %s, %s)"
ADD_CUSTOMER_DATA = "insert into {nlp_database_name}.{table_name}(name, email, phone, address, username, pwd, dash_permission, prod_permission ,created_on, updated_on) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
ADD_PRODUCT_PLAN_DATA = "insert into {nlp_database_name}.{table_name}(username, email, phone, product_plan, created_on, updated_on) values (%s, %s, %s, %s, %s, %s)"
ADD_KHATABOOK_DATA = "insert into {table_name} (username, first_name, last_name, credit_debit, pay_method, amount, reason, date) values(%s, %s, %s, %s, %s, %s, %s, %s)"
ADD_ALL_ADMIN_DATA = "insert into {nlp_database_name}.{table_name} {all_columns_name} values {all_columns_value}"
ADD_TIPS_DATA = "insert into {table_name} (username, tip, short_des, descripation, file_path) values(%s, %s, %s, %s, %s)"
ADD_DASHBOARD_USER_DATA = "insert into {table_name} (username, permission) values (%s, %s)"
ADD_CUSTOMER_USER_DATA = "insert into {table_name} (username, permission) values (%s, %s)"
ADD_ALGO_ACCOUNT_DATA = "insert into {table_name} (username, user, token, password, vc, app_key, imei) values (%s, %s, %s, %s, %s, %s, %s)"


# delete queries
DELETE_DATA = "DELETE FROM {table_name} WHERE {col_name}='{col_value}' and {col_name1}='{col_value1}'"
