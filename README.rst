My Simple Dictionary Querer
===========================

.. image:: https://travis-ci.org/josuebrunel/mysdq.svg?branch=master
    :target: https://travis-ci.org/josuebrunel/mysdq
.. image:: https://coveralls.io/repos/github/josuebrunel/MySDQ/badge.svg?branch=master
    :target: https://coveralls.io/github/josuebrunel/MySDQ?branch=master
.. image:: http://pepy.tech/badge/mysdq
    :target: http://pepy.tech/count/mysdq


**MySDQ** is a simple and easy *dictionary querer* with an api close to the one of *Django QuerySet* 

It is meant to be used just to quickly play around with some JONS/Dict data.

It supports all operator from the *operator module* (Yes even the ones that won't work).

Think *Django QuerySet* when using it.


Installation
------------

.. code:: python

    pip install mysdq

Quickstart
----------

Data used in here can be found in `here <tests/users.json>`_

.. code:: python

   In [1]: import json
   In [2]: data = json.load(open('tests/users.json'))
   In [3]: from mysdq import DictQuerer
   In [4]: qs = DictQuerer(data)
   In [5]: qs.count() == 7
   Out[5]: True
   In [8]: qs.get(nickname='yloking')
   Out[8]:
   {'address': {'city': 'Paris',
     'name': 'rue du chatea',
     'num': 169,
     'zipcode': '75014'},
    'age': 25,
    'firstname': 'yosuke',
    'lastname': 'loking',
    'nickname': 'yloking',
    'profiles': [{'name': 'twitter',
      'url': 'https://twitter.com/yloking/',
      'username': 'yloking'},
     {'name': 'github',
      'url': 'https://github.com/yloking/',
      'username': 'yloking'},
     {'name': 'reddit',
      'url': 'https://reddit.com/yloking/',
      'username': 'yloking'}]}
   # Querying non matching entry
   In [9]: qs.get(lastname='young', age__le=20)
   # Querying an entry and requesting only 2 attributes
   In [11]: qs.filter(lastname='young', age__gt=20).values('nickname', 'age')
   Out[11]: [{'age': 35, 'nickname': 'kyoung'}]
   # Querying a sub key
   In [12]: qs.filter(address__zipcode='44000').values('nickname', 'age', 'address')
   Out[12]:
   [{'address': {'city': 'Nantes',
      'name': 'cheval blanc',
      'num': 12,
      'zipcode': '44000'},
     'age': 35,
     'nickname': 'kyoung'}]
   # Querying a item in a list
   In [13]: qs.filter(profiles__0__url__contains='kwame')
   Out[13]:
   [{'age': 24,
     'nickname': 'kkwame',
     'profiles': [{'name': 'twitter',
       'url': 'https://twitter.com/kkwame/',
       'username': 'kkwame'},
      {'name': 'github',
       'url': 'https://github.com/kkwame/',
       'username': 'kkwame'},
      {'name': 'reddit',
       'url': 'https://reddit.com/kkwame/',
       'username': 'kkwame'}]}]
   # Ordering by attribute
   In [14]: qs.order_by('age').values('nickname', 'age')
   Out[14]:
   [{'age': 15, 'nickname': 'tblack'},
    {'age': 24, 'nickname': 'kkwame'},
    {'age': 25, 'nickname': 'yloking'},
    {'age': 25, 'nickname': 'jrodriguez'},
    {'age': 28, 'nickname': 'jkouka'},
    {'age': 32, 'nickname': 'dmccrey'},
    {'age': 35, 'nickname': 'kyoung'}]
   # Grouping by attribute
   In [16]: res = qs.group_by('age')
   In [17]: assert len(res[25]) == 2
   In [18]: len(res[25])
   Out[18]: 2
   # Apply a function to an attribute
   In [19]: qs.apply(lambda x: x*2, 'age').values('nickname', 'age')
   Out[19]:
   [{'age': 30, 'nickname': 'tblack'},
    {'age': 48, 'nickname': 'kkwame'},
    {'age': 50, 'nickname': 'yloking'},
    {'age': 50, 'nickname': 'jrodriguez'},
    {'age': 56, 'nickname': 'jkouka'},
    {'age': 64, 'nickname': 'dmccrey'},
    {'age': 70, 'nickname': 'kyoung'}]


That's pretty much it.
