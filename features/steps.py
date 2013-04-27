# -*- coding: utf-8 -*-
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
    for pos, row in enumerate(step.hashes):
        username = row['username']
        theme = row['theme']
        all_tags.extend(world.get_tags_from_row(row))
        world.users.append(world.User.create(
            username=username,
            email="{username}@{theme}.test.com".format(**row),
            gravatar_id="gravatar:{0}".format(pos),
            github_id=pos,
            github_token="{username}:token".format(**row),
            default_theme_name=theme,
        ))


@world.absorb
def tag_n_times(bookmark, number):
    for pos in range(number):
        while pos > len(world.all_tags):
            pos = pos - len(world.all_tags)

        bookmark.add_tag(world.all_tags[pos])


@world.absorb
def project_url(project_row):
    return "http://github.com/{owner}/{name}".format(**project_row)


@Given(u'the projects:')
def the_projects(step):
    world.bookmarks = []
    for row in step.hashes:
        user = random.choice(world.users)
        tags = world.get_tags_from_row(row)
        bkm = world.Bookmark.create(
            url=world.project_url(row),
            user_id=user.id
        )
        world.bookmarks.append(bkm)
        map(bkm.add_tag, tags)


@When(u'an anonymous user goes to "([^"]*)"')
def an_anonymous_user_goes_to_group1(step, group1):
    http = world.web_client()
    response = http.get("/ranking")
    world.dom = world.get_dom(response.data)


@Then(u'he should see there are "([^"]*)" top bookmarks in this order:')
def he_should_see_there_are_group1_top_bookmarks_in_this_order(step, group1):
    world.dom.cssselect(".top-bookmark").should.have.length_of(5)
