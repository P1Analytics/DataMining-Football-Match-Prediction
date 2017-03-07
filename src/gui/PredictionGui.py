import logging
import src.util.GuiUtil as GuiUtil

import src.application.Domain.Match as Match
import src.application.MachineLearning.MachineLearningAlgorithm as mla
import src.application.MachineLearning.MachineLearningInput as mli

log = logging.getLogger(__name__)

ml_alg_method = "SVM"
ml_alg_framework = "my_poisson"
ml_train_input_id = 5
ml_train_input_representation = 1
ml_train_stages_to_train = 10


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
    if check_setting_current_predictor() == -1:
        return
    date = GuiUtil.input_date_or_day_passed()
    matches = Match.read_by_match_date(date)
    matches = sorted(matches, key=lambda match: match.date)

    if len(matches) == 0:
        GuiUtil.print_att("No match found in date", date)
    else:
        GuiUtil.print_ans("Prediction by date", date)
        prediction_by_league = dict()
        pi = 1
        for match in matches:
            if not match.is_finished():
                league = match.get_league()
                season = match.season
                stage = match.stage
                try:
                    prediction_by_league[league.id]
                except KeyError:
                    predicted_labels, probability_events, matches_to_predict_id = predict(league, season, stage)
                    prediction_by_league[league.id] = dict()
                    for id, prediction, probability in zip(matches_to_predict_id, predicted_labels, probability_events):
                        prediction_by_league[league.id][id] = [prediction, probability]
                try:
                    prediction, probability = prediction_by_league[league.id][match.id]
                    prediction_str = get_printable_prediction(match, prediction, probability)
                    GuiUtil.print_indent_answer(pi, prediction_str, True)
                    pi += 1
                except KeyError:
                    log.warning("Not possible to predict ["+match.id, match.get_home_team().team_long_name, "vs", match.get_away_team().team_long_name+"]")

        if pi == 1:
            GuiUtil.print_ans("Matches to predict", "NOT FOUND")

def get_printable_prediction(match, prediction, probability):
    out_prediction = ""
    out_prediction += match.get_home_team().team_long_name+" vs "+ match.get_away_team().team_long_name
    out_prediction += "\n"+str(prediction)+"\t("+str(round(probability*100,2))+"%)"

    return out_prediction


def predict(league, season, stage):
    global ml_alg_method
    global ml_alg_framework
    global ml_train_input_id
    global ml_train_input_representation
    global ml_train_stages_to_train

    matches, labels, matches_id, matches_to_predict, matches_to_predict_id, labels_to_predict = \
        mli.get_input_to_train(ml_train_input_id,
                               league,
                               ml_train_input_representation,
                               stage,
                               ml_train_stages_to_train,
                               season)

    ml_alg = mla.get_machine_learning_algorithm(ml_alg_framework,
                                                ml_alg_method,
                                                matches,
                                                labels,
                                                matches_id,
                                                train_percentage=1,
                                                )

    ml_alg.train()
    predicted_labels, probability_events = ml_alg.predict(matches_to_predict)
    return predicted_labels, probability_events, matches_to_predict_id

if __name__ == "__main__":
    set_predictor()
    predict_by_date()