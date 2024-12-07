from metaflow import FlowSpec, kubernetes, step, current, project, Flow, pypi_base
from ob_databricks import databricks

@pypi_base(packages={'databricks-sdk': '0.38.0', 'pandas': '2.2.3'})
class DatabricksFlow(FlowSpec):

    @databricks(job_name='query latest data')
    @step
    def start(self):
        print('output df', self.databricks_output)
        self.next(self.end)

    @databricks(job_name='create ob event')
    @step
    def end(self):
        print('completed')

if __name__ == '__main__':
    DatabricksFlow()
