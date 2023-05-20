import pytest
from mixer.backend.django import mixer

from ..models import Project

pytestmark = pytest.mark.django_db


def test_project_str_returns_name():
    """
    __str__() returns project name
    """
    project = mixer.blend(Project)
    assert project.__str__() == project.name, "Should return project name"
