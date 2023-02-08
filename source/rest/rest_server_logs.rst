============================================
REST API Logs
============================================

The deduplication endpoints serve as a means to manually deduplication datasets and write the results to some output. The format for the urls is "deduplication/input/output". The end results are 
delivered through the output format. Logs on these steps can then be viewed at the "logs" endpoint.

.. _rest_json_logs:

############################################
REST Server JSON Logs Example
############################################


********************************************

rest endpoint: "http://127.0.0.1:8000/logs/json"

We can retrieve a log in json format by sending either the "id" or the "job_id" and "step_name".

.. code-block:: javascript

    // Request
    {
        step_name: "deduplicate_exact_match_name_url",
        job_id: "2106ab31-352c-40ce-b41b-1deb9b5f8ed2"
    }    

    // Response
    {
    "status": "success",
    "payload": {
        "log_message": {
            "results": [
                {
                    "id": "46c4acdfa7407bb1f0de32a2467c7987",
                    "name": "*REQUIRED* text",
                    "website": "http://some.domain.com",
                    "address1": "text",
                    "address2": "text",
                    "city": "text",
                    "state": "Two character state (All caps)",
                    "zip": "99999 or 99999-9999"
                },
                ...
            ],
            "duplicates": [
                ...
            ],
            "original": [
                ...
            ]
        "id": "c030f048-e265-4d65-b75c-6cb1fd50efd7",
        "iteration_id": null,
        "step_name": "deduplicate_exact_match_name_url",
        "contributor_name": null
    }
    

The same logs retrieved using the log id:

.. code-block:: javascript

    // Request

    {
        id: "c030f048-e265-4d65-b75c-6cb1fd50efd7"
    }
    
