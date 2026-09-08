import pytest

from workflow.agents.tech_lead import Ticket
from workflow.pipeline import DependencyCycleError, plan_waves


def _t(tid, deps=()):
    return Ticket(id=tid, title=tid, depends_on=list(deps))


def test_plan_waves_orders_and_parallelizes():
    tickets = [_t("T1"), _t("T2"), _t("T3", ("T1", "T2")), _t("T4", ("T3",))]
    assert plan_waves(tickets) == [["T1", "T2"], ["T3"], ["T4"]]


def test_plan_waves_detects_cycle():
    tickets = [_t("T1", ("T2",)), _t("T2", ("T1",))]
    with pytest.raises(DependencyCycleError):
        plan_waves(tickets)


def test_plan_waves_ignores_unknown_deps():
    tickets = [_t("T1"), _t("T2", ("TX",))]
    assert plan_waves(tickets) == [["T1", "T2"]]
