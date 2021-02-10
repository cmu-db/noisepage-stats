from tabulate import tabulate
import logging

from pss_project.api.github_integration.BasePRBot import (BasePRBot, CONCLUSION_SUCCESS, CONCLUSION_NEUTRAL,
                                                          CONCLUSION_FAILURE)
from pss_project.api.models.database.OLTPBenchResult import OLTPBenchResult
from pss_project.api.constants import MASTER_BRANCH_NAME

logger = logging.getLogger()


class PerformanceGuardBot(BasePRBot):
    """ This PR Bot is initialized in a queued stated. It waits for the CI pipeline to
    complete. When the CI pipeline completes it fetches the latest performance results
    for the commit. Then it compares the performance results with the most recent
    nightly performance results. The results are organized into a markdown table. The
    check is completed based on the results of the performance comparison. """
    # https://github.com/settings/apps/noisepage-performance-guard

    @property
    def conclusion_title_map(self):
        return {
            CONCLUSION_SUCCESS: "Performance Boost!",
            CONCLUSION_NEUTRAL: "Minor Decrease in Performance",
            CONCLUSION_FAILURE: "Major Decrease in Performance",
        }

    @property
    def conclusion_summary_map(self):
        return {
            CONCLUSION_SUCCESS: "Nice job! This PR has increased the throughput of the system.",
            CONCLUSION_NEUTRAL: "Be warned: this PR may have decreased the throughput of the system slightly.",
            CONCLUSION_FAILURE: "STOP: this PR has a major negative performance impact",
        }

    @property
    def conclusion_threshold_map(self):
        return {
            0: CONCLUSION_SUCCESS,
            -5: CONCLUSION_NEUTRAL,
        }

    @property
    def should_add_pr_comment(self):
        return True

    def _get_conclusion_data(self, payload):
        """ Get the performance comparison data between the master branch and
        the commit """
        data = None
        commit_sha = payload.get('commit', {}).get('sha')
        if commit_sha:
            data = get_performance_comparisons(MASTER_BRANCH_NAME, commit_sha)
        return data

    def _get_conclusion(self, data):
        """ Determine the worst performance difference between the master
        branch and the PR's branch and then determine the corresponding
        conclusion status. """
        min_performance_change = get_min_performance_change(data)
        for threshold, conclusion in self.conclusion_threshold_map.items():
            if min_performance_change >= threshold:
                return conclusion
        return CONCLUSION_FAILURE

    def _generate_conclusion_markdown(self, data):
        """ Create a markdown string that describes the Github check and
        details the results of the performance check """
        return generate_performance_result_markdown(data)

    def _generate_pr_comment_markdown(self, data):
        """ Create the markdown string for a PR comment. The comment gives a
        concise view of the performance results and allows the user to expand
        for more details about the tests.
        """
        conclusion = self._get_conclusion(data)

        description_text = f'### {self.conclusion_title_map[conclusion]}\n\n' \
                            f'{self.conclusion_summary_map[conclusion]}\n\n'

        table_headers = ['tps (%change)', 'benchmark_type', 'wal_device', 'details']
        table_content = []
        for config, percent_diff, master_throughput, commit_throughput in data:
            tps = f'{round(percent_diff,2)}%',
            benchmark_type = config.get('benchmark_type')
            wal_device = config.get('wal_device')

            details = generate_details_table_cell(config, master_throughput, commit_throughput)
            row = [tps, benchmark_type, wal_device, details]
            table_content.append(row)

        if len(table_content):
            table_text = tabulate(table_content, headers=table_headers, tablefmt='github')
        else:
            table_text = '**Could not find any performance results to compare for this commit.**'

        return description_text + table_text


def get_performance_comparisons(base_branch, commit_sha):
    """ Compare the performance results from two branches. This returns an array of tuples. The first item in the tuple
    is the OLTPBench config, the second item in the tuple is the % difference in throughput, the third item in the
    tuple is the master branch throughput, and the fourth item in the tuple is the commit's throughput."""
    result_comparisons = []
    commit_results = OLTPBenchResult.get_latest_commit_results(commit_sha)
    logger.debug(f'Commit results: {commit_results}')
    master_results = OLTPBenchResult.get_branch_results_by_oltpbench_configs(base_branch, commit_results)
    logger.debug(f'Master results: {master_results}')
    for c_result in commit_results:
        for m_result in master_results:
            if m_result.is_config_match(c_result):
                config = c_result.get_test_config()
                percent_diff = m_result.compare_throughput(c_result)
                comparison = (config,
                              percent_diff,
                              float(m_result.metrics.get('throughput', 0)),
                              float(c_result.metrics.get('throughput', 0)))
                result_comparisons.append(comparison)
    return result_comparisons


def get_min_performance_change(performance_comparisons):
    """ Determine the worst performance difference between the master branch and the PR's branch and then determine
    the corresponding conclusion status. """
    min_performance_change = 0

    for _, percent_diff, _, _ in performance_comparisons:
        if percent_diff < min_performance_change:
            min_performance_change = percent_diff

    return min_performance_change


def generate_performance_result_markdown(performance_comparisons):
    """ Generate the markdown content that will show up in the detailed view of the check run. This includes a short
    description and a table displaying the OLTPBench test config and results. """
    description_text = ("This performance comparison is based on the performance results collected from the most"
                        " recent nightly build and the results collected during the End-to-End Performance stage of"
                        " this PR's build. If any of the benchmarks see a performance change less than -5% this check"
                        " will fail. If any of the benchmarks see a performance change less than 0% this check will"
                        " have a neutral result. The decrease in performance could be noise or it could be legitimate."
                        " You should rerun the build to check.\n\n")
    table_content = []
    table_headers = []
    for config, percent_diff, master_throughput, commit_throughput in performance_comparisons:
        if len(table_headers) == 0:
            table_headers = ['tps (%change)', 'master tps', 'commit tps'] + list(config.keys())
        row = [f'{round(percent_diff,2)}%',
               round(master_throughput, 2),
               f'{round(commit_throughput,2)}'] + list(config.values())
        table_content.append(row)

    if len(table_content):
        table_text = tabulate(table_content, headers=table_headers, tablefmt='github')
    else:
        table_text = '**Could not find any performance results to compare for this commit.**'

    return description_text + table_text


def generate_details_table_cell(config, master_throughput, commit_throughput):
    config_details_str = ", ".join(["=".join([key, str(val)]) for key, val in config.items()])
    return f'<details><summary>Details</summary>master tps={round(master_throughput,2)},' \
           f' commit tps={round(commit_throughput,2)}, {config_details_str}</details>'
