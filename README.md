# UK Python News

[![Build Status](https://travis-ci.org/PyconUK/uk.python.org.svg?branch=master)](https://travis-ci.org/PyconUK/uk.python.org)

This is the code for uk.python.org.

## Building the site

This site uses [django-amber](https://github.com/inglesp/django-amber).
To install django-amber and other dependencies,
run `pip install -r requirements.txt`.
django-amber is only known to work with Python 3.5+.

To build the site, run `python manage.py buildsite`.
This pulls together all the components into a set of HTML files in `output/`.

Alternatively, if you run `python manage.py serve`,
django-amber will build the site,
serve the built site on port 8000,
and watch for changes.
