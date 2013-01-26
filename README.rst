yamltests
=======

Overview
---------

yamltests is `nose <http://somethingaboutorange.com/mrl/projects/nose>`_ plugin for running tests written in `YAML <http://en.wikipedia.org/wiki/YAML>`_. 


Installation
-----------

From the setup directory::

     python setup.py install
     
Using pip::

     pip install https://github.com/vpekar/yamltests/archive/master.zip

Testing the plugin
-----------------

From the setup directory::

     python tests.py

Usage
------

Add the ``--with-yaml-tests`` option. Can be combined with other options, e.g., ``--with-coverage``::

     nosetests --with-yaml-tests
     
To test the *example* package::

     $ nosetests example --with-yamltests
     .....
     ----------------------------------------------------------------------
     Ran 5 tests in 0.014s

     OK
     

Format of YAML files
--------------------

Should be as follows::

     path.to.myModule:
          myFunctionInMyModule:
               description: "Extract twitter handle"
               text: "... @username ..."
               expected: "username"
          myClassInMyModule:
               myMethod:
                    description: "Extract twitter handle"
                    text: "... @username ..."
                    expected: ["username"]

Filenames should begin with "test" and have extension ".yml".

For a working example, see ``example/tests/tests.yml``.

Types of actual and expected outputs
-------------------------------------

Each function/method being tested can output either a string or a 
list. The expected value can be either a string or a list. 
- If the expected value is a string and actual value is a string, assertEqual
is used.
- If the expected value is a string and actual value is a list, assertIn is 
used.
- If the expected value is a list and actual value is a list, assertListEqual
is used.

Notes
------

- If the yaml file contains comma-separated module name (``SomePackage.SomeModule``) then the ``__init__.py`` file inside SomePackage should explicitly import all modules (see the ``__init__.py`` file in the example folder)


