import functools
import time

from metaflow import current
from metaflow.cards import Markdown, Table

import pandas as pd

def run_job(db_client, flow, step_func, job_id, job_name=None):

    @functools.wraps(step_func)
    def databricks_step():
        current.card['databricks'].append(Markdown(f'# {job_name.capitalize()}'))
        current.card['databricks'].refresh()
        run = db_client.jobs.run_now(job_id=job_id)
        current.card['databricks'].append(Markdown(f'#### Run ID: `{run.run_id}`'))
        status = Markdown(f'#### Status: `STARTED`')
        current.card['databricks'].append(status)
        duration = Markdown(f'#### Duration: 0 seconds')
        current.card['databricks'].append(duration)
        current.card['databricks'].refresh()
        start = time.time()
        while True:
            run_status = db_client.jobs.get_run(run_id=run.run_id)
            state = str(run_status.state.life_cycle_state).split('.')[-1]
            if state == 'RUNNING':
                pretty_state = 'RUNNING 🏃'
            elif state == 'TERMINATED':
                pretty_state = 'TERMINATED ✅'
            else:
                pretty_state = state
            status.update(f'#### Status: `{pretty_state}` {run_status.state.state_message}')
            d = int(time.time() - start) 
            duration.update(f'#### Duration: {d} seconds')
            current.card['databricks'].append(duration)
            current.card['databricks'].refresh()

            if state == "TERMINATED":
                job_status = db_client.jobs.get_run(run_id=run.run_id)
                last_task = list(job_status.tasks)[-1]
                out = db_client.jobs.get_run_output(run_id=last_task.run_id)
                current.card.append(Markdown("## Result"))
                if out.notebook_output.result is None:
                    current.card.append(Markdown("No output"))
                    flow.databricks_output = None
                else:
                    df = pd.read_json(out.notebook_output.result)
                    current.card.append(Table.from_dataframe(df))
                    flow.databricks_output = df
                break

            elif state in ["SKIPPED", "INTERNAL_ERROR"]:
                current.card.append(Markdown("### Job failed"))
                break

            # Wait for some time before checking again
            time.sleep(3)

        step_func()


    return databricks_step