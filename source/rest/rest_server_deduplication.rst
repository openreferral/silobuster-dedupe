############################################
REST API Deduplication Endpoints
############################################


The deduplication endpoints serve as a means to manually deduplication datasets and write the results to some output. The format for the urls is "deduplication/input/output". The end results are 
delivered through the output format. Logs on these steps can then be viewed at the "logs" endpoint.


============================================
Exact Match Name Url Example
============================================



The exact match algorithm matches organizations and websites. Websites are lower cased and the protocol and "www" is removed. The algorithm expects two columns:

#. website
#. name

Any additional column is passed through. So, if several algorithms are chained together, then the columns passed to this algorithm will be "passed through" to the next algorithm. for example,
we can pass an array for steps:

.. code-block:: javascript

    [
        "deduplicate_exact_match_name_url",
        "deduplicate_exact_match_address"
    ]


The "deduplicate_exact_match_address" needs columns related to addresses, such as address_1 and city. So, we pass those columns to the query. Once the "deduplicate_exact_match_name_url" has been executed, those additional columns
are then available to the "deduplicate_exact_match_address".


============================================
Postgres to Postgres Example
============================================


rest endpoint: "http://127.0.0.1:8000/deduplicate/database/database"


The REST API server is configured to run a series of deduplication steps (see :ref:`rest_server_configuration`) by default.


.. code-block:: javascript

    // Request
    {
        source_query: "SELECT o.id as organization_id, o.name as name, o.url as url, a.address_1 as address1, a.address_2 as address2, a.city, a.state_province as state, a.postal_code as zip \
                        FROM organization o JOIN location l on l.organization_id = o.id \
                        JOIN address a on a.location_id = l.id WHERE type = 'physical'",
        destination_query: "INSERT INTO urls_deduped (organization_id, name, url, address_1, address_2, city, state, zip) VALUES (%s, $s, %s, %s, %s, %s, %s, %s)",

    }

    // Response
    {
       "status": "success",
        "message": "Results delivered to db",
        "payload": {
            "job_id": "8332f2cb-b275-4ed0-966f-693fd73d5f21"
        }
    }
    


.. note::
    
    Your actual job_id will be unique and not the same as in the examples.


This will connect to the default environment settings with the prefix of "POSTGRES":

.. code-block:: bash

    POSTGRES_USERNAME='MY_USER'
    POSTGRES_PASSWORD='MY_PASS'
    POSTGRES_DB='MY_DB'
    POSTGRES_HOST='MY_HOST'
    POSTGRES_PORT='25060'


And perform a deduplication of the steps defined in the dict, DEDUPLICATION_STEPS. The results are written to the destination_query.


You can specify custom database settings.

================================================
Custom Database Settings Deduplication Example
================================================


.. code-block:: javascript

    // Request
    {
        source_host: "my_cluster_host",
        source_db: "my_db",
        source_username: "admin",
        source_password: "rossum",
        source_schema: "private_data",
        source_query: "SELECT o.id as organization_id, o.name as name, o.url as url, a.address_1 as address1, a.address_2 as address2, a.city, a.state_province as state, a.postal_code as zip \
                        FROM organization o JOIN location l on l.organization_id = o.id \
                        JOIN address a on a.location_id = l.id WHERE type = 'physical'",
        destination_host: "my_cluster_host",
        destination_db: "my_dedupes_db",
        destination_username: "admin",
        destination_password: "guidovan",
        destination_schema: "public_data",
        destination_query: "INSERT INTO urls_deduped (organization_id, name, url, address_1, address_2, city, state, zip) VALUES (%s, $s, %s, %s, %s, %s, %s, %s)",

    }

    // Response
    {
       "status": "success",
        "message": "Results delivered to db",
        "payload": {
            "job_id": "21e15641-ad3d-42ac-83e1-2df8a90d0e4c"
        }
    }


The return contains the job id (for more information, see :ref:`logs`). To view the log of what our dedupe function did, we can go to the logs endpoint and retrieve those results. See :ref:`_rest_json_logs`.

