import copy
from datetime import datetime

import pytest

from content_planner.agent import Agent
from content_planner.policy import Catalog, Clock
from content_planner.schemas import DemoConfig, Limits
from content_planner.storage import Storage


@pytest.fixture
def request_input():
    return {"request_id": "test-001", "theme": "咖啡杯新品营销活动", "product_id": "P001",
            "budget_units": "20", "deadline_at": "2030-01-01T10:30:00+08:00"}


@pytest.fixture
def storage(tmp_path):
    store = Storage(tmp_path / "tasks.db")
    yield store
    store.close()


@pytest.fixture
def run_task(storage, request_input):
    def run(changes=None, faults=None, limits=None, model=None, catalog=None):
        raw = copy.deepcopy(request_input)
        raw.update(changes or {})
        demo = DemoConfig.model_validate({"faults": faults or []})
        agent = Agent(storage, catalog or Catalog(), Clock(datetime.fromisoformat("2030-01-01T10:00:00+08:00")),
                      model=model, limits=limits or Limits(), demo=demo)
        return agent.run(raw)
    return run
