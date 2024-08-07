"""Sphere function minimization problem."""

import json
import logging
import sys
from traceback import format_exc
from typing import cast

import click
import numpy as np
from jsonschema import validate

from problem_opt_benchmarks.sphere.schema import OPTIMA_SCHEMA, VARIABLE_1D_SCHEMA, VARIABLE_ND_SCHEMA

LOGGER = logging.getLogger(__name__)


def sphere(variable: list[float], optimal: list[list[float]]) -> list[float]:
    """Calculate the sphere function value.

    Args:
        variable (list[float]): decision variable
        optimal (list[list[float]]): optimal value

    Returns:
        list[float]: objective value
    """
    variable_arr = np.array(variable, dtype=float)
    optima_arr = np.array(optimal, dtype=float)
    eval_arr = np.sum((variable_arr - optima_arr) ** 2, axis=1)
    return cast(list[float], eval_arr.tolist())


@click.command(help="Sphere function minimization problem.")
@click.option(
    "-o",
    "--optima",
    type=str,
    envvar="SPHERE_OPTIMA",
    help="Optimal value for the sphere function.",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Log level.",
)
def main(optima: str, log_level: str) -> None:
    """Evaluate a given solution on a multi-objective unconstrained sphere problem."""
    logging.basicConfig(level=log_level)

    try:
        # Validate the input
        LOGGER.info("Validating the input...")
        opt = json.loads(optima)
        validate(instance=opt, schema=json.loads(OPTIMA_SCHEMA))

        decision_dim = len(opt[0])
        variable = json.loads(input())

        if decision_dim == 1:
            combined = {
                "anyOf": [json.loads(VARIABLE_1D_SCHEMA), json.loads(VARIABLE_ND_SCHEMA.format(items=1))],
            }
            validate(instance=variable, schema=combined)
        else:
            validate(instance=variable, schema=json.loads(VARIABLE_ND_SCHEMA.format(items=decision_dim)))
        LOGGER.info("...Validated.")

        LOGGER.debug("variable: %s", variable)
        LOGGER.debug("optima: %s", opt)
        LOGGER.debug("decision_dim: %s", decision_dim)

        # Evaluate variable
        LOGGER.info("Evaluating the variable...")
        objective = sphere(variable, opt)
        LOGGER.info("...Evaluated.")

        LOGGER.debug("objective: %s", objective)

        # Output the result
        LOGGER.info("Outputting the result...")
        sys.stdout.write(json.dumps({"objective": objective[0] if len(objective) == 1 else objective}))
        LOGGER.info("...Outputted.")

    except Exception as e:
        LOGGER.exception(format_exc())
        LOGGER.info("Outputting the result...")
        sys.stdout.write(json.dumps({"objective": None, "error": str(e)}))
        LOGGER.info("...Outputted.")


if __name__ == "__main__":
    main()
