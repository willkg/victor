"""Attempts to figure out what version of things we're using in
playdoh-lib. This is made exceedingly difficult because of the
following things:

1. We install with pip to lib/python/, but nix the .egg-info files so
   we have no clue what we installed unless the package also has the
   version information tucked away somewhere.

   This is dumb--we should stop doing this.

2. Some projects squirrel the version away in a place that's difficult
   to pull out.

3. We have a few projects that apparently don't like doing version
   releases.

Also interesting and vaguely related is that we're not including the
license this code that we're distributing is distributed under. That's
a huge license fail.

"""
import importlib
import logging
import os
import re
import site
import sys

import yaml

from victor import __version__


def fix_sys_path(cfg):
    """Adds sitedirs and moves packages to the beginning of sys.path

    Uses "sitedirs" key in config which is a list of paths.
    """
    if 'sitedirs' not in cfg:
        return

    prev_sys_path = list(sys.path)

    for sitedir in cfg['sitedirs']:
        site.addsitedir(sitedir)

    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)

    sys.path[:0] = new_sys_path


class NoVersion(Exception):
    pass


def get_version_from_module(module_name):
    mod = importlib.import_module(module_name)

    # Try some possible version attributes
    for version_string in ('__version__', 'VERSION', 'majorVersionId', 'ver'):
        if hasattr(mod, version_string):
            return getattr(mod, version_string)

    raise NoVersion('{0}: {1}'.format(module_name, dir(mod)))


def get_version_from_requirement(line):
    version_re = re.compile(
        '^'
        '([^=><]+)'
        '(?:\\s*[=><]*\\s*([^=><]*?))?'
        '$')
    match = version_re.match(line)
    return match.groups(0)


def get_version(module_name, verbosity=0):
    if verbosity:
        print '>>>', module_name

    # Try importing various possible version modules
    for version_module in (module_name,
                           '.'.join([module_name, '__version__']),
                           ):
        try:
            return get_version_from_module(version_module)
        except (NoVersion, ImportError):
            logging.exception(version_module)

    # There are a couple of packages that have setup.py **in** the
    # source which is beyond bizarre, but whatevs.
    try:
        mod = importlib.import_module(module_name)

        fp = open(os.path.join(os.path.dirname(mod.__file__), 'setup.py'), 'r')
        for line in fp.readlines():
            line = line.strip()
            if line.startswith('version'):
                line = line.split('=')
                if len(line) > 1:
                    line = line[1].strip().strip('"\',')
                    return line
    except (ImportError, IOError):
        logging.exception(module_name)

    raise NoVersion('{0}'.format(module_name))


def get_blacklist(cfg):
    """Returns list of blacklisted items

    An item is in the blacklist because victor can't divine version
    information for it. This could be because victor sucks or that the
    item has no version information available. We keep it in the
    blacklist because then we have a record that it's problematic.

    Uses "sitedirs" key in config which is a list of paths.

    """
    # This looks a little weird, but handles the None case, too.
    return cfg.get('blacklist') or []


def load_cfg(cfg_fn):
    return yaml.load(open(cfg_fn, 'rb'))


def cmdline_handler(scriptname, argv):
    print '{0}: {1}'.format(scriptname, __version__)

    logging.basicConfig(level=logging.CRITICAL)

    cfg = load_cfg('victor.yaml')

    logging.debug('Fixing sys path...')
    fix_sys_path(cfg)

    logging.debug('Getting blacklist...')
    blacklist = get_blacklist(cfg)

    logging.debug('Going through packagelist...')
    package_to_version = {}
    for mem in cfg.get('packagelist', []):
        if mem.endswith(os.sep) or os.path.isdir(mem):
            for mod in os.listdir(mem):
                name, extension = os.path.splitext(mod)
                if extension not in ('.py', ''):
                    logging.debug('skipping {0}: wrong file type'.format(mod))
                    continue

                if mod in blacklist:
                    logging.debug('skipping {0}: in blacklist'.format(mod))
                    continue

                if mod.endswith('.py'):
                    mod = mod[:-3]

                try:
                    version = get_version(mod)
                    package_to_version[mod] = version
                except NoVersion:
                    package_to_version[mod] = 'NO VERSION'

        elif mem.startswith('REQ '):
            mem = mem[4:].strip()
            fp = open(mem, 'r')
            for mod in fp.readlines():
                mod = mod.strip()
                if not mod or mod.startswith('#'):
                    continue

                mod, version = get_version_from_requirement(mod)

                if mod in blacklist:
                    logging.debug('skipping {0}: in blacklist'.format(mod))
                    continue

                if mod.endswith('.py'):
                    mod = mod[:-3]

                try:
                    version = get_version(mod)
                    package_to_version[mod] = version
                except NoVersion:
                    package_to_version[mod] = 'NO VERSION'

        else:
            if mem in blacklist:
                logging.debug('skipping {0}: in blacklist'.format(mem))
                continue

            try:
                version = get_version(mem)
                package_to_version[mem] = version
            except NoVersion:
                package_to_version[mem] = 'NO VERSION'

    print ''
    print 'Versions:'
    if package_to_version:
        for key, val in sorted(package_to_version.items()):
            print '  {0}: {1}'.format(key, val)
    else:
        print '  <None>'

    print ''
    print 'These have no discernable version:'
    if blacklist:
        for item in blacklist:
            print '  {0}'.format(item)
    else:
        print '  <None>'

"""
bleach: 1.1.x (c381a)
commonware: 0.4.2 (b5544)
django-appconf: 0.5 (d7ff3)
django-compressor: 1.2a2 (90966)
django-cronjobs: (cfda8)
django-mobility: (644e0)
django-mozilla-product-details: (5a59a)
django-multidb-router: (7e608)
django-nose: 1.0 (83c78)
django-session-csrf: (f00ad)
django-sha2: (3ba2b)
funfactory: (faca9)
jingo: (1dc0e)
jingo-minify: (d2ff3)
nuggets: (ce506)
schematic: (e7499)
test-utils: (3c221)
tower: (6112e)
"""
