# dags/dbt_kubernetes_pod_dag.py

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dbt_kubernetes_pod_dag',
    default_args=default_args,
    description='A simple DAG to run dbt on Kubernetes without environment variables',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['dbt', 'kubernetes'],
) as dag:

    dbt_run = KubernetesPodOperator(
        namespace='default',
        image='fishtownanalytics/dbt:latest',  # Use the appropriate dbt image
        cmds=["dbt"],
        arguments=["run"],
        labels={"app": "dbt"},
        name="dbt-run",
        task_id="dbt_run_task",
        get_logs=True,
        is_delete_operator_pod=True,
        in_cluster=True,
        config_file=None,
        startup_timeout_seconds=600,
    )

    dbt_run
