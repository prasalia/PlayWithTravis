#!/usr/bin/env python2.7
""" Generate release notes for the upcoming release and publish to Confluence
    Link: https://tools.publicis.sapient.com/confluence/display/CNTBG/Git+Commit+History
    Usage:
    python ./generate_release_notes.py previous_version new_version
    Example:
    python ./generate_release_notes.py 1.35 1.40
"""
import re
import sys
import confluence
import jira
import git
import utils

if __name__ == '__main__':

    RN_PARENT_PAGE = 'Git Commit History'
    utils.setencoding()

    def set_release_version():
        """ Displays the command line usage for this script
        """
        if len(sys.argv) != 3:
            raise ValueError \
                (
                    'Invalid arguments. Run the script as below \n'
                    'python ./generate_release_notes.py previous_version new_version\n'
                    'Example:\n'
                    'python ./generate_release_notes.py 1.35 1.40'
                )
        else:
            return (sys.argv[1], sys.argv[2])
    (current_ver, next_ver) = set_release_version()
    rn_page = 'Release %s' % (next_ver)

    if not git.istag('v%s' % (current_ver)):
        raise ValueError('Tag v%s not found. Cannot proceed.' % current_ver)

    branch = 'develop'
    range = ''
    if git.istag('v%s' % (next_ver)):
        branch = ''
        range = 'v%s..v%s' % (current_ver, next_ver)
    else:
        if git.isbranch('beta-trial-%s' % (next_ver)):
            branch = 'beta-trial-%s' % (next_ver)
        elif git.isbranch('alpha-trial-%s' % (next_ver)):
            branch = 'alpha-trial-%s' % (next_ver)
        range = 'v%s..' % (current_ver)

    print 'Collecting the list of PRs and commits in this release'
    pr_list = git.log({ 'range' : range, 'includetype' : 'merges', 'branch' : branch})
    commit_list = git.log({ 'range' : range, 'includetype' : 'nomerges', 'branch' : branch})

    table_data = '<h2><i><font color="blue">List of Features in this release (Pull Requests)</font></i></h2>'
    table_data = table_data + \
                (
                    '<table class="confluenceTable">'
                        '<tbody>'
                            '<tr>'
                                '<th width="200" class="confluenceTh">JIRA</th>'
                                '<th width="600" class="confluenceTh">Summary</th>'
                                '<th class="confluenceTh">JIRA Reporter</th>'
                                '<th class="confluenceTh">JIRA Assignee</th>'
                                '<th class="confluenceTh">Git Hash</th>'
                                '<th class="confluenceTh">Branch</th>'
                                '<th class="confluenceTh">Branch Owner</th>'
                                '<th width="200" class="confluenceTh">Date</th>'
                                '<th class="confluenceTh">Pull Request</th>'
                            '</tr>'
                )

    for key in pr_list:
        print 'Checking log entry %s' % (key)
        (pr_id, jira_id, jira_summary, jira_reporter, jira_assignee, jira_link, pr_id, pr_link, branch_name) = ('-','-','-','-','-','javascript:void(0);','-','javascript:void(0);','-')
        data = re.search(r"^Merge pull request #(\d+) from ConnectedHomes/(.+(CNTBG-\d+).+|.+)", key["commitmessage"])
        if data:
            (pr_id, branch_name) = (data.group(1), data.group(2))
            if data.group(3):
                jira_id = data.group(3)
                print 'Getting additional details for JIRA %s' % (jira_id)
                jira_details = jira.details(jira_id)
                if jira_details:
                    jira_summary = jira_details['summary']
                    jira_reporter = jira_details['reporter']
                    jira_assignee = jira_details['assignee']
                else:
                    jira_id = 'Invalid'
            jira_link = jira.url(jira_id)
            pr_link = git.pr_url(pr_id)

        table_data = table_data + \
                (
                            '<tr>'
                                '<td class="confluenceTd"><a href="' + jira_link + '">' + jira_id + '</a></td>'
                                '<td class="confluenceTd">' + utils.escape_html(jira_summary) + '</td>'
                                '<td class="confluenceTd">' + jira_reporter + '</td>'
                                '<td class="confluenceTd">' + jira_assignee + '</td>'
                                '<td class="confluenceTd">' + key["id"] + '</td>'
                                '<td class="confluenceTd">' + utils.escape_html(branch_name) + '</td>'
                                '<td class="confluenceTd">' + key["owner"] + '</td>'
                                '<td class="confluenceTd">' + key["commitdate"] + '</td>'
                                '<td class="confluenceTd"><a href="' + pr_link + '">' + pr_id + '</a></td>'
                            '</tr>'
                )

    table_data = table_data + \
            (
                    '</tbody>'
                '</table>'
            )

    table_data = table_data + '<h2><i><font color="blue">List of Commits in this release</font></i></h2>'
    table_data = table_data + \
                (
                    '<table class="confluenceTable">'
                        '<tbody>'
                            '<tr>'
                                '<th width="200" class="confluenceTh">Git Hash / Changeset</th>'
                                '<th width="200" class="confluenceTh">Commited By</th>'
                                '<th width="200" class="confluenceTh">Date</th>'
                                '<th class="confluenceTh">Commit Message</th>'
                            '</tr>'
                )

    for key in commit_list:
        print 'Checking log entry %s' % (key)
        commit_link = git.commit_url(key["id"])
        table_data = table_data + \
                (
                            '<tr>'
                                '<td class="confluenceTd"><a href="' + commit_link + '">' + key["id"] + '</a></td>'
                                '<td class="confluenceTd">' + key["commitby"] + '</td>'
                                '<td class="confluenceTd">' + key["commitdate"] + '</td>'
                                '<td class="confluenceTd">' + utils.escape_html(key["commitmessage"]) + '</td>'
                            '</tr>'
                )
                
    table_data = table_data + \
            (
                    '</tbody>'
                '</table>'
            )

    confluence.publish({'title' : rn_page, 'ancestor' : RN_PARENT_PAGE, 'body' : table_data})