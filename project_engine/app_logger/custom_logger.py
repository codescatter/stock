import logging

from logging.handlers import RotatingFileHandler
from concurrent.futures import ThreadPoolExecutor

from project_engine import app, yaml_data
from project_engine.project_constants import constants


class ActivityLogger:
    """
    Activity Logger will logs the incoming and outgoing request/response details. Handles three types of logging.

    a.  `StreamHandler`: Used for stderr error or stdout.
    b.  `RotatingFileHandler`: Used for enter logs in log file.
    c.  `CMRESHandler`: Used for insert logs in elastic-search.
    """

    activity_logger = logging.getLogger(app.import_name + '_activity_logs')
    app.logger.setLevel(logging.INFO)
    activity_file_path = yaml_data['log_file_path']['activity_log_records_path']
    activity_log_file_name = app.config.get('ACTIVITY_LOG_FILE_PATH', activity_file_path) \
        if not app.config.get('DEBUG') else activity_file_path

    formatter = logging.Formatter(fmt=constants.LOG_FORMAT, datefmt=constants.DATE_FORMAT)
    logging.basicConfig(format=constants.LOG_FORMAT, datefmt=constants.DATE_FORMAT, level=logging.DEBUG)

    # File Handler
    activity_rotating_file_handler = RotatingFileHandler(
        filename=activity_log_file_name, maxBytes=100 * 1024 * 1024, backupCount=10, mode='a'
    )
    activity_rotating_file_handler.setLevel(logging.DEBUG)

    activity_rotating_file_handler.setFormatter(formatter)
    activity_logger.addHandler(activity_rotating_file_handler)

    # Console Handler
    activity_console_handler = logging.StreamHandler()
    activity_console_handler.setLevel(logging.DEBUG)

    activity_console_handler.setFormatter(formatter)
    activity_logger.addHandler(activity_console_handler)

    def __init__(self):
        pass


