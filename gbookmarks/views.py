#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import ejson as json

from flask import (
    Blueprint, request, session, render_template, redirect, g, flash, Response, url_for
)


from gbookmarks import settings
from gbookmarks.api import GithubUser, GithubEndpoint, GithubRepository
from gbookmarks.handy.decorators import requires_login
from flaskext.github import GithubAuth


github = GithubAuth(
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    session_key='user_id',
    # request_token_params={'scope': 'user,user:email,user:follow,repo,repo:status'}
)

mod = Blueprint('views', __name__)


def json_response(data):
    return Response(json.dumps(data), mimetype="text/json")


def error_json_response(message):
    return json_response({'success': False, 'error': {'message': message}})


class RepositoryURIInfo(object):
    project = None
    owner = None
    regex = re.compile(r'github.com/(?P<owner>[^/]+)/(?P<project>[^/]+)')

    def __init__(self, uri):
        self.uri = uri
        self.matched = self.regex.search(uri)
        if self.matched:
            self.owner = self.matched.group('owner')
            self.project = self.matched.group('project')

    def remount(self):
        return 'https://github.com/{0}/{1}'.format(self.owner, self.project)


@mod.before_request
def prepare_auth():
    g.user = None
    g.github = github


@mod.context_processor
def inject_basics():
    from gbookmarks.models import Tag

    def full_url_for(*args, **kw):
        return settings.absurl(url_for(*args, **kw))

    all_tags = Tag.all()
    all_ids = {t.id for t in all_tags}

    def pick(tag_id):
        for t in all_tags:
            if t.id == tag_id:
                return t

    def get_remaining_tags(exclude_tags):
        exclude_ids = {t.id for t in exclude_tags}
        return map(pick, all_ids.difference(exclude_ids))

    return dict(user=g.user, settings=settings, RepositoryURIInfo=RepositoryURIInfo, full_url_for=full_url_for, remaining_tags_for=get_remaining_tags)


@github.access_token_getter
def get_github_token(token=None):
    return session.get('github_token')


@mod.before_request
def prepare_user():
    from gbookmarks.models import User
    if 'github_user_data' in session:
        g.user = User.get_or_create_from_github_user(session['github_user_data'])


@mod.route('/.callback')
@github.authorized_handler
def github_callback(resp):
    from gbookmarks.models import User
    next_url = request.args.get('next') or '/'
    if resp is None:
        print (u'You denied the request to sign in.')
        return redirect(next_url)

    error = resp.get('error')

    if error:
        flash(error)
        print error
        return json.dumps(error)

    token = resp['access_token']
    session['github_token'] = token

    github_user_data = GithubUser.fetch_info(token)

    github_user_data['github_token'] = token

    g.user = User.get_or_create_from_github_user(github_user_data)
    session['github_user_data'] = github_user_data

    return redirect(next_url)


@mod.route('/save/<token>')
@requires_login
def save_bookmark(token):
    from gbookmarks.models import User
    uri = request.args.get('uri')
    should_redirect = request.args.get('should_redirect')

    info = RepositoryURIInfo(uri)

    uri = info.remount()
    if not info.matched:
        return render_template('invalid.html', uri=uri)

    user = User.find_one_by(gb_token=token)

    api = GithubEndpoint(user.github_token)
    tags = api.retrieve('/repos/{owner}/{repo}/languages'.format(
        owner=info.owner,
        repo=info.project
    ))
    if 'message' in tags:
        return render_template('invalid.html', uri=uri)

    bookmark = user.save_bookmark(uri)

    print api.save('/user/starred/{owner}/{repo}/'.format(
        owner=info.owner,
        repo=info.project
    )), tags

    # saving tags
    map(bookmark.add_tag, tags)

    # rendering
    return render_template('saved.html', uri=uri, user=user, repository_info=info, bookmark=bookmark, tags=tags, should_redirect=should_redirect)


@mod.route('/bookmarklet/gb_<token>.js')
def serve_bookmarklet(token):
    from gbookmarks.models import User
    user = User.find_one_by(gb_token=token)
    return Response(render_template('bookmarklet.js', user=user), mimetype="text/javascript")


@mod.route('/login')
def login():
    cb = settings.absurl('.callback')
    return github.authorize(callback_url=cb)


@mod.route('/<username>/bookmarks')
@requires_login
def bookmarks(username):
    api = GithubEndpoint(g.user.github_token)
    from gbookmarks.models import User
    user = User.find_one_by(username=username)

    bookmarks = None
    if not user:
        return render_template('invite.html', username=username, githubber=api.retrieve('/users/{0}'.format(username)))
    bookmarks = user.get_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks, user=user, is_self=(user == g.user))


@mod.route('/a/<bookmark_id>/tags', methods=['POST'])
@requires_login
def ajax_add_tags(bookmark_id):
    from gbookmarks.models import Bookmark
    if 'json' not in request.headers['content-type']:
        return json_response({'success': False, 'error': {'message': "Content type must be json"}})

    tag_names = request.json.get('tags', [])
    bk = Bookmark.find_one_by(id=bookmark_id, user_id=g.user.id)

    for tag in bk.tags:
        if tag.name not in tag_names:
            bk.remove_tag(tag)

    tags = [t[0].to_dict() for t in map(bk.add_tag, tag_names)]
    return json_response({'success': True, 'tags': tags})


@mod.route('/a/<bookmark_id>/delete', methods=['POST'])
@requires_login
def ajax_delete_bookmark(bookmark_id):
    from gbookmarks.models import Bookmark
    if 'json' not in request.headers['content-type']:
        return json_response({'success': False, 'error': {'message': "Content type must be json"}})

    bk = Bookmark.find_one_by(id=bookmark_id, user_id=g.user.id)
    if bk:
        bk.delete()
        return error_json_response('Bookmark {0} does not exist'.format(bookmark_id))
    return json_response({'success': True, 'deleted_object': bk.to_dict()})


@mod.route('/bookmark/<bookmark_id>/edit')
@requires_login
def edit_bookmark(bookmark_id):
    from gbookmarks.models import Bookmark

    repository = GithubRepository.from_token(g.user.github_token)
    bk = Bookmark.find_one_by(id=bookmark_id, user_id=g.user.id)
    info = RepositoryURIInfo(bk.url)

    readme = repository.get_readme(info.owner, info.project)

    return render_template('edit-bookmark.html',
                           bookmark=bk, info=info, readme=readme)


@mod.route('/logout')
def logout():
    if g.user and not g.user.github_token.startswith('disabled:'):
        g.user.github_token = 'disabled:{0}'.format(g.user.github_token)
        g.user.save()

    session.clear()
    return render_template('logout.html')


@mod.route("/")
@requires_login
def index():
    return render_template('index.html')
