import logging
import src.util.GuiUtil as GuiUtil
import src.util.util as util

import src.application.Domain.Match as Match
import src.application.Exception.MLException as MLException
import src.application.MachineLearning.MachineLearningAlgorithm as mla
import src.application.MachineLearning.MachineLearningInput as mli
import src.application.MachineLearning.prediction_accuracy.Predictor as Predictor

log = logging.getLogger(__name__)

ml_alg_framework = "my_poisson"
ml_alg_method = "SVM"
ml_train_input_id = 5
ml_train_input_representation = 1
ml_train_stages_to_train = 19


def run():
    GuiUtil.print_head("Predictions")
    menu = {1: "Set Current Predictor",
            2: "Show Current Predictor",
            3: "Check setting current predictor",
            4: "Predict matches by date" }
    GuiUtil.print_menu("Predictions menu:", menu, add_go_back=True)

    while True:
        try:
            user_input = input("\nSelect an item: ")
            user_input = int(user_input)

            if user_input == 1:
                set_predictor()

            elif user_input == 2:
                GuiUtil.print_info("Show", "Current Predictor")
                show_current_predictor()

            elif user_input == 3:
                GuiUtil.print_info("Check Setting", "Current Predictor")
                if check_setting_current_predictor() == 0:
                    GuiUtil.print_ans("Predictor status", "READY")

            elif user_input == 4:
                GuiUtil.print_info("Predict matches by", "date")
                try:
                    predict_by_date()
                except Exception as e:
                    print(e)
                    GuiUtil.print_att("Error during prediction", "controlling your current predictor..")
                    if check_setting_current_predictor() == 0:
                        GuiUtil.print_att("Predictor OK", "contact administrator")

            else:
                raise ValueError

            GuiUtil.print_line_separator()
            GuiUtil.print_menu("Predictions Menu:", menu, add_go_back=True)

        except ValueError:
            if user_input == 'gb':
                return
            print("Insert a valid input!!!")


def set_predictor():
    global ml_alg_method
    global ml_alg_framework
    global ml_train_input_id
    global ml_train_input_representation
    global ml_train_stages_to_train

    show_current_predictor()
    GuiUtil.print_info("Setting", "predictor")

    GuiUtil.show_list_answer(mla.get_frameworks(), label="List", label_value="Frameworks (String)")
    GuiUtil.show_list_answer(mla.get_methods(), label="List", label_value="Algorithms (String)")
    GuiUtil.print_ans("List", "Machine learning input (Id)")
    for input_id, input_desc in mli.get_input_ids().items():
        repr = mli.get_representations(input_id)
        GuiUtil.print_indent_answer(input_id, input_desc+"\nRepresentations: "+str(repr), True)

    GuiUtil.print_inst("list of parameter", "framework(str) algorithm(str) input(int) representation(int) training(int)")
    GuiUtil.print_inst("Use . for", "default")

    while True:
        user_input = input("\nType your representation: ")
        try:
            for i in range(5):
                value = user_input.split()[i]
                if value == '.':
                    continue
                elif i == 0:
                    ml_alg_framework = value
                elif i == 1:
                    ml_alg_method = value
                elif i == 2:
                    ml_train_input_id = int(value)
                elif i == 3:
                    ml_train_input_representation = int(value)
                elif i == 4:
                    ml_train_stages_to_train = int(value)
            break
        except IndexError:
            GuiUtil.print_att("Some input is missing", "5 parameter are needed")
            GuiUtil.print_inst("list of parameter", "framework algorithm input representation training")
            GuiUtil.print_inst("Use . for", "default")
        except ValueError:
            GuiUtil.print_att("Some input should be int", "found string")
            GuiUtil.print_inst("list of parameter", "framework algorithm input representation training")
            GuiUtil.print_inst("Use . for", "default")


def show_current_predictor():
    global ml_alg_method
    global ml_alg_framework
    global ml_train_input_id
    global ml_train_input_representation
    global ml_train_stages_to_train
    GuiUtil.print_info("Machine Learning Framework", ml_alg_framework)
    GuiUtil.print_info("Machine Learning Algorithm", ml_alg_method)
    GuiUtil.print_info("Machine Learning Input", ml_train_input_id)
    GuiUtil.print_info("Machine Learning Input representation", ml_train_input_representation)
    GuiUtil.print_info("Machine Learning Training Size", ml_train_stages_to_train)


