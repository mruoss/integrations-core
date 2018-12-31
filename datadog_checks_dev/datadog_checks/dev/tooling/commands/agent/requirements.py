# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import click

from ..console import (
    CONTEXT_SETTINGS, echo_failure, echo_info, echo_success
)
from ...constants import AGENT_V5_ONLY, get_agent_release_requirements
from ...release import get_agent_requirement_line
from ...utils import get_valid_checks, get_version_string
from ....utils import write_file_lines


@click.command(
    context_settings=CONTEXT_SETTINGS,
    short_help="Generate the list of integrations to ship with the Agent and save it to '{}'".format(
        get_agent_release_requirements()
    )
)
@click.pass_context
def requirements(ctx):
    """Write the `requirements-agent-release.txt` file at the root of the repo
    listing all the Agent-based integrations pinned at the version they currently
    have in HEAD.
    """
    echo_info('Freezing check releases')
    checks = get_valid_checks()
    checks.remove('datadog_checks_dev')

    entries = []
    for check in checks:
        if check in AGENT_V5_ONLY:
            echo_info('Check `{}` is only shipped with Agent 5, skipping'.format(check))
            continue

        try:
            version = get_version_string(check)
            entries.append('{}\n'.format(get_agent_requirement_line(check, version)))
        except Exception as e:
            echo_failure('Error generating line: {}'.format(e))
            continue

    lines = sorted(entries)

    req_file = get_agent_release_requirements()
    write_file_lines(req_file, lines)
    echo_success('Successfully wrote to `{}`!'.format(req_file))
