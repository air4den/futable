from django.db import models

# Create your models here.
class Match(models.Model):
    class Meta:
        db_table = 'matches_table_match'
    match_date = models.DateField(db_index=True)
    league = models.CharField(max_length=100, db_index=True)
    season = models.CharField(max_length=20, db_index=True)
    home = models.CharField(max_length=200)
    away = models.CharField(max_length=200)
    home_score = models.PositiveIntegerField()
    away_score = models.PositiveIntegerField()

    @property
    def home_table_points(self) -> int:
        goal_diff = self.home_score - self.away_score
        result_pts = 0
        if (goal_diff > 0):
            result_pts = 3
        elif (goal_diff == 0):
            result_pts = 1
        elif (goal_diff < 0):
            result_pts = 0
        return result_pts
    
    @property
    def away_table_points(self) -> int:
        goal_diff = self.away_score - self.home_score
        result_pts = 0
        if (goal_diff > 0):
            result_pts = 3
        elif (goal_diff == 0):
            result_pts = 1
        elif (goal_diff < 0):
            result_pts = 0
        return result_pts
    
    def __str__(self):
        return f"{self.home_club} vs {self.away_club} on {self.match_date}: {self.home_score}-{self.away_score}"