Mutation steps can be chained (see :ref:`workers`). The results of one step is fed into another step.



================================================
Chaining Steps Deduplicaton Example
================================================


The following example chains two steps together. The final result will be committed to the database. 

.. code-block:: javascript


    // Request
    {
        source_host: "my_cluster_host",
        source_db: "my_db",
        source_username: "admin",
        source_password: "rossum",
        source_schema: "private_data",
        source_query: "SELECT o.id as organization_id, o.name as name, o.url as url, a.address_1 as address1, a.address_2 as address2, a.city, a.state_province as state, a.postal_code as zip \
                        FROM organization o JOIN location l on l.organization_id = o.id \
                        JOIN address a on a.location_id = l.id WHERE type = 'physical'",
        destination_host: "my_cluster_host",
        destination_db: "my_dedupes_db",
        destination_username: "admin",
        destination_password: "guidovan",
        destination_schema: "public_data",
        destination_query: "INSERT INTO urls_deduped (organization_id, name, url, address_1, address_2, city, state, zip) VALUES (%s, $s, %s, %s, %s, %s, %s, %s)",
        dry_run: "true"
        steps: [
            "deduplicate_exact_match_name_url",
            "deduplicate_exact_match_address"
        ]
    }

    // Response
    {
       "status": "success",
        "message": "Results delivered to db",
        "payload": {
            "job_id": "56b9e0ac-2b97-4b49-b4b5-7b227bc40df0"
        }
    }



================================================
Postgres to JSON Example
================================================


rest endpoint: "http://127.0.0.1:8000/deduplicate/database/json"

We can connect to a database and return the results in JSON using the above endpoint. The payload will include the "job_id" and the "results".



.. code-block:: javascript


    // Request
    {
        source_host: "my_cluster_host",
        source_db: "my_db",
        source_username: "admin",
        source_password: "rossum",
        source_schema: "private_data",
        source_query: "SELECT o.id as organization_id, o.name as name, o.url as url, a.address_1 as address1, a.address_2 as address2, a.city, a.state_province as state, a.postal_code as zip \
                        FROM organization o JOIN location l on l.organization_id = o.id \
                        JOIN address a on a.location_id = l.id WHERE type = 'physical'",
    
        steps: [
            "deduplicate_exact_match_name_url",
            "deduplicate_exact_match_address"
        ]

    }


    // Response

    {
        "status": "success",
        "payload": {
            "job_id": "cc407046-4bfa-4f3b-8736-72ad61ca71ef",
            "results": [
                {
                    "id": "46c4acdfa7407bb1f0de32a2467c7987",
                    "name": "*REQUIRED* text",
                    "website": "http://some.domain.com",
                    "address_1": "text",
                    "address_2": "text",
                    "city": "text",
                    "state_province": "Two character state (All caps)",
                    "postal_code": "99999 or 99999-9999"
                },
                ...
            ]
        }
    }



================================================
Postgres to Excel Example
================================================


rest endpoint "http://127.0.0.1:8000/deduplicate/database/excel"

We can connect to the database and return the results as an excel file. The name of the file is the "job_id". To retrieve the Excel version fo the results, see :ref:`rest_json_logs`.


.. code-block:: javascript


    // Request
    {
        source_host: "my_cluster_host",
        source_db: "my_db",
        source_username: "admin",
        source_password: "rossum",
        source_schema: "private_data",
        source_query: "SELECT o.id as organization_id, o.name as name, o.url as url, a.address_1 as address1, a.address_2 as address2, a.city, a.state_province as state, a.postal_code as zip \
                        FROM organization o JOIN location l on l.organization_id = o.id \
                        JOIN address a on a.location_id = l.id WHERE type = 'physical'",
    
        steps: [
            "deduplicate_exact_match_name_url",
            "deduplicate_exact_match_address"
        ]

    }


If using Postman to test this endpoint, be sure to select "Send and Download".