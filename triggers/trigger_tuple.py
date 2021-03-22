from collections import namedtuple

# The tuple expected as the main argument in each trigger logic implementation.
# The tuple identifies: -
#   the repository to trigger
#   the repository reference (branch or tag)
#   a user that can access the repository
#   any remote workflow/job inputs
Trigger = namedtuple('Trigger', ['owner',
                                 'repository',
                                 'ref',
                                 'user',
                                 'user_token',
                                 'name',
                                 'inputs'])
