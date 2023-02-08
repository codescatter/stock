import project_engine
from project_engine import yaml_data

DATE_FORMAT = '%a, %d %b %Y %H:%M:%S'
LOG_FORMAT = '[%(asctime)s] | %(levelname)-10s | %(message)s'
login_page_name = 'login_temp.html'
report_file_name = '/report_df.csv'
secure_type = "http"
pred_count = 10
cleanned_file_name = "cleanned_data.csv"
ml_model_filename = "ml_model.pkl"
confusion_matrix_filename = "confusion_matrix.csv"
classification_df_filename = "classification_df.csv"
file_path = "/project_engine/data/"

# default database names for checking the user and their roles.
DASHBOARD_USER_ROLE_TABLE = "dashboard_user_role"
DASHBOARD_PERMISSION_TABLE = "dashboard_permission"

# url prefix
SMART_BOT_URL_PREFIX = 'https://demo.turabit.com/api/revamp_{environment}/{file_name}.html'

# url
URL_DICT = {
    'wtUHWB2amtp3gWta': {
        'development': SMART_BOT_URL_PREFIX.format(environment='dev', file_name='DEV-vTech-IT-HR'),
        'qa': SMART_BOT_URL_PREFIX.format(environment='qa', file_name='QA-vTech-IT-HR')
    },
    'TdrpRamNxUdhyrvG': {
        'development': SMART_BOT_URL_PREFIX.format(environment='dev', file_name='DEV-Turabit-IT-HR'),
        'qa': SMART_BOT_URL_PREFIX.format(environment='qa', file_name='qa-turabit-it-hr')
    },
    'iBjMkOd1Gpr8MsyE': {
        'development': SMART_BOT_URL_PREFIX.format(environment='dev', file_name='DEV-GU'),
        'qa': SMART_BOT_URL_PREFIX.format(environment='qa', file_name='QA-GU')
    },
    'FszdmYpRf5Vp3tR3': {
        'development': SMART_BOT_URL_PREFIX.format(environment='dev', file_name='DEV-Karnavati'),
        'qa': SMART_BOT_URL_PREFIX.format(environment='qa', file_name='QA-Karnavati')
    },
    'FszdmYpRf5Vp3tR1': {
        'development': SMART_BOT_URL_PREFIX.format(environment='dev', file_name='DEV-Malhar'),
        'qa': SMART_BOT_URL_PREFIX.format(environment='qa', file_name='QA-Malhar')
    },
    'FszdmYpRf5Vp3tR4': {
        'development': SMART_BOT_URL_PREFIX.format(environment='dev', file_name='DEV-Phoenix'),
        'qa': SMART_BOT_URL_PREFIX.format(environment='qa', file_name='QA-Phoenix')
    },
    'wat8GT7SNqG7285r': {
        'development': SMART_BOT_URL_PREFIX.format(environment='dev', file_name='DEV-Uprize'),
        'qa': SMART_BOT_URL_PREFIX.format(environment='qa', file_name='QA-Uprize')
    },
    'yhgtrfedwsoliu6g': {
        'development': SMART_BOT_URL_PREFIX.format(environment='dev', file_name='dev-satyam'),
        'qa': SMART_BOT_URL_PREFIX.format(environment='qa', file_name='qa-satyam')
    },
    'YZUy6PKFTmew1Zhc': {
        'development': SMART_BOT_URL_PREFIX.format(environment='dev', file_name='DEV-Turabit-CX'),
        'qa': SMART_BOT_URL_PREFIX.format(environment='qa', file_name='QA-Turabit-CX')
    },
    'EuAOkZYx0KEBU56t': {
        'development': SMART_BOT_URL_PREFIX.format(environment='dev', file_name='DEV-vTech-CX'),
        'qa': SMART_BOT_URL_PREFIX.format(environment='qa', file_name='QA-vTech-CX')
    }
}
