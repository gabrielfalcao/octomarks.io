#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


class RepoInfo(object):
    project = None
    owner = None
    matched = None
    regexes = [
        re.compile(r'github[.]com/(?P<owner>[^/]+)/(?P<project>[^/]+)'),
        re.compile(r'(?P<owner>[\w_-]+)[.]github.(?:io|com)/(?P<project>[^/]+)'),
    ]

    def __init__(self, uri):
        self.uri = uri

        for matched in filter(bool, [r.search(uri) for r in self.regexes]):
            self.matched = matched
            self.owner = matched.group('owner')
            self.project = matched.group('project')
            break

    def __nonzero__(self):
        return self.matched is not None

    def remount(self):
        return 'http://github.com/{0}/{1}'.format(self.owner, self.project)

    def to_dict(self):
        return dict(
            owner=self.owner,
            project=self.project,
            url=self.remount()
        )
