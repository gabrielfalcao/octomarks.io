# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
from lettuce import step, world


Given = When = Then = And = step


@world.absorb
def get_tags_from_row(tags_row):
    list_of_tags = tags_row['tags'].split(",")
    return map(unicode.strip, list_of_tags)


@Given(u'the users:')
def the_users(step):
    all_tags = []
    world.users = []
    world.user_names = []
    for pos, row in enumerate(step.hashes):
        username = unicode(row['username'])
        theme = unicode(row['theme'])

        world.user_names.append(username)

        all_tags.extend(world.get_tags_from_row(row))

        world.users.append(world.User.create(
            username=unicode(username),
            email=u"{username}@{theme}.test.com".format(**row),
            gravatar_id="gravatar:{0}".format(pos),
            github_id=pos,
            github_token="{username}:token".format(**row),
            default_theme_name=unicode(theme),
        ))


@world.absorb
def tag_n_times(bookmark, number):
    for pos in range(number):
        while pos > len(world.all_tags):
            pos = pos - len(world.all_tags)

        bookmark.add_tag(world.all_tags[pos])


@world.absorb
def add_favorites_to_project(project, number):
    for pos in range(number):
        while pos > len(world.users):
            pos = pos - len(world.users)

        user = world.users[pos]
        user.save_bookmark(unicode(project['url']))


@world.absorb
def add_user_favorites(user, number):
    for pos in range(number):
        while pos > len(world.projects):
            pos = pos - len(world.projects)

        project = sorted(world.projects.values())[pos]
        user.save_bookmark(unicode(project['url']))


@world.absorb
def project_url(project_row):
    return "http://github.com/{owner}/{name}".format(**project_row)


@Given(u'the projects:')
def the_projects(step):
    world.projects = dict(map(
        lambda data: data.update({
            'owner': random.choice(world.user_names),
            "url": project_url(data)
        }) or (data["name"], data), step.hashes))


@When(u'an anonymous user goes to "([^"]*)"')
def an_anonymous_user_goes_to_group1(step, url_path):
    http = world.web_client()
    response = http.get(url_path)
    world.dom = world.get_dom(response.data)


@Then(u'he should see there are "([^"]*)" top bookmarks in this order:')
def he_should_see_there_are_group1_top_bookmarks_in_this_order(step, length):
    expected = int(length)
    world.dom.cssselect(".top-bookmark").should.have.length_of(expected)
    bookmarks = world.dom.cssselect(".top-bookmark .project-name a")
    owners = world.dom.cssselect(".top-bookmark .project-owner a")
    totals = world.dom.cssselect(".top-bookmark .total span")

    for bookmark, expectation in zip(bookmarks, step.hashes):
        bookmark.text.should.contain(expectation["name"])

    for owner, expectation in zip(owners, step.hashes):
        owner.text.should.contain(expectation["owner"])

    for total, expectation in zip(totals, step.hashes):
        total.text.should.match(r'\d+')
        total.text.strip().should.equal(expectation['favorites'])


@And(u'that the project "([^"]*)" got `(\d+)` favorites?')
def that_the_project_X_got_N_favorites(step, project, favorites_n):
    project = world.projects[project]
    world.add_favorites_to_project(project, int(favorites_n))


@And(u'that the user "([^"]*)" favorited `(\d+)` projects?')
def that_the_user_group1_favorited_5_projects(step, username, favorited_n):
    user = world.User.find_one_by(username=username)
    user.should.be.a(world.User)
    world.add_user_favorites(user, int(favorited_n))


@Then(u'he should see there are "([^"]*)" top users in this order:')
def he_should_see_there_are_group1_top_users_in_this_order(step, length):
    expected = int(length)
    world.dom.cssselect(".top-user").should.have.length_of(expected)
    users = world.dom.cssselect(".top-user .user-name a")
    totals = world.dom.cssselect(".top-user .total span")

    for user, expectation in zip(users, step.hashes):
        user.text.should.contain(expectation["name"])

    for total, expectation in zip(totals, step.hashes):
        total.text.should.match(r'\d+')
        total.text.strip().should.equal(expectation['favorited'])
