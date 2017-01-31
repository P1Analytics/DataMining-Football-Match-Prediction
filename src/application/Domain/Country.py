import src.util.SQLLite as SQLLite
from src.application.Domain import League

class Country(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "Country <id: "+str(self.id)+", name: "+self.name+">"

    def get_league(self):
        '''
        Return the league of this country
        :return:
        '''
        return League.read_by_country(self.id)


def read_all():
    '''
    Reads all tuple in the database
    :return:
    '''
    countries = []
    for c in SQLLite.read_all("Country"):
        country = Country(c["id"])
        for attribute, value in c.items():
            country.__setattr__(attribute, value)
        countries.append(country)
    return countries

