import src.util.SQLLite as SQLLite
import src.util.Cache as Cache
import src.application.Domain.League as League

class Country(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "Country <id: "+str(self.id)+", name: "+self.name+">"

    def get_leagues(self):
        '''
        Return the league of this country
        :return:
        '''
        return League.read_by_country(self.id)


def read_all(column_filter='*'):
    '''
    Reads all tuple in the database
    :return:
    '''
    countries = []
    for c in SQLLite.read_all("Country", column_filter):
        country = Country(c["id"])
        for attribute, value in c.items():
            country.__setattr__(attribute, value)
        countries.append(country)
    return countries

def read_by_name(name, like=False):
    '''

    :param name:
    :return:
    '''
    if like:
        sqllite_rows = SQLLite.get_connection().select_like("Country", **{"name": name})
    else:
        sqllite_rows = SQLLite.get_connection().select("Country", **{"name": name})

    countries = []
    for c in sqllite_rows:
        country = Country(c["id"])
        for attribute, value in c.items():
            country.__setattr__(attribute, value)
        countries.append(country)

    return countries

