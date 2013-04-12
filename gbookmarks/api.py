#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import requests_cache
import markdown2

requests_cache.install_cache()


class GithubEndpoint(object):
    base_url = u'https://api.github.com'

    def __init__(self, token):
        self.token = token
        self.headers = {
            'authorization': 'token {0}'.format(token),
            'X-GitHub-Media-Type: github.beta': 'github.beta'
        }

    def full_url(self, path):
        url = u"/".join([self.base_url, path.lstrip('/')])
        print url
        return url

    def retrieve(self, path, data=None):
        return self.json(requests.get(
            self.full_url(path),
            data=data or {},
            headers=self.headers,
        ))

    def save(self, path, data=None):
        return self.json(requests.put(
            self.full_url(path),
            headers=self.headers,
        ))

    def json(self, response):
        print response.url, response.headers,
        return response.json()


class Resource(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    @classmethod
    def from_token(cls, token):
        endpoint = GithubEndpoint(token)
        return cls(endpoint)


class GithubUser(Resource):
    @classmethod
    def fetch_info(cls, token):
        instance = cls.from_token(token)
        return instance.endpoint.retrieve('/user')


class GithubRepository(Resource):
    def get_readme(self, owner, project):
        reply = self.endpoint.retrieve(
            '/repos/{0}/{1}/readme'.format(owner, project))

        readme = reply['content'].decode(reply['encoding'])
        return markdown2.markdown(readme)
