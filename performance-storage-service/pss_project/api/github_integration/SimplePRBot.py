from pss_project.api.github_integration.BasePRBot import (BasePRBot, CONCLUSION_SUCCESS, CONCLUSION_NEUTRAL,
                                                          CONCLUSION_FAILURE)

class SimplePRBot(BasePRBot):
    @property
    def conclusion_title_map(self):
        return {
            CONCLUSION_SUCCESS: "Dan's Testing something",
        }

    @property
    def conclusion_summary_map(self):
        return {
            CONCLUSION_SUCCESS: "Nice job! This works the way I think"
        }

    def get_conclusion_data(self, payload):
        return None

    def get_conclusion(self, data):
        return CONCLUSION_SUCCESS

    def generate_conclusion_markdown(self,data):
        return "Wow, it is easier to create a PR check than I thought!"