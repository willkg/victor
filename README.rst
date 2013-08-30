=======
Read me
=======

Victor is a valiant attempt at writing a script that tells you the
versions of things you're using on your project and whether they're
out of date.

By "valiant", I mean it currently handles:

* looking at listed packages and directories of packages
* looking for the myriad ways developers squirrel away version
  information---different places (``package/__init__.py``, ...) as
  well as the variety of possible names (``VERSION``, ``sver``,
  ``version``, ``__version__``, ...)

I want to additionally add support for the following:

* pip and easy_install metadata
* git submodules

It currently generates a list of all those packages and the version
information it discovered.


Status
======

August 30th, 2013: I'm still experimenting with this. It's possible
this is a really dumb idea and/or that it's trying to solve a problem
that we created by doing dumb things.


Quick start
===========

1. Install: ``pip install victor``
2. Change directory to the root of a project you want to know version
   information for.
3. Create a ``victor.yaml`` file. (See below.)
4. Run: ``victor-cmd``


YAML configuration file
=======================

Create a ``victor.yaml`` file in the directory you run ``victor-cmd``
in. It has three keys: ``sitedirs``, ``packagelist`` and ``blacklist``.

``sitedirs``
    List of directories to pass into ``site.addsitedir``.

``packagelist``
    List of packages, directoris of packages and requirements files to
    generate the list of packages we're going to hunt for version
    information.

    Examples:

    * ``vendor/`` - Will look at all packages in this directory. Note
      that it does **not** recurse.
    * ``foo`` - Will look at this packages.
    * ``REQ path/to/requirements.txt`` - Will look at packages listed
      in this requirements file.

``blacklist``
    List of packages you know don't have version information in them.

    Some packages have no version information in them. This lets you
    explicitly denote that in your ``.yaml`` file so you don't forget,
    but otherwise doesn't try to find version information for that
    package.


Example::

    sitedirs:
      - vendor/

    packagelist:
      - vendor/src/
      - vendor/packages/
      - REQ requirements/compiled.txt

    blacklist:
      - cef.py


Project details
===============

:Code:          https://github.com/willkg/victor
:Documentation: this README
:Issue tracker: https://github.com/willkg/victor/issues
:License:       BSD 3-clause; see LICENSE file


Why is it called victor?
========================

This is how I name my software projects.
