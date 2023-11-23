from django.db import models


class DashboardRows(models.Model):
    participant_name = models.CharField("Participant name", max_length=200, blank=False)
    points = models.IntegerField("Points", blank=False, default='0')
    cash = models.IntegerField("Cash", blank=False, default='0')

    class Meta:
        verbose_name = "Dashboard row"
        verbose_name_plural = "Dashboard rows"
        db_table = 'dashboard_dashboardrows'

    def __str__(self):
        return f'{self.points} {self.participant_name}'

