import src.util.SQLLite as SQLLite
import src.util.Cache as Cache
import src.application.Domain.League as League

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
        # TODO can be more than one
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

def read_by_name(name):
    '''

    :param name:
    :return:
    '''

    try:
        return Cache.get_element(name, "COUNTRY_BY_NAME")
    except KeyError:
        pass
    try:
        sqllite_row = SQLLite.get_connection().select("Country", **{"name": name})[0]
    except IndexError:
        return None
    country = Country(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        country.__setattr__(attribute, value)

    Cache.add_element(country.name, country, "COUNTRY_BY_NAME")
    return country

