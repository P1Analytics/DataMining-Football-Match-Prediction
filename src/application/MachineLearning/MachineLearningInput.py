import logging
import numpy as np
import src.application.Domain.League as League
import src.application.Domain.Team as Team


import src.application.MachineLearning.input_train.team_form as team_form_input
import src.application.MachineLearning.input_train.team_home_away_form as team_home_away_form_input
import src.application.MachineLearning.input_train.match_statistics as match_statistics_input

log = logging.getLogger(__name__)


def get_input_to_train(id, domain, representation, stage, stages_to_train, season):
    if id == 1:
        log.debug("team form")
        return team_form_input.team_form(domain,
                                         representation,
                                         stage,
                                         stages_to_train=stages_to_train,
                                         season=season)
    if id == 2:
        log.debug("team home away form")
        return team_home_away_form_input.team_home_away_form(domain,
                                                             representation,
                                                             stage,
                                                             stages_to_train=stages_to_train,
                                                             season=season)

    if id == 3:
        log.debug("match statistics")
        return match_statistics_input.match_statistics(domain,
                                                       representation,
                                                       stage,
                                                       stages_to_train=stages_to_train,
                                                       season=season)

    else:
        print("The only possible choices are:")
        print("\t1: team_form")
        print("\t2: team_home_away_form")
        print("\t3: match_statistics")
        raise ValueError
