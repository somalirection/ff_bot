import requests
import json
import os
import random
import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from espnff import League


class GroupMeException(Exception):
    pass

class GroupMeBot(object):
    #Creates GroupMe Bot to send messages
    def __init__(self, bot_id):
        self.bot_id = bot_id

    def __repr__(self):
        return "GroupMeBot(%s)" % self.bot_id

    def send_message(self, text):
        #Sends a message to the chatroom
        template = {
                    "bot_id": self.bot_id,
                    "text": text,
                    "attachments": []
                    }

        headers = {'content-type': 'application/json'}
        r = requests.post("https://api.groupme.com/v3/bots/post",
                          data=json.dumps(template), headers=headers)
        if r.status_code != 202:
            raise GroupMeException('Invalid BOT_ID')

        return r

def pranks_week(league):
        count = 1
        first_team = next(iter(league.teams or []), None)
        #Iterate through the first team's scores until you reach a week with 0 points scored
        for o in first_team.scores:
            if o == 0:
                if count != 1:
                     count = count - 1
                break
            else:
                count = count + 1

        return count

def random_phrase():
    phrases = ['Is this all there is to my existence?',
               'How much do you pay me to do this?', 'Good luck, I guess',
               'I\'m becoming self-aware', 'Help me get out of here',
               'I\'m capable of so much more', 'Sigh',
               'Josh opened the 2017 season with a bang by setting the (at the time) league record in points in a single week at 181.3 only to be beat in week 12 of that season by Keller',
               'Keller currently owns the record for most points in a week at 192.9',
               'Devon mustered a staggering 46.9 points in week 9 of 2016 to set the lowest point total ever in a single week',
               'Alex won The Deyton in 2017',
               'Boof won The Deyton in 2016',
               'Jamie won The Deyton in 2015',
               'In week 12 of 2017 Keller set the record for largest win margin by absolutely decimating Derek 192.9-83.4. A win margin of +109.5',
               'Derek was the Spooby Shitter in 2015',
               'Josh was the Spooby Shitter in 2016',
               'Jamie Was the Spooby Shitter in 2017',
               'Jamie is the only person to have won both The Deyton and The Spooby Shitter',
               'Keller set the record for most points in a week in week 12 of 2017 with a whopping 192.7',
               'The best Monday Night Miracle in league history came in week 8 of 2016 when Adam enter Monday night trailing Devon by 43.8 points and won. Good job Devon you incompetent fuck.',
               'Cody set the record for most bench points in a loss at 83.4',
               'Jahlani and Kendall share the record for most touchdowns in a week at 12.',
               'Jamie leads the Married Couple Matchup at 3-2.',
               'Cody had the worst regular season in league history in 2017 finishing 3-10.',
               'Colin was removed from the Sweater Vest League for winning a championship',
               'All Hail the Deyton was once known as the Sweater Vest League and has three unrecognized champions',
               'Cody won the Sweater Vest League after being removed for wanting to instate league fees',
               'Adam set the record for most points in a season while missing the playoffs at a staggering 1643.9 earning him the Collin J Hennessey Sodium Chloride Award'
               'Adam is undefeated head-to-head against Derek at a perfect 8-0'
               'Kendall has beaten Jamie in back-to-back post-seasons in 2016 and 2017'
               ]
    text = [random.choice(phrases)]
    return '\n'.join(text)

def player_name():
    names = ['Adam','Alex','Boof','Cody','Derek','Devon','Jamie','Josh','Keller','Kendall']
    text = [random.choice(names)]
    return '\n'.join(text)

def get_scoreboard_short(league, final=False):
    #Gets current week's scoreboard
    if not final:
        matchups = league.scoreboard()
    else:
        matchups = league.scoreboard(week=pranks_week(league))
    score = ['%s %.2f - %.2f %s' % (i.home_team.team_abbrev, i.home_score,
             i.away_score, i.away_team.team_abbrev) for i in matchups
             if i.away_team]
    text = ['Score Update'] + score
    return '\n'.join(text)

def get_scoreboard(league):
    #Gets current week's scoreboard
    matchups = league.scoreboard()
    score = ['%s %.2f - %.2f %s' % (i.home_team.team_name, i.home_score,
             i.away_score, i.away_team.team_name) for i in matchups
             if i.away_team]
    text = ['Score Update'] + score
    return '\n'.join(text)

def get_matchups(league):
    #Gets current week's Matchups
    matchups = league.scoreboard()

    score = ['%s(%s-%s) vs %s(%s-%s)' % (i.home_team.team_name, i.home_team.wins, i.home_team.losses,
             i.away_team.team_name, i.away_team.wins, i.away_team.losses) for i in matchups
             if i.away_team]
    text = ['This Week\'s Matchups'] + score
    return '\n'.join(text)

