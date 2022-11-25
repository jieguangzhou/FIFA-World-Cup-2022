from pydolphinscheduler.tasks import Python, Shell
from pydolphinscheduler.core.process_definition import ProcessDefinition

CONVERT_TAG = "# $PARAM:"


# load script to dolphinscheduler, and convert special param with CONVERT_TAG
def load_script(path):
    with open(path, 'r') as f:
        script_lines = []
        for line in f:
            if CONVERT_TAG not in line:
                script_lines.append(line)
                continue

            base_line, annotation = line.rstrip().split(CONVERT_TAG)
            param_name, param_value = base_line.split("=")
            param_value = param_value.strip()

            annotation = annotation or param_name.strip()
            annotation = "${%s}" % annotation.strip()

            if param_value.startswith('"') and param_value.endswith('"'):
                annotation = "\"" + annotation + "\""

            new_line = param_name + "= " + annotation + "\n"
            script_lines.append("# original: " + line)
            script_lines.append(new_line)

        script = "".join(script_lines)
        return script


with ProcessDefinition(
    name="training",
    param={
        "train_time": 240,
    }
) as pd:

    # dowanload data
    task_download_data = Shell(
        name="download_data", command=load_script("download_data.sh"))

    # prepare training data and teams message data
    task_data_preprocessing = Python(name="prepare_data",
                                     definition=load_script("prepare_data.py"))

    # training model with FLAML
    task_training = Python(name="training",
                           definition=load_script("training.py"))

    # Select the team with high probability of winning and make the prediction
    task_predict_match = Python(name="predict_match",
                                definition=load_script("predict_match.py"),
                                local_params=[
                                    {"prop": "random_seed", "direct": "IN", "type": "VARCHAR", "value": -1}]
                                )

    task_download_data >> task_data_preprocessing >> task_training >> task_predict_match

    pd.submit()


with ProcessDefinition(
    name="predict",
) as pd:

    # Simulate the results of multiple matches
    predict_tasks = []
    for seed in range(1000):
        task_predict = Python(name=f"predict_match_{seed}",
                              definition=load_script("predict_match.py"),
                              local_params=[
                                  {"prop": "random_seed", "direct": "IN", "type": "VARCHAR", "value": seed}]
                              )
        predict_tasks.append(task_predict)

    # Calculate all the results, and output the final result
    task_calc_result = Python(name="calc_result",
                              definition=load_script("calc_result.py"))

    predict_tasks >> task_calc_result

    pd.submit()


with ProcessDefinition(
    name="betting_strategy",
    param={
        "bet_date": "$[yyyy-MM-dd]",
    }
) as pd:

    # get bet odds about today's match
    task_get_odds = Python(name="get_odds",
                           definition=load_script("get_odds.py"))

    # use model to predict today's match
    task_predict_today_match = Python(name="predict_today_match",
                                      definition=load_script("predict_today_match.py"))

    # output the betting strategy
    task_betting_strategy = Python(name="betting_strategy",
                                   definition=load_script("betting_strategy.py"))

    task_get_odds >> task_predict_today_match >> task_betting_strategy

    pd.submit()
