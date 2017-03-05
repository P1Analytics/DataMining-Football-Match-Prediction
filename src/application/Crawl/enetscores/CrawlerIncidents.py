import json
import logging
import requests

log = logging.getLogger(__name__)


class CrawlerIncidents(object):
    def __init__(self, match, match_attributes, event):
        self.match = match
        self.match_attributes = match_attributes
        self.event = event

        incident_url = "http://json.mx-api.enetscores.com/live_data/actionzones/" + self.event + "/0?_=1486979583821"
        self.json_incident_match = json.loads(requests.get(incident_url).text)
        log.debug("Instantiated, link [" + incident_url + "]")

    def get_incidents(self):
        """
        read the json string reguarding the incidents in a match
        :return:
        """
        # read incidents only after it's finished
        if self.json_incident_match["s"] == "finished":

            # incidents managed
            goal = "<goal>"
            shoton = "<shoton>"
            shotoff = "<shotoff>"
            foulcommit = "<foulcommit>"
            card = "<card>"
            cross = "<cross>"
            corner = "<corner>"
            possession = "<possession>"

            try:
                self.json_incident_match["i"]
            except KeyError:
                log.debug("Event ["+self.event+"] without incidents")
                return

            for incident in self.json_incident_match["i"]:
                if incident["type"] == "goal":
                    goal += elaborate_tag(incident)
                elif incident["type"] == "shoton":
                    shoton += elaborate_tag(incident)
                elif incident["type"] == "shotoff":
                    shotoff += elaborate_tag(incident)
                elif incident["type"] == "foulcommit":
                    foulcommit += elaborate_tag(incident)
                elif incident["type"] == "card":
                    card += elaborate_tag(incident)
                elif incident["type"] == "cross":
                    cross += elaborate_tag(incident)
                elif incident["type"] == "corner":
                    corner += elaborate_tag(incident)
                elif incident["type"] == "special":
                    try:
                        if incident["subtype"] == "possession":
                            possession += elaborate_tag(incident)
                    except KeyError:
                        pass

            goal += "</goal>"
            shoton += "</shoton>"
            shotoff += "</shotoff>"
            foulcommit += "</foulcommit>"
            card += "</card>"
            cross += "</cross>"
            corner += "</corner>"
            possession += "</possession>"

            self.match_attributes["goal"] = goal
            self.match_attributes["shoton"] = shoton
            self.match_attributes["shotoff"] = shotoff
            self.match_attributes["foulcommit"] = foulcommit
            self.match_attributes["card"] = card
            self.match_attributes["cross"] = cross
            self.match_attributes["corner"] = corner
            self.match_attributes["possession"] = possession

        else:
            log.debug("match ["+str(self.event)+"] not finished")


def elaborate_tag(incident):
    return "<value>"+get_string_by_dict(incident)+"</value>"


def get_string_by_dict(dic):
    dict_str = ""
    for k, v in dic.items():
        # open tag
        dict_str += "<" + k + ">"

        if type(v) is dict:
            # content is an element
            dict_str += get_string_by_dict(v)

        elif type(v) is list:
            # content is a list of element
            for elem in v:
                dict_str += "<value>"+str(elem)+"</value>"
        else:
            # content is a value
            dict_str += str(v)

        # close tag
        dict_str += "</" + k + ">"

    return dict_str
