from functools import wraps

class databricks():

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, f):
        from metaflow import card, ob_databricks
        return card(type='blank', id='databricks', refresh_interval=1)(ob_databricks(**self.kwargs)(f))