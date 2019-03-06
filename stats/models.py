from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from teams.models import Team
from people.models import Referee

# Create your models here.
class Season(models.Model):
    year = models.IntegerField()
    teams = models.IntegerField()

class Game(models.Model):

    GAME_TYPES = (
        ('Pre', 'Preseason Game'),
        ('Reg', 'Regular Season Gam'e),
        ('Post', 'Playoff Game')
    )
    season = models.ForeignKey('Season', models.CASCADE)
    game_type = models.CharField(choices=GAME_TYPES)
    away_team = models.ForeignKey(Team, models.CASCADE)
    home_team = models.ForeignKey(Team, models.CASCADE)
    away_score = models.IntegerField()
    home_score = models.IntegerField()
    winner = models.ForeignKey(Team, models.CASCADE)
    date_played = models.DateTimeField()
    location = models.CharField()
    attendance = models.IntegerField()
    referee_one = models.ForeignKey(Referee, models.SET_NULL, null=True)
    referee_two = models.ForeignKey(Referee, models.SET_NULL, null=True)
    referee_three = models.ForeignKey(Referee, models.SET_NULL, null=True)

class SeasonRecord(models.Model):
    season = models.ForeignKey(Season, models.CASCADE)
    team = models.ForeignKey(Team, models.CASCADE)
    wins = models.IntegerField()
    losses = models.IntegerField()
    seed = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(15)])
    playoffs = models.BooleanField()
    highest_playoff_round = models.IntegerField()
    championship = models.BooleanField()

class BoxScore(models.Model):
    game = models.ForeignKey(Game, models.CASCADE)
    team = models.ForeignKey(Team, models.CASCADE)
    home = models.BooleanField()
    mp = models.IntegerField()
    fg = models.IntegerField()
    fga = models.IntegerField()
    fg_pct = models.FloatField()
    three_p = models.IntegerField()
    three_pa = models.IntegerField()
    three_p_pct = models.FloatField()
    ft = models.IntegerField()
    fta = models.IntegerField()
    ft_pct = models.FloatField()
    orb = models.IntegerField()
    drb = models.IntegerField()
    trb = models.IntegerField()
    ast = models.IntegerField()
    stl = models.IntegerField()
    blk = models.IntegerField()
    tov = models.IntegerField()
    pf = models.IntegerField()
    pts = models.IntegerField()
    
    # Advanced Stats
    pace = models.FloatField() # num of possessions
    
    # ORtg = PTS/pace * 100
    ortg = models.FloatField()
    # DRtg = OPP PTS/pace * 100
    drtg = models.FloatField()

    # TSA = FGA + 0.44 * FTA, TSA: true shooting attempts
    # TS% = pts / 2 * TSA
    ts = models.FloatField()

    # eFG% = (FG + 0.5 * 3P)/FGA
    efg = models.FloatField()
    # 3pAr = 3PA / FGA
    three_par = models.FloatField()
    
    # FTr = FTA/FGA
    ftr = models.FloatField()

    # ORB% = ORB / (FGA - FG)
    orb_pct = models.FloatField()
    
    # DRB% = DRB / (DRB + OPP ORB)
    drb_pct = models.FloatField()

    # TRB% = TRB / (TRB + OPP TRB)
    trb_pct = models.FloatField()

    # AST% = AST / FG
    ast_pct = models.FloatField()

    # STL% = STL / pace
    stl_pct = models.FloatField()
    # BLK% = BLK / (OPP FGA - OPP 3PA)
    blk_pct = models.FloatField()
    # TOV% = 
    tov_pct = models.FloatField()