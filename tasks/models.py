from django.db import models
from django.contrib.auth import get_user_model


class Project(models.Model):
    """
    Project in Taskroo is to group together bunch of tasks with
    tasks number. Treat Project more like a task categories.
    The reason for having a task number is to be able to uniquely
    identify tasks in CLI. 

    We could just use task ID as a unique identifier for CLI as well.
    However, I want to have GitHub Issues style numbering for tasks identifier
    in each project. Basically, I want each tasks number to always start from
    1 in every new project.

    This allows CLI to do something like:

    > taskroo list
    Tasks in project "blah blah"
    1. [-] do something amazing
    2. [-] Another amazing tasks
    3. [-] Motivativng tasks is here 

    > taskroo done 2
    2. [X] Another amazing tasks

    > taskroo list
    Tasks in project "blah blah"
    1. [-] do something amazing
    2. [X] Another amazing tasks
    3. [-] Motivativng tasks is here 
    """
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="projects")
    last_task_number = models.PositiveIntegerField()

    def __str__(self):
        """ Return name """
        return self.name


class Status(models.Model):
    """
    Status represents the current status of an individual task.
    """
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """ Return name """
        return self.name


class Task(models.Model):
    """
    Task represents an individual todo item or task
    """
    title = models.CharField(max_length=150)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()

    def __str__(self):
        """ return title """
        return self.title
