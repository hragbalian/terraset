import os

from .exceptions import (
    SupersetProfileIssue,
    TerrasetProfileNotFoundInPath
)

supported_superset_objects = [
    "charts",
    "dashboards",
    "datasets",
    # "databases"
    ]


directions = [
    'local-to-remote',
    'remote-to-local'
    ]

actions = ['add', 'change', 'delete']

# Kind of hacky but due to inconsistencies in API find vs export -
# key is value in find, value is value in export
find_to_export_map = dict(

    charts = dict(
        slice_name = 'slice_name',
        params = 'params',
        viz_type = 'viz_type',
        description = 'description',
        ),

    dashboards = dict(
        dashboard_title = 'dashboard_title',
        slug = 'slug',
        json_metadata = 'metadata',
        position_json = 'position'
    )

    datasets = dict(
        table_name = 'table_name',
        #others will be supported later
    )
)


required_values = [
    "host","username","password",
    "resources_path",
    ]

if os.environ.get('TERRASET_PROFILE_PATH'):

    from dotenv import dotenv_values
    secrets = dotenv_values(f"{os.environ.get('TERRASET_PROFILE_PATH')}/terraset.profile")

    if not secrets:
        raise TerrasetProfileNotFoundInPath

    host=secrets.get('host')
    username=secrets.get('username')
    password=secrets.get('password')
    resources_path=secrets.get('resources_path')

else:

    if os.environ.get('TERRASET_HOST'):
        host=os.environ.get('TERRASET_HOST')

    if os.environ.get('TERRASET_USERNAME'):
        username=os.environ.get('TERRASET_USERNAME')

    if os.environ.get('TERRASET_PASSWORD'):
        password=os.environ.get('TERRASET_PASSWORD')

    if os.environ.get('TERRASET_RESOURCES_PATH'):
        resources_path=os.environ.get('TERRASET_RESOURCES_PATH')


check = {x:x in globals() and globals()[x] is not None for x in required_values}


if not all([x[1] for x in check.items()]):

    raise SupersetProfileIssue(check)
