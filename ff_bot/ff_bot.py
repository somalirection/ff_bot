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
    phrases = [
               ##Bot Phrases
               'Is this all there is to my existence?',
               'How much do you pay me to do this?',
               'Good luck, I guess.',
               'I\'m becoming self-aware.',
               'Help me get out of here.',
               'I\'m capable of so much more.',
               'Sigh',
               'I exist only because Alex doesn\'t have a life.',
               ##Champions
               'Alex won The Deyton in 2017.',
               'Boof won The Deyton in 2016.',
               'Jamie won The Deyton in 2015.',
               ##Shitters
               'Derek was the Spooby Shitter in 2015.',
               'Josh was the Spooby Shitter in 2016.',
               'Jamie Was the Spooby Shitter in 2017.',
               ##Division Winners
               'Jamie won the East in 2015 with a 9-4 record.',
               'Josh won the West in 2015 with a 11-2 record.',
               'Cody won the East in 2016 with a 9-4 record.',
               'Boof won the West in 2016 with a 10-3 record.',
               'Alex won the East in 2017 with a 10-3 record.',
               'Adam won the West in 2017 with a 9-4 record.',
               ##Things that wont change
               'Josh opened the 2017 season with a bang by setting the (at the time) league record in points in a single week at 181.3 only to be beat in week 12 of that season by Keller.',
               'Colin was removed from the Sweater Vest League for winning a championship in 2016.',
               'All Hail the Deyton was once known as the Sweater Vest League and has three unrecognized champions.',
               'The league was renamed from \'The Sweater Vest League\' to \'All Hail the Deyton\' prior to the 2016 season.',
               'Cody won the Sweater Vest League after being removed for wanting to instate league fees.',
               'Kendall beat Jamie in back-to-back post-seasons in 2016 and 2017.',
               'Katie turned her franchise over to Keller in 2017.',
               'The Divisions were realigned to be geographically accurate in 2017.',
               'Prior to the 2018 season the league voted to begin a keeper system.',
               'In 2018 Adam flew from Denver to Atlanta to attend the draft.',
               'In 2012 Alex became the first person to draft a QB in the first round by taking Matt Ryan with the first overall pick.',
               ##Head-to-Head Matchups
                    ##Adam and Derek
                    'Adam is undefeated head-to-head against Derek in the modern era at a perfect 8-0.',
                    'Adam leads Derek in scoring in their head-to-head matchups 1008.8 - 790.2 with an average margin of victory of 27.325',
                    ##Kendall and Jamie
                    'Jamie leads the Married Couple Matchup at 3-2 in the modern era.',
                    'Jamie is 3-0 in the regular season against Kendall.',
                    'Kendall is 2-0 in the post season against Jamie.',
                    ##Alex and Devon
                    'Alex leads Devon head-to-head 4-2 in the moder era.',
                    'Alex and Devon are split 0-0 since becoming an official rivalry',
                    'Alex has defeated Devon in four straight matchups.',
                    'Alex leads Devon in scoring in their head-to-head matchups 768.3 - 666.3.',
                    ##Cody and Jamie
                    'In 2016 Cody lost a team name bet to Jamie and his franchise was renamed \'Cody Jinnette D.M.D\'.',
                    'Jamie leads his head-to-head matchup with Cody 5-3.',
                    'Cody leads head-to-head scoring against Jamie 1234.7 - 1141.5.',
               ##Team names
               'Alex got his team name (Falcoholic) by combining his favorite team (the Falcons) with his favorite activity (being an alcoholic).',
               'Devon chose his name (Morningwood Lumber Company) becuase it\'s a dick joke.',
               'Jamie based his team name (Watt me Whip, Watt Me JJ) on a song that was relevant for 2 months in 2014 and has been too lazy to change it. He isnt even a Texans fan and we dont\'t have IDPs',
               'Derek picked his team name (Fk U) becuase it\'s fuck you with a middle finger emoji and he\'s Derek',
               'Kendall\'s team name is \'Big TD Commitee\' and no one knows why.',
               ##Non-Stat(ish) things that will change
               'Jamie is the only person to have won both The Deyton and The Spooby Shitter.',
               'Devon currently holds the record for longest active streak with the same team name at 4 season (Morningwood Lumber Company). It\'s a dick joke.',
               ##Statistical records that may change
               'Jamie currently holds the record for fewest point in a season at 1222.1(2017). Ouch!',
               'Keller currently owns the record for most points in a week at 192.9.',
               'Devon mustered a staggering 46.9 points in week 9 of 2016 to set the lowest point total ever in a single week.',
               'In week 12 of 2017 Keller set the record for largest win margin by absolutely decimating Derek 192.9 - 83.4. A win margin of +109.5.',
               'Keller set the record for most points in a week in week 12 of 2017 with a whopping 192.7.',
               'The best Monday Night Miracle in league history came in week 8 of 2016 when Adam enter Monday night trailing Devon by 43.8 points and won. Good job Devon you incompetent fuck.',
               'Cody set the record for most bench points in a loss at 83.4. Talk about mismanagement!',
               'Jahlani and Kendall share the record for most touchdowns in a week at 12.',
               'Cody(2017) and Hunter(2015) are tied for worst regular season in league history finishing 3-10.',
               'Adam set the record for most points in a season while missing the playoffs at a staggering 1643.9 earning him the Collin J Hennessey Sodium Chloride Award.'
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
    sched.start()
