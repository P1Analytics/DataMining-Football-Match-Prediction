import src.util.Cache as Cache
import src.util.SQLLite as SQLLite
import src.application.Domain.Bet_Event as Bet_Event


class MatchEvent(object):
    def __init__(self, id):
        self.id = id

    def get_all_bet_values(self):
        """
        return all the bet values for this match event
        :return:
        """
        return Bet_Event.read_by_match_event_id_and_event_name(self.id)

    def get_last_bet_values(self, event_name):
        """
        return the last bet_value of the input event name, of this match event
        :param event_name:
        :return:
        """
        bet_events = Bet_Event.read_by_match_event_id_and_event_name(self.id, event_name)
        bet_events = sorted(bet_events, key=lambda bet_event: bet_event.date)
        if len(bet_events) == 0:
            return None
        return bet_events[-1]

    def __str__(self):
        return "MatchEvent <id: "+str(self.id)+", match_id: "+str(self.match_id)+">"


def read_all():
    """
    read all the bet events
    :return:
    """
    match_events = []
    sqllite_rows = SQLLite.get_connection().select("Match_Event")
    for sqllite_row in sqllite_rows:
        match_event = MatchEvent(sqllite_row["id"])
        for attribute, value in sqllite_row.items():
            match_event.__setattr__(attribute, value)
        match_events.append(match_event)

    return match_events


def read_by_match_id(match_id):
    """
    Return the bet event by the match id related
    :param match_id:
    :return:
    """
    try:
        return Cache.get_element(str(match_id), "MATCH_EVENT_BY_MATCH_ID")
    except KeyError:
        pass

    try:
        sqllite_row = SQLLite.get_connection().select("Match_Event", **{"match_id": str(match_id)})[0]
    except IndexError:
        return None
    match_event = MatchEvent(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        match_event.__setattr__(attribute, value)

    Cache.add_element(str(match_event.match_id), match_event, "MATCH_EVENT_BY_MATCH_ID")
    return match_event


def write_new_match_event(match_id):
    """
    Write a new bet event in the DB
    :param match_id:
    :return:
    """
    SQLLite.get_connection().insert("Match_Event", {'match_id': match_id})
    return read_by_match_id(match_id)
