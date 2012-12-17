# -*- coding: utf-8 -*-
#
#  Copyright (c) 2010—2012 Andrey Mikhailenko and contributors
#
#  This file is part of Argh.
#
#  Argh is free software under terms of the GNU Lesser
#  General Public License version 3 (LGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#
"""
Interaction
===========
"""
from argh.six import text_type, PY3


__all__ = ['confirm']


def _input(prompt):
    # this function can be mocked up in tests
    if PY3:
        return input(prompt)
    else:
        return raw_input(prompt)


def safe_input(prompt):
    "Prompts user for input. Correctly handles prompt message encoding."

    if PY3:
        if not isinstance(prompt, text_type):
            # Python 3.x: bytes →  unicode
            prompt = prompt.decode()
    else:
        if isinstance(prompt, text_type):
            # Python 2.x: unicode →  bytes
            prompt = prompt.encode('utf-8')

    return _input(prompt)


def confirm(action, default=None, skip=False):
    """A shortcut for typical confirmation prompt.

    :param action:

        a string describing the action, e.g. "Apply changes". A question mark
        will be appended.

    :param default:

        `bool` or `None`. Determines what happens when user hits :kbd:`Enter`
        without typing in a choice. If `True`, default choice is "yes". If
        `False`, it is "no". If `None` the prompt keeps reappearing until user
        types in a choice (not necessarily acceptable) or until the number of
        iteration reaches the limit. Default is `None`.

    :param skip:

        `bool`; if `True`, no interactive prompt is used and default choice is
        returned (useful for batch mode). Default is `False`.

    Usage::

        @arg('key')
        @arg('--silent', help='do not prompt, always give default answers')
        def delete(args):
            item = db.get(Item, args.key)
            if confirm('Delete '+item.title, default=True, skip=args.silent):
                item.delete()
                print('Item deleted.')
            else:
                print('Operation cancelled.')

    Returns `None` on `KeyboardInterrupt` event.
    """
    MAX_ITERATIONS = 3
    if skip:
        return default
    else:
        defaults = {
            None: ('y','n'),
            True: ('Y','n'),
            False: ('y','N'),
        }
        y, n = defaults[default]
        prompt = text_type('{action}? ({y}/{n})').format(**locals())
        choice = None
        try:
            if default is None:
                cnt = 1
                while not choice and cnt < MAX_ITERATIONS:
                    choice = safe_input(prompt)
                    cnt += 1
            else:
                choice = safe_input(prompt)
        except KeyboardInterrupt:
            return None
    if choice in ('yes', 'y', 'Y'):
        return True
    if choice in ('no', 'n', 'N'):
        return False
    if default is not None:
        return default
    return None
