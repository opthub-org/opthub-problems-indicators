"""The indicator to calculate the hyper volume."""

import json
import logging
import sys
from traceback import format_exc

import click

from opthub_indicators.hypervolume.scorer import calculate_score
from opthub_indicators.hypervolume.validator import (
    validate_ref_point,
    validate_trial_to_score,
    validate_trials_scored,
)

LOGGER = logging.getLogger(__name__)


@click.command(help="The indicator to calculate the hyper volume.")
@click.option(
    "-r",
    "--ref-point",
    type=str,
    default=None,
    envvar="HV_REF_POINT",
    help="Reference point.",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Log level.",
)
def main(ref_point: str, log_level: str) -> None:
    """Calculate the hyper volume."""
    logging.basicConfig(level=log_level)
    LOGGER.info(("ref_point: ", ref_point))
    try:
        # Validate the input
        LOGGER.info("Validating the input...")

        trial_to_score = json.loads(input())
        trials_scored = json.loads(input())
        validated_ref_point = validate_ref_point(json.loads(ref_point) if ref_point is not None else None)
        validated_trial_to_score = validate_trial_to_score(trial_to_score)

        validated_trials_scored = validate_trials_scored(trials_scored)
        LOGGER.info("...Validated.")
        LOGGER.debug("ref_point: %s", validated_ref_point)
        LOGGER.debug("trial_to_score: %s", validated_trial_to_score)
        LOGGER.debug("trials_scored: %s", validated_trials_scored)

        # Calculate the score
        LOGGER.info("Calculating the score...")
        score = calculate_score(validated_ref_point, validated_trial_to_score, validated_trials_scored)
        LOGGER.info("...Calculated.")
        LOGGER.debug("score: %s", score)

        # Output the result
        LOGGER.info("Outputting the result...")
        sys.stdout.write(json.dumps(score))
        LOGGER.info("...Outputted.")

    except Exception as e:
        LOGGER.exception(format_exc())
        LOGGER.info("Outputting the result...")
        sys.stdout.write(json.dumps({"score": None, "error": str(e)}))
        LOGGER.info("...Outputted.")


if __name__ == "__main__":
    main()
