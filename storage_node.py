import re

import graveldb
import gravelrpc
import cmd_util

import gravelnode

PATH = '/gravel/system/node'

class Box(graveldb.Table('boxes', PATH)):
    default = dict(type=None, active=False, options=None)
    autocreate = False

    def validate(self):
        if not re.match('^[a-zA-Z0-9:_.]+$', self.name):
            raise ValueError('invalid name')
        for k in self.data.options or []:
            if not re.match('^[a-z0-9_]+$', self.name):
                raise ValueError('invalid option name')

    def asked_to_activate(self):
        self.fetch(make_new=True)
        self.save()

    def fetch(self, make_new=False):
        if self.data.active:
            return
        fetch_info = gravelnode.master_call('storage', 'fetchinfo', self.name, decode=gravelrpc.bson)
        if fetch_info.get('new'):
            if make_new:
                self._init_new()
            else:
                raise Exception('resource doesn\'t exist yet')
        else:
            self._really_fetch(fetch_info)

    def _init_new(self):
        args = ['new', self.name]
        for k, v in self.data.options.items():
            args.append('--%s=%s' % (k, v)) # hmm, hmm
        cmd_util.call_exe_in_directory('plugins.d', self.data.type, args)

    def _really_fetch(self, info):
        raise NotImplementedError()

    def ensure_active(self):
        if not self.data.active:
            gravelnode.master_call('storage', 'activate')

    def _fetch_first(self):
        info = gravelnode.master_call('storage', 'getinfo', self.name, decode=gravelrpc.bson)
        self.data.type = info['type']
        self.data.options = info['options']
        self.validate()

def get_box(name):
    box = Box(name, autocreate=True)
    if not box.exists:
        box._fetch_first()
    return box
