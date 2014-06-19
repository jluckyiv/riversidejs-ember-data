# RiversideJS Ember Data demo

Follow the installation instructions below. Presentation slides file
is `slides.pdf`. PostgreSQL is needed to run the API server locally.

You can deploy this app to **Heroku**, but remember to add the
**Heroku-Postgres** addon and set `BUILDPACK_URL` config to
`https://github.com/heroku/heroku-buildpack-python`, as below:

```bash
heroku addons:add heroku-postgres:dev
heroku config:set BUILDPACK_URL= https://github.com/heroku/heroku-buildpack-python
```

## Installation

* `git clone` this repository
* `npm install`
* `bower install`

* `virtualenv env`
* `source env/bin/activate`
* `pip install -r requirements.txt`

## Running

* `ember server` for local ember testing
* `python api.py` for API server (remember to run `ember build` first)

## Running Tests

* `ember test`
* `ember test --server`

## Building

* `ember build`

For more information on using ember-cli, visit [http://iamstef.net/ember-cli/](http://iamstef.net/ember-cli/).
