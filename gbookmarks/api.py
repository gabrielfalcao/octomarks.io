#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests


class GithubEndpoint(object):
    base_url = u'https://api.github.com'

    def __init__(self, token):
        self.token = token
        self.headers = {
            'authorization': 'token {0}'.format(token),
        }

    def full_url(self, path):
        return u"/".join([self.base_url, path.lstrip('/')])

    def retrieve(self, path, data=None):
        return requests.get(
            self.full_url(path),
            data=data or {},
            headers=self.headers,
        ).json()


class GithubResource(dict):
    endpoint = None

    def __init__(self, data, token=None):
        if isinstance(data, dict):
            super(GithubResource, self).__init__(data)

        else:
            token = data
            data = {
                'data': data,
                'id': id,
            }

        if 'token' in data:
            self.set_endpoint(data['token'])
        elif token:
            self.set_endpoint(token)

    def set_endpoint(self, token):
        self.endpoint = GithubEndpoint(token)

    def absorb(self, data):
        self.update(data)
        return self


class GithubRepository(GithubResource):
    pass


class GithubUser(GithubResource):
    def get_starred_repositories(self):
        path = '/users/{login}/starred'.format(**self)

        if 'starred_repositories' not in self:
            self['starred_repositories'] = self.endpoint.retrieve(path)

        return map(GithubRepository, self['starred_repositories'])

    def get_watched_repositories(self):
        path = '/users/{login}/watched'.format(**self)

        if 'watched_repositories' not in self:
            self['watched_repositories'] = self.endpoint.retrieve(path)

        return map(GithubRepository, self['watched_repositories'])

    @property
    def is_hollow(self):
        return len(self) > 3  # id, login, email, at least

    @classmethod
    def from_token(cls, token):
        user = cls(token)
        user.absorb(user.endpoint.retrieve('/user'))
        return user



    # user
    # {
    #   "login": "octocat",
    #   "id": 1,
    #   "avatar_url": "https://github.com/images/error/octocat_happy.gif",
    #   "gravatar_id": "somehexcode",
    #   "url": "https://api.github.com/users/octocat",
    #   "name": "monalisa octocat",
    #   "company": "GitHub",
    #   "blog": "https://github.com/blog",
    #   "location": "San Francisco",
    #   "email": "octocat@github.com",
    #   "hireable": false,
    #   "bio": "There once was...",
    #   "public_repos": 2,
    #   "public_gists": 1,
    #   "followers": 20,
    #   "following": 0,
    #   "html_url": "https://github.com/octocat",
    #   "created_at": "2008-01-14T04:33:35Z",
    #   "type": "User",
    #   "total_private_repos": 100,
    #   "owned_private_repos": 100,
    #   "private_gists": 81,
    #   "disk_usage": 10000,
    #   "collaborators": 8,
    #   "plan": {
    #     "name": "Medium",
    #     "space": 400,
    #     "collaborators": 10,
    #     "private_repos": 20
    #   }
    # }
