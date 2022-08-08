# Terraset





### Usage
--------

Terraset will manage your superset charts and dashboard (future: other Superset
resources) through code.  In it's usage, it is inspired by Terraform.

Terraset looks within specified folders for chart and dashboard information, appropriately
named `charts` and `dashboards`.  You can put these folders anywhere (e.g. a /tmp/charts, /tmp/dashboards )
but typically you will want to use terraset as part of a CI deployment so these folders
will be in a repository.

### Configuration
-------------

To work, Terraset must connect to a running Superset instance, running either
locally or remotely.  To establish a connection requires a `host`, `username`,
and `password`.  This information can be entered into a `terraset.profile` file
within a directory set by `TERRASET_PROFILE_PATH`, or with environment variables
for each item: `TERRASET_HOST` for host, `TERRASET_USERNAME` for username, and
`TERRASET_PASSWORD` for password.  If set in a terraset.profile file, the file should
be structure as as such:

```{.profile}
host=<my-host>
username=<my-username>
password=<my-password>
```

For the most flexibility, the user connecting to Superset should
have Admin privileges.

### Terraset API
------------

There are six actions that are part of the Terraset api.

1. Terraset Initialize: Downloads all existing dashboards and charts into a
specified folder (future: other resource settings)
2. Terraset Plan: Reports the differences between remote and local and identifies
the updates that will be made upon an `update` call
3. Terraset Create: Uploads
4. Terraset Destroy: Delete all remote resources
5. Terraset Update: Looks at difference between remote and local and updates
remote to local settings (both adding and deleting).
6. Terraset Get: Get's remote settings and overwrites local settings

### Gotchas
-------
* Chart and dashboard folder names need to be unique
* Chart and dashboard folder names should correspond to the corresponding name
of the yml file housing its settings
* If you update a chart or dashboard remotely, to have it reflected in your local
settings use the `.get()` before `.update()`, otherwise you will overwrite your remote
charts with now outdated local settings.

### Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
