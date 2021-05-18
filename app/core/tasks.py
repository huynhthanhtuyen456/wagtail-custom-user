from celery.schedules import crontab
from celery.task import PeriodicTask, Task


class TestPeriodicTask(PeriodicTask):
    # Execute every minute
    run_every = crontab(minute=1)

    def run(self):
        print('Periodic Task is running ....')
