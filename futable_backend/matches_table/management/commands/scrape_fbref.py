from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from matches_table.models import Match
import sqlite3

import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

class Command(BaseCommand):
    help = 'Scrape match data.'
    
    def add_arguments(self, parser):
        parser.add_argument('league', type=str)
        parser.add_argument('season', type=str)

    def handle(self, *args, **options):
        league = options['league']  # "Premier-League"
        season = options['season']  # "2024-2025", "2023-2024"

        df = scrape_league(league=league, season=season)

        df_to_sql_pd(df)

        self.stdout.write(self.style.SUCCESS(f"Scraped data for {league} {season}."))


def df_to_model_django(df):
    match_objs = []
    for row in df.itertuples(index=False):
        match_objs.append(
            Match(
                match_date=row.match_date,
                home=row.home,
                away=row.away,
                home_score=row.home_score,
                away_score=row.away_score,
            )
        )
    Match.objects.bulk_create(match_objs)

def df_to_sql_pd(df):
    db_path = settings.DATABASES['default']['NAME']

    with sqlite3.connect(db_path) as connection:
        df.to_sql(
        name='matches_table_match',
        con=connection,
        if_exists='append',        # TODO: fix this so db will be added too only if new matches (current season) have been placed since last updated; will need to be 'append'
        index=False
        )

def scrape_league(league: str, season: str) -> pd.core.frame.DataFrame:
    LEAGUE_URLS = {
            'Premier-League': f'https://fbref.com/en/comps/9/{season}/schedule/{season}-Premier-League-Scores-and-Fixtures',
            'La-Liga': f'https://fbref.com/en/comps/12/{season}/schedule/{season}-La-Liga-Scores-and-Fixtures'
        }

    url = LEAGUE_URLS.get(league)
    if not url:
        raise KeyError(f"Unknown league: {league}.")
    
    response = requests.get(url)
    print(str(response.status_code))

    if response.status_code != 200:
        raise Exception("Error getting response from http request.")

    url_league_num = url.split('/')[5]
    table_id = f'sched_{season}_{url_league_num}_1'

    soup = BeautifulSoup(response.text, 'html.parser')
    schedule_table = soup.find('table', {'id': table_id})

    df = pd.read_html(StringIO(str(schedule_table)))[0]
    df = df.dropna(how='all')

    df[['home_score', 'away_score']] = df['Score'].str.split(r'\D+', expand=True)

    df = df.rename({'Home': 'home', 
                    'Away': 'away', 
                    'Date': 'match_date'}, axis="columns")
    
    df['league'] = league
    df['season'] = season
    COLS_KEEP = ['match_date', 'league', 'season', 'home', 'away', 'home_score', 'away_score']

    df['match_date'] = pd.to_datetime(df['match_date'], errors='coerce').dt.date
    df['home_score'] = pd.to_numeric(df['home_score'], errors='coerce').fillna(0).astype(int)
    df['away_score'] = pd.to_numeric(df['away_score'], errors='coerce').fillna(0).astype(int)

    df = df[COLS_KEEP]

    return df