.. _usage:

Usage
=====

Using StaticMaps Signature is pretty straight forward::

    from staticmaps_signature import StaticMapURLSigner
    staticmap_url_signer = StaticMapURLSigner(
        public_key=YOUR_API_KEY, private_key=YOUR_SECRET)

    signed = staticmap_url_signer.sign_url(URL_TO_SIGN)

