import os

from .exceptions import (
    SupersetProfileIssue,
    TerrasetProfileNotFoundInPath
)

supported_superset_objects = ["charts", "dashboards"]

# These are the entries in the charts YAML files that can be updated
# updateable_info = dict(
#     charts = ['slice_name','params', 'viz_type'], # Description is missing from export
#     dashboards = ['dashboard_title', 'slug'] # There are inconsistencies in what the export produces vs. the read that need to get resolved
# )

bases = ['local-to-remote', 'remote-to-local']

# Kind of hacky but due to inconsistencies in API find vs export -
# key is value in find, value is value in export
find_to_export_map = dict(

    charts = dict(
        slice_name = 'slice_name',
        params = 'params',
        viz_type = 'viz_type',
        description = 'description'
        ),

    dashboards = dict(
        dashboard_title = 'dashboard_title',
        slug = 'slug',
        json_metadata = 'metadata',
        position_json = 'position'
    )

)


required_values = [
    "host","username","password",
    "charts_path", "dashboards_path"
    ]

if os.environ.get('TERRASET_PROFILE_PATH'):

    from dotenv import dotenv_values
    secrets = dotenv_values(f"{os.environ.get('TERRASET_PROFILE_PATH')}/terraset.profile")

    if not secrets:
        raise TerrasetProfileNotFoundInPath

    host=secrets.get('host')
    username=secrets.get('username')
    password=secrets.get('password')
    charts_path=secrets.get('charts_path')
    dashboards_path=secrets.get('dashboards_path')

else:

    if os.environ.get('TERRASET_HOST'):
        host=os.environ.get('TERRASET_HOST')

    if os.environ.get('TERRASET_USERNAME'):
        username=os.environ.get('TERRASET_USERNAME')

    if os.environ.get('TERRASET_PASSWORD'):
        password=os.environ.get('TERRASET_PASSWORD')

    if os.environ.get('TERRASET_CHARTS_PATH'):
        charts_path=os.environ.get('TERRASET_CHARTS_PATH')

    if os.environ.get('TERRASET_DASHBOARDS_PATH'):
        dashboards_path=os.environ.get('TERRASET_DASHBOARDS_PATH')


check = {x:x in globals() and globals()[x] is not None for x in required_values}


if not all([x[1] for x in check.items()]):

    raise SupersetProfileIssue(check)
