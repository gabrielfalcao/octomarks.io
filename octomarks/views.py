#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ejson as json
from functools import partial
from flask import (
    Blueprint, request, session, render_template, redirect, g, flash, Response, url_for
)


from octomarks import settings
from octomarks.api import GithubUser, GithubEndpoint, GithubRepository
from octomarks.core import RepoInfo, mailtoify, full_url_for
from octomarks.handy.decorators import requires_login
from octomarks.handy.functions import user_is_authenticated
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
    from octomarks.models import User
    if 'github_user_data' not in session:
        g.user = None
    else:
        g.user = User.get_or_create_from_github_user(session['github_user_data'])

    g.github = github


@mod.context_processor
def inject_basics():
    return dict(
        user=g.user,
        default_theme_url=settings.absurl('/static/themes/tango.css'),
        settings=settings,
        RepoInfo=RepoInfo,
        full_url_for=full_url_for,
        mailtoify=mailtoify,
    )


def tag_context(**dictionary):
    from octomarks.models import Tag

    def get_remaining_tags(exclude_tags):
        all_tags = Tag.all()
        all_ids = {t.id for t in all_tags}

        def pick(tag_id):
            for t in all_tags:
                if t.id == tag_id:
                    return t

        exclude_ids = {t.id for t in exclude_tags}
        return map(pick, all_ids.difference(exclude_ids))

    dictionary.update({
        'remaining_tags_for': get_remaining_tags,
    })
    return dictionary


@github.access_token_getter
def get_github_token(token=None):
    return session.get('github_token')


@mod.route('/.callback')
@github.authorized_handler
def github_callback(resp):
    from octomarks.models import User
    next_url = request.args.get('next') or '/'
    if resp is None:
        print (u'You denied the request to sign in.')
        return redirect(next_url)

    error = resp.get('error')

    if error:
        flash(error)
        return json.dumps(error)

    token = resp['access_token']
    session['github_token'] = token

    github_user_data = GithubUser.fetch_info(token)

    github_user_data['github_token'] = token

    g.user = User.get_or_create_from_github_user(github_user_data)
    session['github_user_data'] = github_user_data

    return redirect(next_url)


@mod.route('/save/<token>')
def save_bookmark(token):
    from octomarks.models import User
    original_uri = request.args.get('uri')
    should_redirect = request.args.get('should_redirect')

    user = User.find_one_by(gb_token=token)

    info = RepoInfo(original_uri)

    owner = info.owner
    project = info.project

    uri = info.remount()

    if not info.matched:
        if should_redirect:
            return redirect(uri)

        return render_template('invalid.html', uri=uri)

    if should_redirect:
        user.save_bookmark(original_uri)
        return redirect(uri)

    context = get_repository_data(owner, project, user.github_token)
    repository_exists = bool(context.get('success'))

    bookmark = user.save_bookmark(original_uri)

    if not repository_exists:
        return render_template('index.html', uri=uri, error="Invalid github project")

    owner_data = context['owner']
    if not owner_data or 'message' in owner_data:
        return render_template('saved.error.html',
                               info=info, bookmark=bookmark)

    return redirect(url_for('.show_bookmark', owner=owner, project=project))


def get_repository_data(owner_name, project, token):
    repository_fetcher = GithubRepository(GithubEndpoint(token, public=True))

    readme = ''
    index = []
    repository = repository_fetcher.get(owner_name, project)
    owner = {}
    tags = []

    if repository and 'message' not in repository:
        readme, index = repository_fetcher.get_readme(owner_name, project)
        tags = repository_fetcher.get_languages(owner_name, project)
        owner = repository_fetcher.get_owner(owner_name)

    return {
        'success': bool(readme),
        'documentation': readme,
        'documentation_index': index,
        'project': project,
        'repository': repository,
        'owner': owner,
        'owner_name': owner_name,
        'project': project,
        'tags': tags,
    }


def get_token_with_fallback_for(username):
    from octomarks.models import User
    if g.user:
        token = g.user.github_token
    else:
        user = User.find_one_by(username=username)
        token = user and user.github_token

    return token


@mod.route('/<owner>/<project>')
def show_bookmark(owner, project):
    token = get_token_with_fallback_for(owner)
    if not token:
        return render_template(
            'invite.anon.html',
            username=owner)

    context = get_repository_data(owner, project, token)
    if not context['success']:
        return Response(render_template('bookmark-404.html', **context), status=404)
    return render_template('show-bookmark.html', **context)


@mod.route('/<owner>/<project>/docs/<path:path>')
def show_documentation(owner, project, path):
    if not path.endswith(".md"):
        return Response(status=404)

    token = get_token_with_fallback_for(owner)
    repository_fetcher = GithubRepository(GithubEndpoint(token, public=True))

    if not token:
        return render_template(
            'invite.anon.html',
            username=owner)

    context = get_repository_data(owner, project, token)
    doc, doc_index = repository_fetcher.retrieve_docs(owner, project, path)
    context.update({
        'documentation': doc,
        'documentation_index': doc_index,
    })

    if not context['success']:
        return Response(render_template('bookmark-404.html', **context), status=404)
    return render_template('show-bookmark.html', **context)


@mod.route('/bookmarklet/gb_<token>.js')
def serve_bookmarklet(token):
    from octomarks.models import User
    user = User.find_one_by(gb_token=token)
    return Response(render_template('bookmarklet.js', user=user), mimetype="text/javascript")


@mod.route('/login')
def login():
    cb = settings.absurl('.callback')
    return github.authorize(callback_url=cb)


@mod.route('/<username>')
@requires_login
def bookmarks(username):
    api = GithubEndpoint(g.user.github_token)
    from octomarks.models import User
    user = User.find_one_by(username=username)

    bookmarks = None
    if not user:
        return render_template(
            'invite.html',
            user=user,
            is_self=(user == g.user),
            username=username,
            githubber=api.retrieve('/users/{0}'.format(username)))

    bookmarks = user.get_bookmarks()
    return render_template('bookmarks.html', **tag_context(
        bookmarks=bookmarks,
        user=user,
        is_self=(user == g.user)))


@mod.route('/a/<bookmark_id>/tags', methods=['POST'])
@requires_login
def ajax_add_tags(bookmark_id):
    from octomarks.models import Bookmark
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
    from octomarks.models import Bookmark
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
    from octomarks.models import Bookmark

    repository = GithubRepository.from_token(g.user.github_token)
    bk = Bookmark.find_one_by(id=bookmark_id, user_id=g.user.id)
    info = RepoInfo(bk.url)

    readme, index = repository.get_readme(info.owner, info.project)

    return render_template('edit-bookmark.html',
                           bookmark=bk, info=info, readme=readme, readme_index=index)


@mod.route('/.cleanup')
def cleanup():
    from octomarks.models import Tag, BookmarkTags, db
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
    g.user = None
    return render_template('logout.html')


@mod.route("/")
def index():
    if user_is_authenticated():
        return redirect(url_for('.bookmarks', username=g.user.username))

    return redirect(url_for('.ranking'))


@mod.route("/ranking")
def ranking():
    from octomarks.models import Bookmark
    ranking = Bookmark.get_most_bookmarked()
    return Response(render_template('ranking.html', ranking=ranking), headers={
        'Cache-Control': 'public, max-age=31536000'
    })


@mod.route("/explore")
def explore():
    return render_template('explore.html')


@mod.route("/500")
def five00():
    return render_template('500.html')


@mod.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