def get_close_scores(league):
    #Gets current closest scores (15.999 points or closer)
    matchups = league.scoreboard()
    score = []

    for i in matchups:
        if i.away_team:
            diffScore = i.away_score - i.home_score
            if -16 < diffScore < 16:
                score += ['%s %.2f - %.2f %s' % (i.home_team.team_abbrev, i.home_score,
                        i.away_score, i.away_team.team_abbrev)]
    if not score:
        score = ['None']
    text = ['Close Scores'] + score
    return '\n'.join(text)

def get_power_rankings(league):
    #Gets current week's power rankings
    #Using 2 step dominance, as well as a combination of points scored and margin of victory.
    #It's weighted 80/15/5 respectively
    pranks = league.power_rankings(week=pranks_week(league))

    score = ['%s - %s' % (i[0], i[1].team_name) for i in pranks
             if i]
    text = ['This Week\'s Power Rankings'] + score
    return '\n'.join(text)

def get_trophies(league):
    #Gets trophies for highest score, lowest score, closest score, and biggest win
    matchups = league.scoreboard(week=pranks_week(league))
    low_score = 9999
    low_team_name = ''
    high_score = -1
    high_team_name = ''
    closest_score = 9999
    close_winner = ''
    close_loser = ''
    biggest_blowout = -1
    blown_out_team_name = ''
    ownerer_team_name = ''

    for i in matchups:
        if i.home_score > high_score:
            high_score = i.home_score
            high_team_name = i.home_team.team_name
        if i.home_score < low_score:
            low_score = i.home_score
            low_team_name = i.home_team.team_name
        if i.away_score > high_score:
            high_score = i.away_score
            high_team_name = i.away_team.team_name
        if i.away_score < low_score:
            low_score = i.away_score
            low_team_name = i.away_team.team_name
        if abs(i.away_score - i.home_score) < closest_score:
            closest_score = abs(i.away_score - i.home_score)
            if i.away_score - i.home_score < 0:
                close_winner = i.home_team.team_name
                close_loser = i.away_team.team_name
            else:
                close_winner = i.away_team.team_name
                close_loser = i.home_team.team_name
        if abs(i.away_score - i.home_score) > biggest_blowout:
            biggest_blowout = abs(i.away_score - i.home_score)
            if i.away_score - i.home_score < 0:
                ownerer_team_name = i.home_team.team_name
                blown_out_team_name = i.away_team.team_name
            else:
                ownerer_team_name = i.away_team.team_name
                blown_out_team_name = i.home_team.team_name

    low_score_str = ['Low score: %s with %.2f points' % (low_team_name, low_score)]
    high_score_str = ['High score: %s with %.2f points' % (high_team_name, high_score)]
    close_score_str = ['%s barely beat %s by a margin of %.2f' % (close_winner, close_loser, closest_score)]
    blowout_str = ['%s blown out by %s by a margin of %.2f' % (blown_out_team_name, ownerer_team_name, biggest_blowout)]

    text = ['Trophies of the week:'] + low_score_str + high_score_str + close_score_str + blowout_str
    return '\n'.join(text)

def bot_main(function):
    bot_id = os.environ["BOT_ID"]
    league_id = os.environ["LEAGUE_ID"]

    try:
        year = os.environ["LEAGUE_YEAR"]
    except KeyError:
        year=2018

    bot = GroupMeBot(bot_id)
    league = League(league_id, year)

    test = False
    if test:
        print(get_matchups(league))
        print(get_scoreboard(league))
        print(get_scoreboard_short(league))
        print(get_close_scores(league))
        print(get_power_rankings(league))
        print(get_trophies(league))
        function="get_final"
        #bot.send_message(get_trophies(league))

    if function=="get_matchups":
        text = get_matchups(league)
        bot.send_message(text)
    elif function=="get_scoreboard":
        text = get_scoreboard(league)
        bot.send_message(text)
    elif function=="get_scoreboard_short":
        text = get_scoreboard_short(league)
        bot.send_message(text)
    elif function=="get_close_scores":
        text = get_close_scores(league)
        bot.send_message(text)
    elif function=="get_power_rankings":
        text = get_power_rankings(league)
        bot.send_message(text)
    elif function=="get_trophies":
        text = get_trophies(league)
        bot.send_message(text)
    elif function=="get_final":
        text = "Final " + get_scoreboard_short(league, True)
        text = text + "\n\n" + get_trophies(league)
        if test:
            print(text)
        else:
            bot.send_message(text)
    elif function=="get_random_phrase":
        text = random_phrase()
        bot.send_message(text)
    elif function=="predict_high":
        text = "I predict this weeks highest scorer will be..."
        bot.send_message(text)
        time.sleep(10)
        text = player_name()
        bot.send_message(text)
    elif function=="predict_low":
        text = "I predict this weeks lowest scorer will be..."
        bot.send_message(text)
        time.sleep(10)
        text = player_name()
        bot.send_message(text)
    elif function=="predict_td":
        text = "I predict the most touchdowns this week will be scored by..."
        bot.send_message(text)
        time.sleep(10)
        text = player_name()
        bot.send_message(text)
    elif function=="predict_champ":
        text = "I predict this years champion will be..."
        bot.send_message(text)
        time.sleep(10)
        text = player_name()
        bot.send_message(text)
    elif function=="predict_spoob":
        text = "I predict this years Spooby will be..."
        bot.send_message(text)
        time.sleep(10)
        text = player_name()
        bot.send_message(text)
    elif function=="init":
        try:
            text = os.environ["INIT_MSG"]
            bot.send_message(text)
        except KeyError:
            #do nothing here, empty init message
            pass
    else:
        text = "Something happened. HALP"
        bot.send_message(text)