def check_setting_current_predictor():
    global ml_alg_framework
    global ml_alg_method
    global ml_train_input_id
    global ml_train_input_representation
    global ml_train_stages_to_train

    # check framework
    if ml_alg_framework not in mla.get_frameworks():
        GuiUtil.print_att("Framework NOT FOUND", ml_alg_framework)
        GuiUtil.show_list_answer(mla.get_frameworks(), label="List", label_value="Valid Frameworks")
        return -1

    # check algorithm
    methods_by_framework = mla.get_methods_by_framework(ml_alg_framework)
    if len(methods_by_framework) > 0 and ml_alg_method not in methods_by_framework:
        GuiUtil.print_att("Methods for framework NOT FOUND", ml_alg_method)
        GuiUtil.show_list_answer(methods_by_framework, label="List", label_value="Valid Methods for "+ml_alg_framework)
        return -1

    # ml input
    ml_inputs_by_framework = mla.get_inputs_by_framework(ml_alg_framework)
    if ml_train_input_id not in ml_inputs_by_framework:
        GuiUtil.print_att("Inputs for framework NOT FOUND", ml_train_input_id)
        GuiUtil.show_list_answer(ml_inputs_by_framework, label="List", label_value="Valid Inputs for " + ml_alg_framework)
        return -1

    # ml input representations
    ml_train_input_representations = mla.get_inputs_by_input(ml_train_input_id)
    if len(ml_train_input_representations) > 0 and ml_train_input_representation not in ml_train_input_representations:
        GuiUtil.print_att("Representation for Input NOT FOUND", ml_train_input_id)
        GuiUtil.show_list_answer(ml_train_input_representations, label="List",
                                 label_value="Valid Inputs for input " + ml_train_input_id)
        return -1

    return 0


def predict_by_date():
    global ml_alg_method
    global ml_alg_framework
    global ml_train_input_id
    global ml_train_input_representation
    global ml_train_stages_to_train

    if check_setting_current_predictor() == -1:
        return
    date = GuiUtil.input_date_or_day_passed()
    matches = Match.read_by_match_date(date)
    matches = sorted(matches, key=lambda match: match.date)

    if len(matches) == 0:
        GuiUtil.print_att("No match found in date", date)
    else:
        GuiUtil.print_ans("Prediction by date", date)
        pi = 1
        for match in matches:
            if not match.is_finished():
                league = match.get_league()
                season = match.season
                stage = match.stage

                predictor = Predictor.get_predictor(ml_alg_framework,
                       ml_alg_method,
                       ml_train_input_id,
                       ml_train_input_representation,
                       ml_train_stages_to_train)
                prediction_by_league = predictor.predict(league, season, stage)

                try:
                    prediction, probability = prediction_by_league[match.id]
                    prediction_str = get_printable_prediction(match, prediction, probability)
                    GuiUtil.print_indent_answer(pi, prediction_str, True)
                    pi += 1

                except KeyError:
                    log.warning("Not possible to predict [" + str(match.id) + ": "
                                + match.get_home_team().team_long_name + "vs"
                                + match.get_away_team().team_long_name + "]")

        if pi == 1:
            GuiUtil.print_ans("Matches to predict", "NOT FOUND")


def get_printable_prediction(match, prediction, probability):
    out_prediction = ""
    out_prediction += match.get_home_team().team_long_name+" vs " + match.get_away_team().team_long_name
    out_prediction += "\n"+str(prediction)+"\t("+str(round(probability*100, 2))+"%):"

    match_event = match.get_match_event()
    if util.is_None(match_event):
        return out_prediction

    bet_event = match_event.get_last_bet_values(event_name="Match Result")["Match Result"]
    if not util.is_None(bet_event):
        bookmaker_bet_odd = bet_event.get_bet_odds_by_bet(prediction)
        if not util.is_None(bookmaker_bet_odd):
            out_prediction += "\t"+str(bookmaker_bet_odd)+"\t("+str(round(100/bookmaker_bet_odd, 2))+"%)"
            out_prediction += "\nBet > "+str(probability > 1/bookmaker_bet_odd)
    out_prediction += ""

    return out_prediction
