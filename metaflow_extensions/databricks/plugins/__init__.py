from metaflow.decorators import StepDecorator
from metaflow.exception import CommandException

class DatabricksDecorator(StepDecorator):
    name = "ob_databricks"
    defaults = {
        "job_name": None,
    }

    AUTH = { # FIXME
        'host': "dbc-8f5f55db-1fec.cloud.databricks.com",
        'token': "dapi18fddda1832c4a545c74e765e21dc9ad"
    }

    def task_decorate(
        self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context
    ):
        from .databricks_ops import run_job
        from databricks.sdk import WorkspaceClient

        w = WorkspaceClient(**self.AUTH)

        job_name = self.attributes['job_name']
        for job in w.jobs.list():
            if job.settings.name == job_name:
                self.job_id = job.job_id
                break
        else:
            raise CommandException(f'@databricks in step[{step_name}]: Job name *{job_name}* not found in the Databricks workspace')

        return run_job(w, flow, step_func, job_id, **self.attributes)

STEP_DECORATORS_DESC = [('ob_databricks', ".DatabricksDecorator")]
