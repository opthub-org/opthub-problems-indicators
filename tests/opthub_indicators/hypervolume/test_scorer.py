"""Test for the calculation of the hypervolume scorer."""

from typing import TYPE_CHECKING

from opthub_indicators.hypervolume.scorer import calculate_score

if TYPE_CHECKING:
    from opthub_indicators.hypervolume.validator import SolutionScored, SolutionToScore

EPS = 1e-6


def test_2d_without_ref_point() -> None:
    """Test the calculation of the hypervolume scorer with 2D."""
    ref_point = None
    solution_to_score: SolutionToScore = {"objective": [1.0, 1.0], "feasible": True}
    solutions_scored: list[SolutionScored] = [
        {"objective": [2.0, 0.0], "feasible": True},
        {"objective": [0.0, 2.0], "feasible": True},
    ]
    score = calculate_score(ref_point, solution_to_score, solutions_scored)

    if abs(score["score"] - 1.0) > EPS:
        msg = f"Expected score: 1.0, but got: {score['score']}"
        raise ValueError(msg)


def test_2d_with_ref_point() -> None:
    """Test the calculation of the hypervolume scorer with 2D and a reference point."""
    ref_point = [2.0, 4.0]
    solution_to_score: SolutionToScore = {"objective": [1.0, 1.0], "feasible": True}
    solutions_scored: list[SolutionScored] = [
        {"objective": [2.0, 0.0], "feasible": True},
        {"objective": [0.0, 2.0], "feasible": True},
    ]
    score = calculate_score(ref_point, solution_to_score, solutions_scored)

    if abs(score["score"] - 5.0) > EPS:
        msg = f"Expected score: 5.0, but got: {score['score']}"
        raise ValueError(msg)


def test_2d_with_infeasible() -> None:
    """Test the calculation of the hypervolume scorer with 2D and an infeasible solution."""
    ref_point = None
    solution_to_score: SolutionToScore = {"objective": [0.5, 1.0], "feasible": False}
    solutions_scored: list[SolutionScored] = [
        {"objective": [2.0, 0.0], "feasible": True},
        {"objective": [0.0, 2.0], "feasible": True},
        {"objective": [1.0, 1.0], "feasible": True},
        {"objective": [1.0, 0.5], "feasible": False},
    ]
    score = calculate_score(ref_point, solution_to_score, solutions_scored)

    if abs(score["score"] - 1.0) > EPS:
        msg = f"Expected score: 1.0, but got: {score['score']}"
        raise ValueError(msg)