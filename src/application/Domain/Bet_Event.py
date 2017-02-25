import json

import src.util.SQLLite as SQLLite
import src.util.util as util

class BetEvent(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "BetEvent <"+str(self.match_event_id)+", "+self.event_name+", "+self.date+", "+self.bet_value+">"


def read_by_match_event_id_and_event_name(match_event_id, event_name=None):
    '''
    Return the list of bet_event of the input match
    :param match_event_id:
    :param event_name:
    :return:
    '''

    filter = {}
    filter["match_event_id"] = str(match_event_id)

    if not util.is_None(event_name):
        filter["event_name"] =  event_name

    bet_events = []
    for sqllite_row in SQLLite.get_connection().select("Bet_Event", **filter):
        be = BetEvent(sqllite_row["id"])
        for attribute, value in sqllite_row.items():
            be.__setattr__(attribute, value)
        bet_events.append(be)

    return bet_events


def write_new_bet_event(match_event_id, event_name, bet_values):
    '''
    Insert a new bet event in the DB
    :param match_event_id:
    :param event_name:
    :param bet_values:
    :return:
    '''
    bet_values_str = json.dumps(bet_values)
    # decode
    #j = json.loads(l)
    #print(j, type(j))


    SQLLite.get_connection().insert("Bet_Event", {'match_event_id':match_event_id,
                                                  'event_name':event_name,
                                                  'bet_value':bet_values_str,
                                                  'date':util.get_today_date(with_hours=True)})
