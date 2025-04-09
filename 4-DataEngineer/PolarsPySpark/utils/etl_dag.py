# etl_dag.py
import asyncio
import logging
import time
import os
from typing import Dict, List, Callable, Any, Set, Union
import subprocess
import sys

class Task:
    def __init__(self, name: str, func: Callable, *args, **kwargs):
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.upstream_tasks: Set[Task] = set()
        self.downstream_tasks: Set[Task] = set()
        self.logger = logging.getLogger(f"ETL.Task.{name}")

    def set_upstream(self, task: Union['Task', List['Task']]):
        if isinstance(task, list):
            for t in task:
                self.upstream_tasks.add(t)
                t.downstream_tasks.add(self)
        else:
            self.upstream_tasks.add(task)
            task.downstream_tasks.add(self)
        return self

    def set_downstream(self, task: Union['Task', List['Task']]):
        if isinstance(task, list):
            for t in task:
                self.downstream_tasks.add(t)
                t.upstream_tasks.add(self)
        else:
            self.downstream_tasks.add(task)
            task.upstream_tasks.add(self)
        return self

    async def run(self) -> Any:
        self.logger.info(f"Iniciando tarea '{self.name}'")
        start_time = time.time()

        try:
            if asyncio.iscoroutinefunction(self.func):
                result = await self.func(*self.args, **self.kwargs)
            else:
                result = self.func(*self.args, **self.kwargs)

            elapsed = time.time() - start_time
            self.logger.info(f"Tarea '{self.name}' completada en {elapsed:.2f} segundos")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            self.logger.error(f"Error en tarea '{self.name}' después de {elapsed:.2f} segundos: {str(e)}")
            raise

class DAG:
    def __init__(self, dag_id: str, description: str = ""):
        self.dag_id = dag_id
        self.description = description
        self.tasks: Dict[str, Task] = {}
        self.logger = logging.getLogger(f"ETL.DAG.{dag_id}")

    def task(self, name: str, func: Callable, *args, **kwargs) -> Task:
        task = Task(name, func, *args, **kwargs)
        self.tasks[name] = task
        return task

    def get_execution_order(self) -> List[Task]:
        remaining_tasks = list(self.tasks.values())
        execution_order = []

        while remaining_tasks:
            ready_tasks = [
                task for task in remaining_tasks
                if all(dep in execution_order for dep in task.upstream_tasks)
            ]

            if not ready_tasks and remaining_tasks:
                cyclic_tasks = [t.name for t in remaining_tasks]
                self.logger.error(f"Ciclo detectado entre tareas: {cyclic_tasks}")
                raise ValueError("Ciclo detectado en el DAG")

            execution_order.extend(ready_tasks)
            for task in ready_tasks:
                remaining_tasks.remove(task)

        return execution_order

    async def run(self) -> Dict[str, Any]:
        self.logger.info(f"Iniciando DAG '{self.dag_id}'")
        start_time = time.time()

        execution_order = self.get_execution_order()
        results = {}

        try:
            for task in execution_order:
                results[task.name] = await task.run()

            elapsed = time.time() - start_time
            self.logger.info(f"DAG '{self.dag_id}' completado en {elapsed:.2f} segundos")
            return results
        except Exception as e:
            elapsed = time.time() - start_time
            self.logger.error(f"Error en DAG '{self.dag_id}' después de {elapsed:.2f} segundos: {str(e)}")
            raise

def run_script(script_path):
    python_executable = sys.executable
    env = os.environ.copy()

    if not os.path.exists(script_path):
        local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_path)
        if os.path.exists(local_path):
            script_path = local_path

    python_path = os.pathsep.join(sys.path)
    if 'PYTHONPATH' in env:
        env['PYTHONPATH'] = python_path + os.pathsep + env['PYTHONPATH']
    else:
        env['PYTHONPATH'] = python_path

    result = subprocess.run(
        [python_executable, script_path],
        capture_output=True,
        text=True,
        env=env
    )

    if result.returncode != 0:
        error_msg = f"Error en script {script_path}:\n{result.stderr}"
        logging.error(error_msg)
        raise RuntimeError(error_msg)

    return result.stdout