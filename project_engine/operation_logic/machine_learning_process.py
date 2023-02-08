# import pandas as pd
# import numpy as np
# import joblib
# from sklearn.model_selection import train_test_split, cross_val_score
# from sklearn.metrics import classification_report, confusion_matrix
# from flask import session
# from project_engine.project_constants.constants import cleanned_file_name, file_path, ml_model_filename, confusion_matrix_filename, classification_df_filename
# from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder, PolynomialFeatures
# from sklearn.pipeline import Pipeline
# from sklearn.linear_model import LinearRegression, Ridge, Lasso, LogisticRegression
# from sklearn.svm import SVC, SVR
# from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
# from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, BaggingClassifier, BaggingRegressor, IsolationForest, StackingRegressor, GradientBoostingRegressor, GradientBoostingClassifier, AdaBoostClassifier, AdaBoostRegressor, ExtraTreesClassifier, ExtraTreesRegressor, StackingClassifier, VotingClassifier
# from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
# from sklearn.naive_bayes import BernoulliNB
# from project_engine.project_constants.constants import pred_count
#
# class Build_ML_Model:
#     """ This class will scrape all links then iterate over that links
#          and scrape data and at last with main function returns all scrape data in JSON"""
#
#
#     def create_ml_model(self, csv_path, column_name, dc_method, ohe_method, ml_model, fs_method):
#         try:
#             ml_model_spliting = ml_model.split()
#             df = pd.read_csv(csv_path)
#
#             all_columns = df.columns
#             num_cols = df.select_dtypes(["int64","float64"]).keys()
#             cat_cols = df.select_dtypes("O").keys()
#
#             pred_column = column_name
#             non_pred_column = all_columns.drop(column_name)
#
#             if dc_method.lower()=="pandas":
#                 for num_c in num_cols:
#                     df[num_c].fillna(df[num_c].mean(), inplace=True)
#
#                 for cat_c in cat_cols:
#                     count = df[cat_c].value_counts().keys()
#                     df[cat_c].fillna(count[0], inplace=True)
#             else:
#                 for num_c in num_cols:
#                     df[num_c].fillna(df[num_c].mean(), inplace=True)
#
#                 for cat_c in cat_cols:
#                     count = df[cat_c].value_counts().keys()
#                     df[cat_c].fillna(count[0], inplace=True)
#
#             decide_reg_cla = df["pred_column"].unique()
#             value_count = len(decide_reg_cla)
#
#             df.to_csv(file_path+cleanned_file_name)
#             X = df.drop(non_pred_column, axis=1)
#             y = df[non_pred_column]
#
#             X_train, y_train, X_test, y_test = train_test_split(X, y, test_size=0.20)
#
#             if fs_method.lower()=="yes":
#                 sc = StandardScaler()
#                 X_train = sc.fit_transform(X_train)
#                 X_test = sc.fit_transform(X_test)
#
#             if value_count>pred_count:
#                 flag = "Regression"
#             else:
#                 flag = "Classification"
#
#             if flag == "Regression":
#                 first_word = ml_model_spliting[0]
#                 X_train, X_test, y_train, y_test
#                 if first_word.lower() == "linear":
#                     lr = LinearRegression()
#                     acc = self.common_model(lr, X_train, X_test, y_train, y_test)
#                     return acc
#                 elif first_word.lower() == "ridge":
#                     rd = Ridge()
#                     acc = self.common_model(rd)
#                     return acc
#                 elif first_word.lower() == "lasso":
#                     ls = Lasso()
#                     acc = self.common_model(ls)
#                     return acc
#                 elif first_word.lower() == "support":
#                     svr = SVR()
#                     acc = self.common_model(svr)
#                     return acc
#                 elif first_word.lower() == "decision":
#                     dtr = DecisionTreeRegressor()
#                     acc = self.common_model(dtr)
#                     return acc
#                 elif first_word.lower() == "random":
#                     rfr = RandomForestRegressor()
#                     acc = self.common_model(rfr)
#                     return acc
#                 elif first_word.lower() == "k-nearest":
#                     knr = KNeighborsRegressor()
#                     acc = self.common_model(knr)
#                     return acc
#                 elif first_word.lower() == "bagging":
#                     br = BaggingRegressor()
#                     acc = self.common_model(br)
#                     return acc
#                 elif first_word.lower() == "adaboost":
#                     ada = AdaBoostRegressor()
#                     acc = self.common_model(ada)
#                     return acc
#                 elif first_word.lower() == "extraTrees":
#                     etr = ExtraTreesRegressor()
#                     acc = self.common_model(etr)
#                     return acc
#                 elif first_word.lower() == "grediantBoosting":
#                     gbr = GradientBoostingRegressor()
#                     acc = self.common_model(gbr)
#                     return acc
#                 elif first_word.lower() == "stacking":
#                     sr = StackingRegressor()
#                     acc = self.common_model(sr)
#                     return acc
#                 elif first_word.lower() == "polynomial":
#                     poly =
#                 else:
#                     return 400
#             else:
#
#
#
#
#
#
#
#
#
#
#
#         return 200
#
#     def common_model(self, instant_name, X_train, X_test, y_train, y_test):
#         instant_name.fit(X_train, y_train)
#         y_pred = instant_name.predict(X_test)
#         acc = instant_name.score(X_test, y_test)
#
#         joblib.dump(instant_name, file_path + ml_model_filename)
#
#         cm = confusion_matrix(y_test, y_pred)
#         cm_df = pd.DataFrame(cm, index=["TP", "FN"], columns=["TP", "FP"])
#         cm_df.to_csv(file_path + confusion_matrix_filename)
#
#         report = classification_report(y_test, y_pred, output_dict=True)
#         classification_df = pd.DataFrame(report).transpose()
#         classification_df.to_csv(file_path + confusion_matrix_filename)
#         return acc
#
#     def method_pred(self, csv_path):
#         try:
#             df = pd.read_csv(csv_path)
#             all_columns_name = df.columns
#             return all_columns_name
#
#         except Exception as e:
#             return 400
