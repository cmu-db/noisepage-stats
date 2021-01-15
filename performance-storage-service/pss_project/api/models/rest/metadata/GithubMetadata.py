class GithubMetadata(object):
    """ This class is the model of the github data relating to the what version of the code the tests/metrics were
    gathered from. This class is how the model is represented in the HTTP API
        git_commit_id - the sha of the commit
        git_branch - the branch that the metrics come from
    """

    def __init__(self, git_commit_id, git_branch):
        self.git_commit_id = git_commit_id
        self.git_branch = git_branch
