from tabulate import tabulate
import logging

from pss_project.api.models.database.OLTPBenchResult import OLTPBenchResult
from pss_project.api.constants import GITHUB_APP_IDENTIFIER, PERFORMANCE_COP_CHECK_NAME, MASTER_BRANCH_NAME

logger = logging.getLogger()

CONCLUSION_SUCCESS = 'success'
CONCLUSION_NEUTRAL = 'neutral'
CONCLUSION_FAILURE = 'failure'

THRESHOLD_CONCLUSION_MAP = {
    0: CONCLUSION_SUCCESS,
    -5: CONCLUSION_NEUTRAL,
}

CONCLUSION_TITLE_MAP = {
    CONCLUSION_SUCCESS: "Performance Boost!",
    CONCLUSION_NEUTRAL: "Minor Decrease in Performance",
    CONCLUSION_FAILURE: "Major Decrease in Performance",
}

CONCLUSION_SUMMARY_MAP = {
    CONCLUSION_SUCCESS: "Nice job! This PR has increased the throughput of the system.",
    CONCLUSION_NEUTRAL: "Be warned: this PR may have decreased the throughput of the system slightly.",
    CONCLUSION_FAILURE: "STOP: this PR has a major negative performance impact",
}


def should_initialize_check_run(pull_request_action):
    """ Determine if the pull request event should initialize a check run """
    return pull_request_action in ['synchronize', 'opened', 'reopened']


def initialize_check_run_if_missing(repo_client, commit_sha):
    """ Check to see if the check run was already created. If it was not then
    initialize the check run """
    check_run = repo_client.get_commit_check_run_for_app(commit_sha, GITHUB_APP_IDENTIFIER)
    if not check_run:
        initialize_check_run(repo_client, commit_sha)
        logger.debug('Check run did not exist. It has been initialized')


def initialize_check_run(repo_client, sha):
    """ Create the initial performance cop check run. The run starts in the
    queued state """
    create_body = create_initial_check_run(sha)
    repo_client.create_check_run(create_body)
    logger.debug('Initialized check run')


def create_initial_check_run(sha):
    """ Generate the body of the request to create the github check run. """
    return {
        "name": PERFORMANCE_COP_CHECK_NAME,
        "head_sha": f"{sha}",
        "status": "queued",
        "output": {
            "title": "Pending CI",
            "summary": "This check will run after CI completes successfully"
        }
    }


def complete_check_run(repo_client, commit_sha):
    """ Update the check run with a complete status based on the performance
    results. If the check run does not exist do nothing """
    check_run = repo_client.get_commit_check_run_for_app(commit_sha, GITHUB_APP_IDENTIFIER)
    if check_run:
        repo_client.update_check_run(check_run.get('id'), performance_check_result(commit_sha))
        logger.debug('Check run updated with performance results')


def performance_check_result(commit_sha):
    """ Create a check run request body to make a check run as complete. Generate the status and output contents based
    on the comparison between this PRs performance results and the nightly build's performance results."""
    performance_comparisons = get_performance_comparisons(MASTER_BRANCH_NAME, commit_sha)
    conclusion = get_performance_comparisons_conclusion(performance_comparisons)
    return {
        "name": PERFORMANCE_COP_CHECK_NAME,
        "status": "completed",
        "conclusion": conclusion,
        "output": {
            "title": CONCLUSION_TITLE_MAP.get(conclusion),
            "summary": CONCLUSION_SUMMARY_MAP.get(conclusion),
            "text": generate_performance_result_markdown(performance_comparisons),
        },
    }


def get_performance_comparisons(base_branch, commit_sha):
    """ Compare the performance results from two branches. This returns an array of tuples. The first item in the tuple
    is the OLTPBench config and the second item in the tuple is the difference in throughput. """
    result_comparisons = []
    branch_results = OLTPBenchResult.get_latest_commit_results(commit_sha)
    master_results = OLTPBenchResult.get_branch_results_by_oltpbench_configs(base_branch, branch_results)
    for b_result in branch_results:
        for m_result in master_results:
            if m_result.is_config_match(b_result):
                config = b_result.get_test_config()
                percent_diff = m_result.compare_throughput(b_result)
                result_comparisons.append((config, percent_diff))
    return result_comparisons


def get_performance_comparisons_conclusion(performance_comparisons):
    """ Determine the worst performance difference between the master branch and the PR's branch and then determine
    the corresponding conclusion status. """
    min_performance_change = 0

    for _, percent_diff in performance_comparisons:
        if percent_diff < min_performance_change:
            min_performance_change = percent_diff

    return get_comparisons_conclusion(min_performance_change)


def get_comparisons_conclusion(min_performance_change):
    """ Determine the conclusion status of the check run based on the worst performance difference between the master
    branch and the PR branch's performance results. Improved performance will yield a positive status and degraded
    performance will yeild a neutral or failed status. """
    for threshold, conclusion in THRESHOLD_CONCLUSION_MAP.items():
        if min_performance_change >= threshold:
            return conclusion
    return CONCLUSION_FAILURE


def generate_performance_result_markdown(performance_comparisons):
    """ Generate the markdown content that will show up in the detailed view of the check run. This includes a short
    description and a table displaying the OLTPBench test config and results. """
    description_text = ("This performance comparison is based on the performance results collected from the most"
                        " recent nightly build and the results collected during the End-to-End Performance stage of"
                        " this PR's build. If any of the benchmarks see a performance change less than -5% this check"
                        " will fail. If any of the benchmarks see a performance change less than 0% this check will"
                        " have a neutral result. In this case it could the decrease in performance could be noise or"
                        " it could be legitimate. You should rerun the build to check.\n\n")
    table_content = []
    table_headers = []
    for config, percent_diff in performance_comparisons:
        if len(table_headers) == 0:
            table_headers = list(config.keys()) + ['tps (% change)']
        row = list(config.values()) + [f'{round(percent_diff,2)}%']
        table_content.append(row)

    table_text = tabulate(table_content, headers=table_headers, tablefmt='github')

    return description_text + table_text


def cleanup_check_run(branch):
    """ After finished with a branch delete all the performance results from the database relating to that branch """
    logger.debug(f'Running cleanup on {branch} branch')
    # OLTPBenchResult.get_all_branch_results(branch).delete()
    # #TODO: cleanup method once we know this wont delete the wrong thing
    logger.debug("The following records will be deleted by the cleanup")
    branch_results = OLTPBenchResult.get_all_branch_results(branch)
    for result in branch_results:
        logger.debug(f"Deleting record {result.id} with git_branch {result.git_branch}")
