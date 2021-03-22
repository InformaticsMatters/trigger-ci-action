"""GitHub Workflow Dispatch Logic.

See https://docs.github.com/en/rest/reference/actions#create-a-workflow-dispatch-event
"""

import requests
import sys

from typing import Dict

from .trigger_tuple import Trigger

_REQUEST_TIMEOUT: float = 4.0


def trigger(trigger: Trigger) -> bool:
    """We're given all the inputs. Here we implement a
    GitHub Workflow Dispatch trigger, returning True on success.
    """

    # 1. Find the workflow (check it exists)
    url: str = 'https://api.github.com/repos/{}/{}/actions/workflows'.\
        format(trigger.owner, trigger.repository)
    headers: Dict[str, str] = {'Accept': 'application/vnd.github.v3+json'}
    auth = (trigger.user, trigger.user_token)
    resp = requests.get(url,
                        headers=headers,
                        auth=auth,
                        timeout=_REQUEST_TIMEOUT)
    assert resp

    if resp.status_code != 200:
        print('Got {} from {}'.format(resp.status_code, url))
        print('json()={}'.format(resp.json()))
        sys.exit(1)
    workflow_url: str = None
    payload: Dict[str, any] = resp.json()
    if 'total_count' not in payload:
        print('Expected "total_count" in response')
        sys.exit(1)
    total_count = payload['total_count']
    if total_count > 0:
        if 'workflows' not in payload:
            print('Expected "workflows" in response')
            sys.exit(1)
        for workflow in payload['workflows']:
            assert 'name' in workflow
            assert 'url' in workflow
            if workflow['name'] == trigger.name:
                workflow_url = workflow['url']
                break
    if not workflow_url:
        print('Workflow not found')
        sys.exit(1)

    # 2. Run the workflow
    dispatch_url = '{}/dispatches'.format(workflow_url)
    payload = {'ref': trigger.ref,
               'inputs': trigger.inputs}
    resp = requests.post(dispatch_url,
                         headers=headers,
                         auth=auth,
                         json=payload,
                         timeout=_REQUEST_TIMEOUT)
    if resp.status_code != 204:
        print('Got {} from {}'.format(resp.status_code, url))
        print('json()={}'.format(resp.json()))
        sys.exit(1)

    # Success if we get here
    return True
