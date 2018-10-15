Development
-----------

Because the parser may break on changes to the canteen website, it should be easy to fix. Refer to the following sections to jumpstart development.

Quickstart
~~~~~~~~~~

Use `Pipenv <https://pipenv.readthedocs.io/en/latest/>`_ to setup the environment and start coding: ::

    $ pipenv install --two --dev  # Create venv
    $ make test                   # Check setup by running tests
    $ make debug                  # Start app instance with debugger and pretty printing of JSON
    $ make run                    # Start app without debugger
    $ make lint                   # Enforce style guide / check for logic bugs
    $ cd docs && make livehtml    # View live-updating docs in the browser

The list of available canteens is available at the ``/canteens`` endpoint. The ``/canteens/<name>`` endpoint provides the XML feed for individual canteens, e.g., ``/canteens/griebnitzsee``.

Given the default configuration, http://127.0.0.1:5000/canteens/griebnitzsee will display the `OpenMensa` meta-feed for the Griebnitzsee canteen, and http://127.0.0.1:5000/canteens/griebnitzsee/menu will render the menu feed.

Main Module Entry Points
~~~~~~~~~~~~~~~~~~~~~~~~

In the following the main workflow of this parser is explained.
Generating a new `OpenMensa` feed starts by reading the configured canteens. Some canteen data, such as ID, name, and location, are currently not scraped. Doing so would be very brittle and involve a multistep process. Refer to the :ref:`cache_hash` for deeper insight into the obstacles.

.. autofunction:: stw_potsdam.config.read_canteen_config

.. autoclass:: stw_potsdam.config.Canteen

Use the canteen data to assemble the menu parameters in order to download the menu JSON. The menu parameters are also used as cache key: it should uniquely identify the retrieved menu.

.. autoclass:: stw_potsdam.canteen_api.MenuParams

.. autofunction:: stw_potsdam.canteen_api.download_menu

The render module contains methods for converting the JSON response into valid `OpenMensa` menu and meta feeds, respectively:

.. autofunction:: stw_potsdam.feed.render_menu
.. autofunction:: stw_potsdam.feed.render_meta

Tests
~~~~~

Unit tests are not a really good fit to the problem at hand. The parser is basically a converter, transforming loosely defined JSON input to well-specified XML output. The conversion is not very sophisticated, and the parser's correctness mainly depends on the stability of the JSON output of the canteen website. Two main questions are remaining.

First, if the parser logic has changed, has the change been intentionally, and is it meaningful? The `consistency` integration test covers that, it compares the results of one examplary API response to a canned XML feed.

Second, if the canteen API changed, or there is some variance in the response which has not been apparent at development time, which canteens are affected? The `retrieval` acceptance test iterates over all configured canteens, and tries to download and interpret the current API responses. No exception indicates a successful run.

Test execution works as follows: ::

    make test                    # (1)
    ENABLE_API_QUERY=1 make test # (2)

The first invocation runs tests whose outcome can solely be determined by the test suite, which makes them suitable for frequent execution and CI systems.
Setting the environment variable ``ENABLE_API_QUERY`` enables tests which require querying the canteen API. Because third-party services are queried, those are more suited to manual execution. Developers can quickly check if their change is applicable to today's menu.



