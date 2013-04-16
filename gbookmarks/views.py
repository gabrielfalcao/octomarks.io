#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ejson as json
from functools import partial
from flask import (
    Blueprint, request, session, render_template, redirect, g, flash, Response, url_for
)


from gbookmarks import settings
from gbookmarks.api import GithubUser, GithubEndpoint, GithubRepository
from gbookmarks.core import RepoInfo
from gbookmarks.handy.decorators import requires_login
from flaskext.github import GithubAuth


github = GithubAuth(
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    session_key='user_id',
    # request_token_params={'scope': 'user,user:email,user:follow,repo,repo:status'}
)

mod = Blueprint('views', __name__)


def json_response(data, status=200):
    return Response(json.dumps(data), mimetype="text/json", status=str(status))


def error_json_response(message):
    return json_response({'success': False, 'error': {'message': message}})


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

    return dict(user=g.user, settings=settings, RepoInfo=RepoInfo, full_url_for=full_url_for, remaining_tags_for=get_remaining_tags)


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

    info = RepoInfo(uri)

    owner = info.owner
    project = info.project

    uri = info.remount()

    if not info.matched:
        if should_redirect:
            return redirect(uri)

        return render_template('invalid.html', uri=uri)

    context = get_repository_data(owner, project)
    repository_exists = bool(context.get('success'))

    if not repository_exists:
        return render_template('index.html', uri=uri, error="Invalid github project")

    user = User.find_one_by(gb_token=token)

    bookmark = user.save_bookmark(uri)

    if should_redirect:
        return redirect(uri)
    owner_data = context['owner']
    if not owner_data or 'message' in owner_data:
        return render_template('saved.error.html',
                               info=info, bookmark=bookmark)

    return redirect(url_for('.show_bookmark', owner=owner, project=project))


def get_repository_data(owner_name, project):
    repository_fetcher = GithubRepository(GithubEndpoint(g.user.github_token, public=True))

    readme = ''
    repository = repository_fetcher.get(owner_name, project)
    owner = {}
    tags = []

    if repository and 'message' not in repository:
        readme = repository_fetcher.get_readme(owner_name, project)
        tags = repository_fetcher.get_languages(owner_name, project)
        owner = repository_fetcher.get_owner(owner_name)

    return {
        'success': bool(readme),
        'readme': readme,
        'project': project,
        'repository': repository,
        'owner': owner,
        'project': project,
        'tags': tags,
    }


@mod.route('/<owner>/<project>')
@requires_login
def show_bookmark(owner, project):

    context = get_repository_data(owner, project)
    return render_template('show-bookmark.html', **context)


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
    info = RepoInfo(bk.url)

    readme = repository.get_readme(info.owner, info.project)

    return render_template('edit-bookmark.html',
                           bookmark=bk, info=info, readme=readme)


@mod.route('/.cleanup')
def cleanup():
    from gbookmarks.models import Tag, BookmarkTags, db
    conn = Tag.get_connection()

    res = conn.execute(Tag.table.select().where(Tag.table.c.id.notin_(db.select([BookmarkTags.table.c.tag_id]))))

    Tags = partial(Tag.from_result_proxy, res)

    deleted_tags = []
    for tag in map(Tags, res.fetchall()):
        deleted_tags.append(tag.to_json())
        tag.delete()

    return json_response({'deleted_tags': deleted_tags})


@mod.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')


@mod.route("/")
def index():
    from gbookmarks.models import Bookmark
    if g.user:
        return render_template('index.html')
    else:
        ranking = Bookmark.get_most_bookmarked()
        return render_template('index.anon.html', ranking=ranking)
