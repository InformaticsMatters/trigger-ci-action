#!/usr/bin/env python

# All triggers are supplied with a set of arguments,
# containing the following values...
#
# ci-owner
# ci-repository
# ci-ref
# ci-user
# ci-user-token
# ci-name
# ci-inputs (a potentially empty dictionary of keys and values
#            required/expected as the remote workflow inputs)


import importlib
import sys
from typing import Dict, List

from triggers.trigger_tuple import Trigger

# A map of types to modules.
# Rather than use the variable to load the module (not terribly safe)
# we use a simple built-in lookup. For every type of CI trigger
# there is a Python module in the 'triggers' package that implements it.
# This dictionary maps type to trigger module...
_SUPPORTED_TYPES: Dict[str, str] =\
    {'github-workflow-dispatch': 'github_workflow_dispatch'}

# Executed, within the Action, with a number of arguments.
# The first must me the trigger type. The first argument is
# our name, so inputs begin at '1'.
num_args = len(sys.argv) - 1
if num_args != 8:
    print('Incorrect argument count (%s)' % num_args)
    sys.exit(1)
_CI_TYPE: str = sys.argv[1]

if _CI_TYPE not in _SUPPORTED_TYPES:
    print('Unsupported type (%s)' % _CI_TYPE)
    sys.exit(1)

# The last index contains the space-separated CI inputs (i.e. 'x=1 b=2').
# Create a map from it, ignoring any key called 'no-such-input',
# which is our 'user supplied nothing' default
_CI_INPUTS: str = sys.argv[-1]
_CI_INPUT_MAP: Dict[str, str] = {}
for ci_input in _CI_INPUTS.split():
    # Each item must have two parts, i.e. "a=1" must be "a" and "1"
    items = ci_input.split('=')
    if len(items) != 2:
        print('Expected "a=1" got "%s"' % ci_input)
        sys.exit(1)
    # If the key is our dummy value we can stop
    if items[0] == 'no-such-input':
        break
    # Otherwise collect the pair
    _CI_INPUT_MAP[items[0]] = items[1]

# Create a new Trigger tuple from the arguments,
# excluding the ci-type and replacing the last entry
# with our input key/value dictionary (which may be empty).
_TRIGGER_ARGS: List[any] = sys.argv[2:-1]
_TRIGGER_ARGS.append(_CI_INPUT_MAP)
_TRIGGER = Trigger(*_TRIGGER_ARGS)

# Import the ci-type-specific trigger logic.
# Each logic module has a 'trigger' method that takes a Trigger tuple,
# returning False on failure.
module = importlib.import_module('triggers.' + _SUPPORTED_TYPES[_CI_TYPE])
if not module.trigger(_TRIGGER):
    print('Trigger failed')
    sys.exit(1)
