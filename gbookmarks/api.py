#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ejson
import logging
import requests
import markdown2


class GithubEndpoint(object):
    base_url = u'https://api.github.com'

    def __init__(self, token, cache=None):
        self.history = []
        self.token = token
        self.cache = cache
        self.headers = {
            'authorization': 'token {0}'.format(token),
            'X-GitHub-Media-Type: github.beta': 'github.beta'
        }
        self.log = logging.getLogger('gbookmarks.api')

    @property
    def last_response(self):
        return self.history and self.history[-1]

    def full_url(self, path):
        url = u"/".join([self.base_url, path.lstrip('/')])
        print url
        return url

    def get_from_cache(self, url, headers, data=None):
        from gbookmarks.models import HttpCache

        cached = HttpCache.find_one_by(url=url)
        if not cached:
            return {}

        data = cached.to_dict()
        data['request_data'] = data
        data['request_headers'] = headers
        return data

    def get_from_web(self, path, headers, data=None):
        url = self.full_url(path)
        data = data or {}

        request = {
            'url': url,
            'data': data,
            'headers': headers,
        }
        response = {}
        error = None
        try:
            response = requests.get(**request)
        except Exception as e:
            error = e
            self.log.exception("Failed to retrieve `%s` with data %s", path, repr(data))

        return {
            'url': url,
            'request_headers': headers,
            'request_data': data,
            'response_headers': dict(response.headers),
            'error': error,
            'response_data': response.content,
            'cached': False,
            'status_code': response.status_code,
        }

    def retrieve(self, path, data=None):
        headers = self.headers
        response = self.get_from_cache(path, headers, data)
        if not response:
            response = self.get_from_web(path, headers, data)

        self.history.append(response)
        return self.json(response)

    def save(self, path, data=None):
        return self.json(requests.put(
            self.full_url(path),
            headers=self.headers,
        ))

    def json(self, response):
        return ejson.loads(response['response_data'])


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

    def get_languages(self, owner, project):
        return self.endpoint.retrieve(
            '/repos/{0}/{1}/languages'.format(owner, project))

    def get_owner(self, owner):
        response = self.endpoint.retrieve(
            '/users/{0}'.format(owner))

        return response

    def get(self, owner, project):
        return self.endpoint.retrieve('/repos/{0}/{1}'.format(owner, project))
