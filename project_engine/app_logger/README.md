# App Logger

**Note:**
Do not use any `print` statement in entire code. We have been defined some methods there those will help you for such stuff. This below some of the methods act as per the current project environment.

`log_stderr`,
`log_stdout`,
`log_debug`,
`log_info`,
`log_warning`,
`log_error`,
`log_critical`

Use `log_stderr`, `log_stdout` this two methods instead of `print` statement. Follow below parameters in case of other methods.

```python
logger.log_error(msg='Something', exc_info=True)

# Elastic Search Additional Fields
# Additional field must be registered as described below section. 
logger.log_error(msg='Something', exc_info=True, company_name='Turabit')
```

Follow below steps to integrate this app with out project.

* Paste this app as sibling of other apps in your project.
* To add app in you project configure it in your configuration files as per environment, such as `default.yaml`.

```yaml
installed_apps:
  - nlp_engine.process_controller
  - nlp_engine.app_logger
```
Also, you must add some ElasticSearch host and ports at the end of same file.
```yaml
app_logger:
  - elastic-search: localhost
    host: 0.0.0.0
    port: 9200
  #    Such a way we can set multiple hosts for elastic search
  #  - elastic-search: aws-elastic
  #    host: 0.0.0.0
  #    port: 9200
```
* Now, Import and declare variable at exact below of api declaration like,
```python
# Registered Flask Rest API
api = Api(app)

from nlp_engine.app_logger.custom_logger import AppLogger

logger = AppLogger()
```
* **Optional:** You need to register additional fields if required for elastic search. Ex:
```python custom_logger.py
# Register additional parameters here if we want to add
elastic_search_handler.es_additional_fields = {
    'company_name': '',
    'client_id': ''
}
```

Now, you can use this variable by importing in your app and modules as you want.