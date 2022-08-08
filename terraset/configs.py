import os

from .exceptions import (
    SupersetProfileIssue,
    TerrasetProfileNotFoundInPath
)

if os.environ.get('TERRASET_PROFILE_PATH'):

    from dotenv import dotenv_values
    secrets = dotenv_values(f"{os.environ.get('TERRASET_PROFILE_PATH')}/terraset.profile")

    if not secrets:
        raise TerrasetProfileNotFoundInPath

    host=secrets.get('host')
    username=secrets.get('username')
    password=secrets.get('password')

else:

    if os.environ.get('TERRASET_HOST'):
        host=os.environ.get('TERRASET_HOST')

    if os.environ.get('TERRASET_USERNAME'):
        username=os.environ.get('TERRASET_USERNAME')

    if os.environ.get('TERRASET_PASSWORD'):
        password=os.environ.get('TERRASET_PASSWORD')

check = {x:x in globals() for x in ["host","username","password"]}

if not all([x[1] for x in check.items()]):

    raise SupersetProfileIssue(check)


chart_info = ['slice_name','params', 'viz_type','description']
