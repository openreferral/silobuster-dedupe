============================================
REST API
============================================

The REST API included is meant to be ran as a micro service. A defined set of deduplication and/or transformation steps will be a system default setting. Clients can then request information and post
jobs against a set of data. The micro service then handles that job. The idea behind the architecutre is that each micro service handles a particular job. The REST API then handles that job, accepting
inputs from multiple source configurations and outputting to multiple source configurations.

############################################
Initialization
############################################

The core silobuster library can be ran with the included Django DRF server. In the *dockerfiles* directory, issue the following command:

.. code-block:: bash

    docker-compose up -d --build

    # Or

    docker compose up -d --build

    # Depending on your version.


############################################
Configuration
############################################

The server will be exposed to port 8000 by default. This can be changed in the *dockerfiles/docker-compose.yml* file.

The volumes mapped are *deduper* and *libs*.

############################################
Server Configuration
############################################

In the bottom of *deduper/settings.py*, there are some system settings. These include:

#. DEDUPLICATION_STEPS: The available deduplication steps that will be communicated to the client. These are also the default steps for the system.
#. app_logger: A Singleton instance of the :ref:`log_handler` class. This is the server's logger configuration that will be used throughout.