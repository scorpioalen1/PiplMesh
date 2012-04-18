Installation
============

The procedure of installing and running your own instance of PiplMesh follows.

*Note: we are assuming that you are running an UNIX-like operating system.*

Prerequisites
-------------

In addition to Python_ the following is required on the system to run PiplMesh:

* Python virtualenv_ package
* Python pip_ package (1.0+)
* MongoDB_ (2.0+)

.. _Python: http://python.org/
.. _Django-supported: https://docs.djangoproject.com/en/1.3/ref/databases/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _pip: http://pypi.python.org/pypi/pip
.. _MongoDB: http://www.mongodb.org/

Other prerequisites (Python packages) are installed later.

Getting Source
--------------

Use ``master`` branch which contains stable PiplMesh source from the project
git_ repository. Get it using this command::

    git clone https://github.com/wlanslovenija/PiplMesh.git

If you are not familiar with git_, please refer to its tutorial_.

.. _git: http://git-scm.com/
.. _tutorial: http://schacon.github.com/git/gittutorial.html

Development/Testing Instance
----------------------------

Deploying
^^^^^^^^^
	
Once you have all prerequisites and PiplMesh itself, you can create Python
virtualenv_ for PiplMesh::

    virtualenv --no-site-packages env_piplmesh
    source env_piplmesh/bin/activate

This will create a local virtualenv directory named ``env_piplmesh`` in your
current working directory. Once you have made it, you can install Python
packages into using pip_::

    pip install -r requirements.txt

This will install all required Python packages into a local virtualenv
directory.

Running
^^^^^^^

PiplMesh consist of many components, so multiple daemons should be running. Run
the following in separate terminals::

    ./manage.py runpushserver
    ./manage.py runserver

PiplMesh is now available at http://localhost:8000/.

More about Django development server in its `documentation`_.

.. _documentation: https://docs.djangoproject.com/en/1.3/intro/tutorial01/#the-development-server

Platform Specific Instructions
------------------------------

Mac OS X
^^^^^^^^

Prerequisites can be installed with MacPorts_ or Homebrew_. For MacPorts::

    sudo port install mongodb py27-virtualenv py27-pip

and to start MongoDB at startup::

    sudo port load mongodb

For Homebrew::

    brew install mongodb

and follow instructions to start MongoDB at startup. You also need Python_,
pip_, and virtualenv_::

    brew install python --universal --framework
    brew install pip
    pip install virtualenv

.. _MacPorts: http://www.macports.org/
.. _Homebrew: http://mxcl.github.com/homebrew/

Debian
^^^^^^

The following Debian packages are needed:

* ``python-virtualenv``
* ``python-pip``
* ``mongodb``

Be careful about required versions. It could be necessary to use packages from
Debian testing or backports distribution.
