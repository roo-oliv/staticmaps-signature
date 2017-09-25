StaticMaps Signature
====================

Easily sign Google StaticMap API request urls with your API Key or Client ID.

Python 2.x and 3.x are supported.

.. |build| image:: https://travis-ci.org/allrod5/staticmaps-signature.svg?branch=master
    :target: https://travis-ci.org/allrod5/staticmaps-signature
    :scale: 100%
    :align: middle
.. |coverage| image:: https://coveralls.io/repos/github/allrod5/staticmaps-signature/badge.svg?branch=master
    :target: https://coveralls.io/github/allrod5/staticmaps-signature?branch=master
    :scale: 100%
    :align: middle

+---------+------------+
| |build| | |coverage| |
+---------+------------+

Usage
-----

Using StaticMaps Signature is pretty straight forward:

.. code:: python

    from staticmaps_signature import StaticMapURLSigner
    staticmap_url_signer = StaticMapURLSigner(
        public_key=YOUR_API_KEY, private_key=YOUR_SECRET)

    signed = staticmap_url_signer.sign_url(URL_TO_SIGN)

This will return your URL appended with
``'&key=YOUR_API_KEY&signature=UNIQUE_SIGNATURE'``.

If you wish to use your Cliend ID instead then just instantiate
:class:`StaticMapURLSigner` like this:

.. code:: python

    staticmap_url_signer = StaticMapURLSigner(
        client_id=YOUR_CLIENT_ID, private_key=YOUR_SECRET)

In case your URL already contains your API Key or Cliend ID instantiate
:class:`StaticMapURLSigner` with your shared secret only:

.. code:: python

    staticmap_url_signer = StaticMapURLSigner(private_key=YOUR_SECRET)

If you want just to append your API Key to the URL rather than signing it
just instantiate :class:`StaticMapURLSigner` with your key only:

.. code:: python

    staticmap_url_signer = StaticMapURLSigner(public_key=YOUR_API_KEY)

That's all there is for it.

This project is not maintained or supported by Google nor Google Maps.