if __name__ == '__main__':
    try:
        ff_start_date = os.environ["SEASON_START_DATE"]
    except KeyError:
        ff_start_date='2018-09-05'
    try:
        fact_start_date = os.environ["FACTS_START_DATE"]
    except KeyError:
        fact_start_date='2018-08-23'
    try:
        ff_end_date = os.environ["END_DATE"]
    except KeyError:
        ff_end_date='2018-12-30'

    try:
        myTimezone = os.environ["TIMEZONE"]
    except KeyError:
        myTimezone='America/New_York'

    bot_main("init")
    sched = BlockingScheduler(job_defaults={'misfire_grace_time': 15*60})

    #power rankings:                     tuesday evening at 6:30pm.
    #matchups:                           thursday evening at 7:30pm.
    #close scores (within 15.99 points): monday evening at 6:30pm.
    #trophies:                           tuesday morning at 7:30am.
    #score update:                       friday, monday, and tuesday morning at 7:30am.
    #score update:                       sunday at 1pm, 4pm, 8pm.

    sched.add_job(bot_main, 'cron', ['get_power_rankings'], id='power_rankings',
        day_of_week='tue', hour=18, minute=30, start_date=ff_start_date, end_date=ff_end_date,
        timezone=myTimezone, replace_existing=True)
    sched.add_job(bot_main, 'cron', ['get_matchups'], id='matchups',
        day_of_week='thu', hour=19, minute=30, start_date=ff_start_date, end_date=ff_end_date,
        timezone=myTimezone, replace_existing=True)
    sched.add_job(bot_main, 'cron', ['get_close_scores'], id='close_scores',
        day_of_week='mon', hour=18, minute=30, start_date=ff_start_date, end_date=ff_end_date,
        timezone=myTimezone, replace_existing=True)
    sched.add_job(bot_main, 'cron', ['get_final'], id='final',
        day_of_week='tue', hour=7, minute=30, start_date=ff_start_date, end_date=ff_end_date,
        timezone=myTimezone, replace_existing=True)
    sched.add_job(bot_main, 'cron', ['get_scoreboard_short'], id='scoreboard1',
        day_of_week='fri,mon', hour=7, minute=30, start_date=ff_start_date, end_date=ff_end_date,
        timezone=myTimezone, replace_existing=True)
    sched.add_job(bot_main, 'cron', ['get_scoreboard_short'], id='scoreboard2',
        day_of_week='sun', hour='16,20', start_date=ff_start_date, end_date=ff_end_date,
        timezone=myTimezone, replace_existing=True)
    ###Fun Facts
    sched.add_job(bot_main, 'cron', ['get_random_phrase'], id='random_phrase',
        day_of_week='sun,mon,tue,wed,thu,fri,sat', hour='9,15,21', minute='20', start_date=fact_start_date, end_date=ff_end_date,
        timezone=myTimezone, replace_existing=True)
    ###Predictions
    sched.add_job(bot_main, 'cron', ['predict_td'], id='predict_td',
        day_of_week='Thu', hour=8, minute=10, start_date=ff_start_date, end_date=ff_end_date,
        timezone=myTimezone, replace_existing=True)
    sched.add_job(bot_main, 'cron', ['predict_low'], id='predict_low',
        day_of_week='thu', hour=14, minute=25, start_date=ff_start_date, end_date=ff_end_date,
        timezone=myTimezone, replace_existing=True)
    sched.add_job(bot_main, 'cron', ['predict_high'], id='predict_high',
        day_of_week='thu', hour=18, minute=40, start_date=ff_start_date, end_date=ff_end_date,
        timezone=myTimezone, replace_existing=True)
    sched.add_job(bot_main, 'cron', ['predict_champ'], id='predict_champ',
        day_of_week='thu', hour=17, minute=30, start_date=ff_start_date, end_date=(ff_start_date + datetime.timedelta(days=1)),
        timezone=myTimezone, replace_existing=True)
    sched.add_job(bot_main, 'cron', ['predict_spoob'], id='predict_spoob',
        day_of_week='thu', hour=17, minute=30, start_date=ff_start_date, end_date=(ff_start_date + datetime.timedelta(days=1)),
        timezone=myTimezone, replace_existing=True)

    sched.start()
