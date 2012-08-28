#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>

"""Dumps lists of files.
"""

import os
import sys

# Driver API
# ==========

def dumplist(args):
  """Dumps lists of files based on your criteria"""

  from .query import Database
  db = Database()

  r = db.files(
      directory=args.directory,
      extension=args.extension,
      protocol=args.protocol,
      purposes=args.purposes,
      #model_ids=args.model_ids,
      groups=args.groups
      )

  output = sys.stdout
  if args.selftest:
    from bob.db.utils import null
    output = null()

  for id, f in r.items():
    output.write('%s\n' % (f,))
  
  return 0

def add_command(subparsers):
  """Add specific subcommands that the action "dumplist" can use"""

  from argparse import SUPPRESS

  parser = subparsers.add_parser('dumplist', help=dumplist.__doc__)

  parser.add_argument('-d', '--directory', dest="directory", default='', help="if given, this path will be prepended to every entry returned (defaults to '%(default)s')")
  parser.add_argument('-e', '--extension', dest="extension", default='', help="if given, this extension will be appended to every entry returned (defaults to '%(default)s')")
  parser.add_argument('-p', '--protocol', dest="protocol", default='', help="if given, limits the dump to a particular subset of the data that corresponds to the given protocol (defaults to '%(default)s')", choices=('lp1', 'lp2', 'darkened-lp1', 'darkened-lp2', ''))
  parser.add_argument('-u', '--purposes', dest="purposes", default='', help="if given, this value will limit the output files to those designed for the given purposes. (defaults to '%(default)s')", choices=('enrol', 'probe', ''))
  # TODO: model_ids
  parser.add_argument('-g', '--groups', dest="groups", default='', help="if given, this value will limit the output files to those belonging to a particular protocolar group. (defaults to '%(default)s')", choices=('dev', 'eval', 'world', ''))
  parser.add_argument('-c', '--classes', dest="classes", default='', help="if given, this value will limit the output files to those belonging to the given classes. (defaults to '%(default)s')", choices=('client', 'impostor', ''))
  parser.add_argument('--self-test', dest="selftest", default=False,
      action='store_true', help=SUPPRESS)

  parser.set_defaults(func=dumplist) #action
