:orphan:
Token
==============

When?
---------------
When you're working with Kitsu.io API, you can encounter situation where
you want to make authenticated request to fetch some content etc.
To do so, you need a token

How to obtain a token?
-----------------------
Kitsu API documentation already cover this topic `here <https://kitsu.docs.apiary.io/#introduction/authentication>`_

| First you will need to make an account on `kitsu <https://kitsu.io>`_ website.
| After making an acconut, you'll need to make a post request to `https://kitsu.io/api/oauth/token`
| Kitsu supports 3 grant types, but for now only **Password** is implemented

Making POST request
-------------------

To make a post request we can run this simple python script

.. code:: python

    import requests

    url = "https://kitsu.io/api/oauth/token"


    #Make sure to replace username and password with your credentials
    data ={
        "grant_type": 'password',
        "username": '<username or email>',
        "password": '<password>' #Must be RFC3986 encoded
    }

    response = requests.post(url, data=data)
    print(response.text)

If the response was successful, this will print out

.. code:: python

    #From kitsu docs
    {
    access_token: 'abc123', #The token
    created_at: 1518235801,
    expires_in: 2591963, #Seconds until the access_token expires (30 days default)
    refresh_token: '123abc', #Token used to get a new access_token it expires
    scope: 'public',
    token_type: 'bearer'
    }


After obtaining a token
-------------------------
Now that we got a token, we can pass it to :class:`askitsu.Client` and make 
authenticated requests

.. code:: python

    import askitsu

    client = askitsu.Client("abc123...")

Next: :doc:`Simple examples <../examples>`
