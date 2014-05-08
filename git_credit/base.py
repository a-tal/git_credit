"""Give credit for the current git project or all projects down from cwd."""


import os
import sys
import subprocess


def _get_credit(filepath):
    """Get a dict of {user: lines in HEAD} for the filepath git repo."""

    _prev_dir = os.getcwd()
    os.chdir(filepath)
    proc = subprocess.Popen(
        "git log --pretty=format:%an", shell=True, stdout=subprocess.PIPE
    )
    proc.wait()
    os.chdir(_prev_dir)

    committers = {}
    for line in proc.stdout or []:
        line = line.strip()
        if isinstance(line, bytes):
            line = line.decode("latin-1")
        if line in committers:
            committers[line] += 1
        else:
            committers[line] = 1
    return committers


def _is_git_dir(filepath):
    """Return a boolean of if this filepath has a .git folder."""

    git_dir = os.path.join(os.path.realpath(filepath), ".git")
    return os.path.exists(git_dir) and os.path.isdir(git_dir)


def _sorted_by_value(credit):
    """Return the credit dict as a sorted list by value."""

    return sorted(credit.items(), key=lambda user: user[1], reverse=True)


def display_credit(credit):
    """Display the credit dict in a nice fashion."""

    total_per_committer = {}
    for repo, committers in credit.items():
        repo_total = sum(committers.values())
        print("git credit for repo: {0}".format(repo))
        for committer, lines in _sorted_by_value(committers):
            print("  {0}: {1} ({2}%)".format(
                committer,
                lines,
                float("{:.2f}".format((lines / repo_total) * 100))
            ))
            if committer in total_per_committer:
                total_per_committer[committer] += lines
            else:
                total_per_committer[committer] = lines

    if len(credit) > 1:
        total_lines = sum(total_per_committer.values())
        print("total git credit for all repos:")
        for committer, lines in _sorted_by_value(total_per_committer):
            print("  {0}: {1} ({2}%)".format(
                committer,
                lines,
                float("{:.2f}".format((lines / total_lines) * 100))
            ))


def _walk_for_git(filepath=None):
    """Get credit for all repos down from filepath.

    Returns:
        dict of {repo: {committer: lines_in_HEAD}}
    """

    if filepath is None:
        filepath = os.curdir

    all_credit = {}
    for repo, _, _ in os.walk(os.path.realpath(filepath)):
        if _is_git_dir(repo):
            all_credit[repo] = _get_credit(repo)
    return all_credit


def _get_help(repo=None):
    """Raises SystemExit with a help message for the user."""

    if repo and len(repo) == 1:
        msg = "{0} is not a git repo".format(repo)
    elif repo and len(repo) > 1:
        msg = "{0} are not git repos".format(", ".join(repo))
    else:
        msg = "{0} is not a git repo".format(os.path.realpath(os.curdir))

    raise SystemExit(msg)


def parse_argv():
    """Check sys.argv for arguments and build the all_credit dict with them."""

    if len(sys.argv) == 1:
        all_credit = _walk_for_git()
    elif len(sys.argv) == 2:
        all_credit = _walk_for_git(sys.argv[1])
    else:
        all_credit = {}
        for arg in sys.argv[1:]:
            all_credit.update(_walk_for_git(arg))

    return all_credit or _get_help()


def main():
    """Command line entry point."""

    display_credit(parse_argv())


if __name__ == "__main__":
    main()
