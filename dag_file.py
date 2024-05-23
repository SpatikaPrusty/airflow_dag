from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pytz
from airflow.utils.email import send_email
from airflow.models import Variable
# from airflow.operators.http_operator import SimpleHttpOperator
# import json

ecr_image_no = Variable.get("ecr_image_no")

ist_tz = pytz.timezone('Asia/Kolkata')

default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2024, 4, 26, 0, 0, tzinfo=ist_tz)
}

with DAG(
        dag_id='Airflow',
        default_args=default_args,
        catchup=False,
        schedule_interval="20 * * * *",
    ) as dag:

    FnD_load_start = DummyOperator(
        task_id="FnD_load_start",
        trigger_rule="all_success",
    )

    command = 'dbt run -m fct_intrmdry_trnsctn'

    ontology_run = KubernetesPodOperator(
        task_id='ontology_run',
        name='ontology_run',
        namespace="airflow",
        image=f'Image',
        image_pull_policy='Always',
        cmds=["bash", "-c"],
        arguments=[command],
        in_cluster=True,
        is_delete_operator_pod=True,
        labels={"DBT": "Ontology"},
        startup_timeout_seconds=300,
        do_xcom_push=False,
        trigger_rule='all_success',
        get_logs=True,
        dag=dag,
    )


    FnD_load_End = DummyOperator(
        task_id="FnD_load_End",
        trigger_rule="all_success",
    )

    FnD_load_start > ontology_run > FnD_load_End