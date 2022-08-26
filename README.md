Terraset
========

This is a work in progress.

Terraset is a bi-directional source control framework for resources hosted within a Superset environment.
As such, it will help you manage your Superset resources (e.g. charts and dashboards) through code.
The API for Terraset is inspired by Terraform.


Quickstart
--------

```{python}
from terraset.main import Terraset

terraset = Terraset()

terraset.fetch_all()

terraset.plan("local-to-remote")

terraset.apply()
```


Design Considerations
--
Superset is configured to manage all resources (charts, dashboards, datasets, etc) through a set of YAML files, and
it is these files that we want to make sure to store and interact with as our source of truth.  These YAML files can be considered to be Superset's version of a data model, and understanding
the particular specification and parameters (Superset's language, so to speak) these files accept is to understand how to configure Superset purely through code.  

However, because these YAML files are somewhat esoteric for more complex kinds of updates,
and because sometimes (usually!) it is easier to make an update remotely through the UI,
Terraset enables two way synchronization to create a single understanding of truth.  As such, you don't need to start with these YAML files to create a source controlled Superset
environment; you can have an environment up and running, and then move to source control. In fact, we expect most work to be done in the UI and source controlled post-hoc, and for users to have a hybrid workflow, though Terraset neither assumes nor requires this.


Configuration
--
Terraset looks within specified folders for chart and dashboard information,
named `charts` and `dashboards`.  You can put these folders anywhere (e.g. a /tmp/charts, /tmp/dashboards )
but typically you will want to use Terraset as part of a CI deployment so these folders
will be in a repository.

To work, Terraset must connect to a running Superset instance, running either
locally or remotely.  To establish a connection requires a `host`, `username`,
and `password`.  This information can be entered into a `terraset.profile` file
within a directory set by `TERRASET_PROFILE_PATH`, or with environment variables
for each item: `TERRASET_HOST` for host, `TERRASET_USERNAME` for username, and
`TERRASET_PASSWORD` for password.  If set in a terraset.profile file, the file should
be structure as as such:

```
host=<my-host>
username=<my-username>
password=<my-password>
charts_path=
dashboards_path=
```

For the most flexibility, the user connecting to Superset should
have Admin privileges.

Details
--

There are six actions that are part of the Terraset api.

1. Terraset Initialize: Downloads all existing dashboards and charts into a
specified folder (future: other resource settings)
2. Terraset Plan: Reports the differences between remote and local and identifies
the updates that will be made upon an `update` call
3. Terraset Create: Uploads
4. Terraset Destroy: Delete all remote resources
5. Terraset Apply: Looks at difference between remote and local and updates
remote to local settings (both adding and deleting).
6. Terraset Get: Get's remote settings and overwrites local settings



Gotchas
--
* Chart and dashboard folder names need to be unique
* Chart and dashboard folder names should correspond to the corresponding name
of the yml file housing its settings
* If you update a chart or dashboard remotely, to have it reflected in your local
settings use the `.get()` before `.update()`, otherwise you will overwrite your remote
charts with now outdated local settings.

Credits
--

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
