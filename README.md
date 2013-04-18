# Octomarks

It's a bookmark app for github projects

## Deploying

1. Push to heroku and update the release hash

```console
make deploy
```

2. Run the migrations

```console
make migrate-forward
```

## Hacking

1. Install dependencies:

```console
pip install -r development.txt
```

2. Run the server

```console
make run
```

3. Run tests

```console
make unit functional
```


# TODO:

* Please show me the new libraries from people I already favorited
  libraries

* A button to import all the repos you already starred

* Show suggestions for projects you already liked

* allow people to add others peoples bookmarks as their owns (bookmark it too btn)
