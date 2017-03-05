import src.util.GuiUtil as GuiUtil

import src.application.Domain.Match as Match
import src.application.MachineLearning.MachineLearningAlgorithm as mla
import src.application.MachineLearning.MachineLearningInput as mli


ml_alg_method = "SVM"
ml_alg_framework = "my_poisson"
ml_train_input_id = 5
ml_train_input_representation = 1
ml_train_stages_to_train = 10


def run():
    GuiUtil.print_head("Predictions")
    menu = {1: "Set Current Predictor", 2: "Show Current Predictor", 3: "Predict matches by date"}
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
                GuiUtil.print_info("Predict matches by", "date")
                predict_by_date()

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

    GuiUtil.show_list_answer(mla.get_frameworks(), label="List", label_value="Frameworks")
    GuiUtil.show_list_answer(mla.get_methods(), label="List", label_value="Algorithms")
    GuiUtil.print_ans("List", "Machine learning input")
    for input_id, input_desc in mli.get_input_ids().items():
        repr = mli.get_representations(input_id)
        GuiUtil.print_indent_answer(input_id, input_desc+"\nRepresentations: "+str(repr), True)

    GuiUtil.print_inst("list of parameter", "framework algorithm input representation training")
    GuiUtil.print_inst("Use . for", "default")

    user_input = input("\nType your representation: ")
    for i, value in enumerate(user_input.split()):
        if value == '.':
            continue
        elif i == 0:
            ml_alg_framework = value
        elif i == 1:
            ml_alg_method = value
        elif i == 2:
            ml_train_input_id = value
        elif i == 3:
            ml_train_input_representation = value
        elif i == 4:
            ml_train_stages_to_train = value


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


def predict_by_date():
    date = GuiUtil.input_date_or_day_passed()
    matches = Match.read_by_match_date(date)
    matches = sorted(matches, key=lambda match: match.date)

    if len(matches) == 0:
        GuiUtil.print_att("No match found in date", date)
    else:
        prediction_by_league = dict()
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
                    print(match.get_home_team().team_long_name,"vs",match.get_away_team().team_long_name)
                    print("\t",prediction, probability)
                except KeyError:
                    print("Not found ")
                    print(match.id, match.get_home_team().team_long_name, "vs", match.get_away_team().team_long_name)
                    print(prediction_by_league[league.id])


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

if __name__ == "__main__": predict_by_date()