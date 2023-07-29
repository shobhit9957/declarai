from time import time
from typing import Any, Callable, Dict

from rich.progress import Progress
from rich.table import Table

from declarai import Declarai


def evaluate_single_task_scenario(
    scenario_name: str,
    scenario: Callable,
    scenario_kwargs: Dict[str, Any],
    models: Dict[str, Declarai],
    table: Table,
):
    with Progress() as progress:
        evaluator = progress.add_task(f"[red]{scenario_name}...", total=len(models))

        for model, declarai in models.items():
            initialized_scenario = declarai.task(scenario)

            start_time = time()
            res = initialized_scenario(**scenario_kwargs)
            total_time = time() - start_time
            progress.update(evaluator, advance=1)

            table.add_row(
                declarai.llm_config.provider,
                declarai.llm_config._model,
                declarai.llm_config._version or "latest",
                scenario_name,
                f"{round(total_time, 3)}s",
                str(res),
            )


def evaluate_sequence_task_scenario(
    scenario_name: str,
    scenario: Callable,
    scenario_kwargs: Dict[str, Any],
    models: Dict[str, Declarai],
    table: Table,
):
    with Progress() as progress:
        evaluator = progress.add_task(f"[red]{scenario_name}...", total=len(models))

        for model, declarai in models.items():
            initialized_scenario = scenario(declarai, **scenario_kwargs)
            start_time = time()
            res = initialized_scenario()
            total_time = time() - start_time
            progress.update(evaluator, advance=1)

            table.add_row(
                declarai.llm_config.provider,
                declarai.llm_config._model,
                declarai.llm_config._version or "latest",
                scenario_name,
                f"{round(total_time, 3)}s",
                str(res),
            )