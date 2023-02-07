============================================
REST API Deduplication Endpoints
============================================

The deduplication endpoints serve as a means to manually deduplication datasets and write the results to some output. The format for the urls is "deduplication/input/output". The end results are 
delivered through the output format. Logs on these steps can then be viewed at the "logs" endpoint.


############################################
Exact Match Name Url Example
############################################

Postgres to Postgres
********************************************

rest endpoint: "http://127.0.0.1:8000/deduplicate/database/database"

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
    

This will connect to the default environment settings with the prefix of "POSTGRES":

.. code-block:: bash

    POSTGRES_USERNAME='MY_USER'
    POSTGRES_PASSWORD='MY_PASS'
    POSTGRES_DB='MY_DB'
    POSTGRES_HOST='MY_HOST'
    POSTGRES_PORT='25060'


And perform a deduplication of organization names to urls. The results are written to another table.

To connect to another database instance:

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


The important piece of data in the return is the job id. To view the log of what our dedupe function did, we can go to the logs endpoint and retrieve those results.

