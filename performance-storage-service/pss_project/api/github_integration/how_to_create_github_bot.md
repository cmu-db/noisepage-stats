# How to Create a Github Checker Bot

The main purpose of the Github checks are to integrate CI tasks into the Github flow. For example, the performance guard will prevent merging a PR if the performance of the PR is significantly worse than master. 

## Github Bot flow
1. PR submitted
2. Bot initializes a check in the pending state
3. Jenkins CI successfully finishes
4. Bot updates the check to the complete state with a status

The `BasePRBot` is designed to follow that flow. It isn't too complicated to follow a different flow. You will need to override a couple methods in your subclass.

## Guide
1. Create a Github App. You can either do this yourself and tranfer ownership to Andy later or ask Andy to do this. You can generally follow this guide for help: [Creating a Github App](https://docs.github.com/en/free-pro-team@latest/developers/apps/creating-a-github-app). The key settings you will need to set are: `GitHub App name = <pick a name>`, `Webhook =  active`, `Webhook secret = <pick a secret value>`. When you create this it should give you a private key -- save this for later.
2. Pick the permissions that you will need for your app. The basic case needs `pull-request` to know when PRs are created, updated, or closed. It also needs `status` to know when the CI has completed.
3. Create a class that inherits `BasePRBot.py`. See `PerformanceGuardBot.py` for an example. Next override the `conclusion_title_map` and `conclusion_summary_map` attributes. These maps associate different titles and summary lines based on whether the result of the check is success, neutral, or failure.

You must override three methods:

- `get_conclusion_data(self, payload)`- This method takes in the payload from the Github event and it should return data that is needed to determine whether the check was a success, neutral, or failure. The return value can be of any type.

- `get_conclusion(self, data)`- This function takes in the data that was returned from `get_conclusion_data` and determines the outcome of the check. This function should return either `CONCLUSION_SUCCESS`, `CONCLUSION_NEUTRAL`, or `CONCLUSION_FAILURE`.

- `generate_conclusion_markdown(self, data)`- his function takes in the data that was returned from `get_conclusion_data` and generates a string that will be displayed in the detailed view of the check. The string can use markdown.

4. Next add an instance of your Bot to `pss_project/api/views/git_events.py`. You will need the App ID, which can be found on Github. Then pick two environment variables for the private key and webhook secret. Pick a name for the bot. Instantiate the object and call `run()` like:
```python
    my_bot = MyBot(app_id=1234,private_key=get_environ_value('MY_BOT_PRIVATE_KEY'), webhook_secret=get_environ_value('MY_BOT_WEBHOOK_SECRET'), name='my-bot')
    my_bot.connect_to_repo()
    my_bot.run(request)
```

5. Follow the instructions on [how to create a new secret](https://github.com/cmu-db/noisepage-stats/wiki/Credentials#how-to-create-a-new-secret) to create a Kubernetes secret for the webhook secret and the private key. 
6. Add the configuration to load the secrets into environment variables in `/deployments/kubernetes/performance/performance-storage-service/deployment.yml` and `/deployments/kubernetes/performance/performance-storage-service/deployment.yml`. You want to add something that looks like:
```yaml
            - name: MY_BOT_WEBHOOK_SECRET
              valueFrom:
                secretKeyRef:
                  name: "secrets-{{ env }}"
                  key: my_bot_webhook_secret 
            - name: MY_BOT_PRIVATE_KEY
              valueFrom:
                secretKeyRef:
                  name: "secrets-{{ env }}"
                  key: my_bot_github_private_key
```
7. Now you are ready to deploy the updated code. Don't forget to increment the version numbers. For instructions on deploying follow the guide [here](https://github.com/cmu-db/noisepage-stats/wiki/Performance-storage-service)