class AppLogger(ActivityLogger):
    """
    App Logger will maintain all logs of this project. Handles three types of logging.

    a.  `StreamHandler`: Used for stderr error or stdout.
    b.  `RotatingFileHandler`: Used for enter logs in log file.
    c.  `CMRESHandler`: Used for insert logs in elastic-search.
    """

    logger = logging.getLogger(app.import_name)
    app.logger.setLevel(logging.DEBUG)
    file_path = yaml_data['log_file_path']['log_records_path']
    file_name = app.config.get('LOG_FILE_PATH', file_path) if not app.config.get('DEBUG') else file_path

    formatter = logging.Formatter(fmt=constants.LOG_FORMAT, datefmt=constants.DATE_FORMAT)
    logging.basicConfig(format=constants.LOG_FORMAT, datefmt=constants.DATE_FORMAT, level=logging.DEBUG)

    # File Handler
    rotating_file_handler = RotatingFileHandler(
        filename=file_name, maxBytes=100 * 1024 * 1024, backupCount=10, mode='a'
    )
    rotating_file_handler.setLevel(logging.DEBUG)

    rotating_file_handler.setFormatter(formatter)
    logger.addHandler(rotating_file_handler)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    def __init__(self):
        super().__init__()

    def log_stderr(self, **kwargs):
        """
        This method will be use for print errors on console. User this method instead of `print` statement in our entire
        code. Will work only if `DEBUG = True`.

        Such as,
            import sys
            sys.stderr

        :param kwargs:
        :return:
        """
        try:
            if app.config.get('DEBUG', False):
                self.log_stdout(**kwargs)
        except Exception as e:
            print(e)

    @staticmethod
    def log_stdout(**kwargs):
        """
        This method will be use for print output on console. User this method instead of `print` statement in our entire
        code. Will work only if `DEBUG = True`.

        Such as,
            import sys
            sys.stdout

        :param kwargs:
        :return:
        """
        try:
            if app.config.get('DEBUG', False):
                print(str(kwargs.get('msg', '')))
        except Exception as e:
            print(e)

    def log_debug(self, **kwargs):
        """
        This method will be use for `logging.debug`. Will work only if `DEBUG = True`.

        :param kwargs:  exc_info: True
        :return:
        """
        try:
            if app.config.get('DEBUG', False):
                self.async_logger(self.logger.debug, **kwargs)
        except Exception as e:
            self.async_logger(self.log_stderr, msg=str(e))

    def log_info(self, **kwargs):
        """
        This method will be use for `logging.info`.

        :param kwargs:  exc_info: True
        :return:
        """
        try:
            self.async_logger(self.logger.info, **kwargs)
        except Exception as e:
            self.async_logger(self.log_stderr, msg=str(e))

    def log_warning(self, **kwargs):
        """
        This method will be use for `logging.warning`.

        :param kwargs:  exc_info: True
        :return:
        """
        try:
            self.async_logger(self.logger.warning, **kwargs)
        except Exception as e:
            self.async_logger(self.log_stderr, msg=str(e))

    def log_error(self, **kwargs):
        """
        This method will be use for `logging.error`.

        :param kwargs:  exc_info: True
        :return:
        """
        try:
            self.async_logger(self.logger.error, **kwargs)
        except Exception as e:
            self.async_logger(self.log_stderr, msg=str(e))

    def log_critical(self, **kwargs):
        """
        This method will be use for `logging.critical`.

        :param kwargs:  exc_info: True
        :return:
        """
        try:
            self.async_logger(self.logger.critical, **kwargs)
        except Exception as e:
            self.async_logger(self.log_stderr, msg=str(e))

    def log_exception(self, **kwargs):
        """
        This method will be use for `logging.exception`.

        :param kwargs:  exc_info: True
        :return:
        """
        try:
            self.async_logger(self.logger.exception, **kwargs)
        except Exception as e:
            self.async_logger(self.log_stderr, msg=str(e))

    def activity_log_info(self, **kwargs):
        """
        This method will be use for `logging.info`.

        :param kwargs:  exc_info: True
        :return:
        """
        try:
            self.async_logger(self.activity_logger.info, **kwargs)
        except Exception as e:
            self.async_logger(self.log_stderr, msg=str(e))

    def log_incoming_request(self, **kwargs):
        """
        Log incoming requests.
        :param kwargs: :request: as parameter
        :return:
        """
        try:
            request = kwargs.get('request')
            if request:
                incoming_request = {
                    'data': request.json,
                    'access_route': request.access_route,
                    'headers': request.headers,
                    'url_rule': request.url_rule
                }
                self.activity_log_info(msg=str(incoming_request), is_activity=True)

        except Exception as e:
            self.async_logger(self.log_stderr, msg=str(e))

    def log_api_response(self, **kwargs):
        """
        Log API Response.
        :param kwargs:  response: pass `response` as parameter
                        data: pass `data` that you have been pass as JSON, body or headers.
        :return:
        """
        try:
            response = kwargs.get('response')
            if response:
                api_response = {
                    'data': kwargs.get('data', ''),
                    'status_code': response.status_code,
                    'url_rule': response.url,
                    'response_text': response.json()
                }
                self.activity_log_info(msg=str(api_response), is_activity=True)

        except Exception as e:
            self.async_logger(self.log_stderr, msg=str(e))

    def async_logger(self, func, **kwargs):
        """
        This method handles asynchronous calls for logging. Also, handles additional fields for Elastic Search.

        :param func: Function name that we are going to execute.
        :param kwargs:
        :return:
        """
        try:
            with ThreadPoolExecutor(max_workers=5) as executor:

                app_name, is_activity = app.import_name, False
                if kwargs.get('is_activity'):

                    if not app.config.get('ACTIVITY_LOGGER'):
                        return

                    app_name, is_activity = app.import_name + '_activity_logs', True
                    kwargs.pop('is_activity')

                executor.map(func(**kwargs))
        except Exception as e:
            print(e)
