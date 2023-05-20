import pytest
from mixer.backend.django import mixer

from ..models import Project, Status, Task

pytestmark = pytest.mark.django_db


def test_project_str_returns_name():
    """
    __str__ returns project name
    """
    project = mixer.blend(Project)
    assert str(project) == project.name, "Should return project name"


def test_status_str_returns_name():
    """
    __str__ returns status name
    """
    status = mixer.blend(Status)
    assert str(status) == status.name, "Should return status name"


def test_task_str_returns_title():
    """
    __str__() returns task title
    """
    task = mixer.blend(Task)
    assert str(task) == task.title, "Should return task title"
