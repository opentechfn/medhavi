.. _api_guide:

API Guide
=========

Currently added support for below restful APIs. To run these APIs follow below
steps:

1. Create a Database by running below commands:


.. code-block:: python

    python migrate.py db init
    python migrate.py db migrate

2. Run the application by running wsgi.py


.. code-block:: python

    python wsgi.py

Create data [POST]
------------------

The json file passed by user is validated first. If the json file is valid
then MLData, resource and nodes data is added in DB.


.. code-block:: python


    http://localhost:9000/data

List Resource [GET]
--------------------

List all the resources and nodes attached to each resource.


.. code-block:: python

    http://localhost:9000/resource

Show Resource Details [GET]
---------------------------

Show a particular resource details. In the response it will return resource data
along with nodes information attached to it.


.. code-block:: python

   http://localhost:9000/resource/<uuid>

Delete Resource [DELETE]
------------------------

Delete a particular resource by providing its uuid.


.. code-block:: python

    http://localhost:9000/resource/<uuid>

List MLData [GET]
-----------------

List all MLData.


.. code-block:: python

    http://localhost:9000/mldata

Show MLData Details [GET]
-------------------------

Show a particular MLData details by providing its uuid.


.. code-block:: python

    http://localhost:9000/mldata/<uuid>

Delete MLData [DELETE]
----------------------

Delete a particular MLData by providing its uuid.


.. code-block:: python

    http://localhost:9000/mldata/<uuid>

List Nodes [GET]
-----------------

List all nodes.


.. code-block:: python

    http://localhost:9000/node

Show Node Details [GET]
-----------------------

Show a particular node details by providing its uuid.


.. code-block:: python

    http://localhost:9000/node/<uuid>

Delete Node [DELETE]
--------------------

Delete a particular Node by providing its uuid.


.. code-block:: python

    http://localhost:9000/node/<uuid>
