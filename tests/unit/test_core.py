#!/usr/bin/env python
# -*- coding: utf-8 -*-
from octomarks.core import RepoInfo


def test_repository_info_matches_project():
    "RepoInfo should match a github project url"

    info = RepoInfo('http://github.com/gabrielfalcao/sure')

    info.matched.should_not.be.none
    info.owner.should.equal('gabrielfalcao')
    info.project.should.equal('sure')


def test_repository_info_matches_page():
    "RepoInfo should match a github page url"

    info = RepoInfo('http://gabrielfalcao.github.io/sure')

    info.matched.should_not.be.none
    info.owner.should.equal('gabrielfalcao')
    info.project.should.equal('sure')


def test_repository_info_matches_project_without_http():
    "RepoInfo should match a github project url"

    info = RepoInfo('github.com/gabrielfalcao/lettuce')

    info.matched.should_not.be.none
    info.owner.should.equal('gabrielfalcao')
    info.project.should.equal('lettuce')


def test_repository_info_matches_page_without_http():
    "RepoInfo should match a github page url"

    info = RepoInfo('gabrielfalcao.github.com/lettuce')

    info.matched.should_not.be.none
    info.owner.should.equal('gabrielfalcao')
    info.project.should.equal('lettuce')
