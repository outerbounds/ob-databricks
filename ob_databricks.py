from functools import wraps

class databricks():

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    """
    @wraps(f)
    def wrapper(self):
        self.highlight = HighlightData()
        try:            
            f(self)
            if self.highlight._modified():
                Flow(current.flow_name)[current.run_id].add_tag("highlight")
        finally:
            self.highlight_data = self.highlight._serialize()
            del self.highlight
    """

    def __call__(self, f):
        from metaflow import card, ob_databricks
        return card(type='blank', id='databricks', refresh_interval=1)(ob_databricks(**self.kwargs)(f))