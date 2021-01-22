# How to Create a Github Checker Bot

The main purpose of the Github checks are to integrate CI tasks into the Github flow. For example, the performance guard will prevent merging a PR if the performance of the PR is significantly worse than master. 

## Github Bot flow
1. PR opened/updated/reopened
2. Bot initializes a check in the pending state
3. Jenkins CI successfully finishes
4. Bot updates the check to the complete state with a status(succuess/neutral/failed)

The `BasePRBot` is designed to follow that flow. It isn't too complicated to follow a different flow. You will need to override a couple methods in your subclass.

## Guide
1. Create a class that inherits `BasePRBot.py`. See `PerformanceGuardBot.py` for an example. Next override the `conclusion_title_map` and `conclusion_summary_map` attributes. These maps associate different titles and summary lines based on whether the result of the check is success, neutral, or failure.

You must override three methods:

- `get_conclusion_data(self, payload)`- This method takes in the payload from the Github event and it should return data that is needed to determine whether the check was a success, neutral, or failure. The return value can be of any type.

- `get_conclusion(self, data)`- This function takes in the data that was returned from `get_conclusion_data` and determines the outcome of the check. This function should return either `CONCLUSION_SUCCESS`, `CONCLUSION_NEUTRAL`, or `CONCLUSION_FAILURE`.

- `generate_conclusion_markdown(self, data)`- This function takes in the data that was returned from `get_conclusion_data` and generates a string that will be displayed in the detailed view of the check. The string can use markdown.

2. Next add an instance of your Bot to `pss_project/api/views/git_events.py`. Pass the `repo_client` into the bot. The `repo_client` allows the PR bot to make API calls to the NoisePage repository. Pick a name for the bot. Instantiate the object and call `run()` like:
```python
    my_bot = MyBot(repo_client=repo_client, name='my-bot')
    my_bot.run(event, payload)
```
3. Now you are ready to deploy the updated code. Don't forget to increment the version numbers. For instructions on deploying follow the guide [here](https://github.com/cmu-db/noisepage-stats/wiki/Performance-storage-service).
