# Django-Highrise

This app provides integration between Django and Highrise, which is used to
provide CRM capabilities.

Currently this supports only two operations - adding a new person to Highrise,
and retrieving their feed - known as 'recordings' in the Highrise API.

It uses the (pyrise)[https://github.com/feedmagnet/pyrise] library.

## Why bother?

Django is a great web app framework, it's not such a good CRM tool. Sometimes
you need a little bit extra. Highrise is a simple CRM product from the guys
behind Basecamp. It allows you to keep tabs on contacts (amongst a lot of
other sales-related stuff), and has a great email integration feature. You can
read more about it [here](http://highrisehq.com/signup).

## Tell me more

This app simplifies the process of integrating with Highrise. It provides the
API hooks to allow you to push django user records into Highrise, and to read
a Highrise contact's feed (notes, emails, comments) back out. Where and when
you use these hooks is up to you. It could be at the point of user registration,
it could be through the Django admin site, it could even be from the command
line, run as a batch job overnight.

## Show me some code

    >>> from django_highrise import push_to_highrise, get_user_feed
    >>> person = push_to_highrise(user)
    >>> print len(person.emails)
    3
    >>> for m in get_user_feed(user):
    ...  print m.body
    ...
    this is a note
    this is a comment
    this is an email

