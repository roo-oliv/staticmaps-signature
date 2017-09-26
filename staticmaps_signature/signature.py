"""
Adapted from: https://github.com/googlemaps/url-signing
Author: Rodrigo Martins de Oliveira (github.com/allrod5)
"""
import hashlib
import hmac
import base64

import logging

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


class StaticMapURLSigner(object):
    def __init__(
            self, client_id=None, public_key=None, private_key=None,
            verify_endpoint=True):
        # type: (str, str, str, bool) -> None
        """
        StaticMap URL Signer offers the ability to generate a Google
        StaticMap API request URL appended with an API Key or Client ID
        and signed with a digital signature.

        When only the `public_key` is set, then no signature will be
        generated and only a `&key` parameter will be appended when
        signing an URL.

        When only the `private_key` is set, it is assumed that any URL
        to sign will already contain the `&key` or `&client_id` query
        parameter.

        Parameters `client_id` and `public_key` are mutually exclusive
        and must not be both set. When parameter `client_id` is set,
        then setting also parameter `private_key` is mandatory.

        Args:
        client_id       - StaticMap Client ID
        public_key      - StaticMap API Key
        private_key     - StaticMap shared secret
        verify_endpoint - Flag to verify the URL endpoint
        """
        self.client_id = client_id
        self.public_key = public_key
        self.private_key = private_key
        self.verify_endpoint = verify_endpoint
        self.staticmap_api_endpoint = urlparse.urlparse(
            "https://maps.googleapis.com/maps/api/staticmap")
        if self.client_id is not None:
            if self.public_key is not None:
                raise ValueError(
                    "Parameters `client_id` and `public_key` are"
                    " mutually exclusive")
            if self.private_key is None:
                raise ValueError(
                    "Parameter `private_key` is required when"
                    " using `client_id`")
        elif self.public_key is None and self.private_key is None:
            raise ValueError(
                "At least one of `public_key` or `private_key` must be set")

    def sign_url(self, input_url):
        # type: (str) -> str
        """
        Generates a signed URL from the `input_url` if
        :class:`StaticMapURLSigner` is provided with a private key,
        otherwise just the public key will be appended to the URL.

        Usage:
        >>> from staticmaps_signature import StaticMapURLSigner
        >>> staticmap_url_signer = StaticMapURLSigner(
        >>>     public_key='PUBLIC_KEY', private_key='PRIVATE_KEY')
        >>> signed_url = staticmap_url_signer.sign_url('URL')

        Args:
        input_url - StaticMap API request URL

        Returns:
        The request URL appended by an API Key or Client ID and a
        signature (if `private_key` was provided to
        :class:`StaticMapURLSigner`)
        """
        if not input_url:
            raise ValueError("`input_url` cannot be None")

        scheme, netloc, path, _, query, _ = urlparse.urlparse(input_url)

        if self.verify_endpoint:
            if scheme != self.staticmap_api_endpoint.scheme:
                logging.warning(
                    "URL scheme `%s` remapped to `%s`", scheme,
                    self.staticmap_api_endpoint.scheme)
                scheme = self.staticmap_api_endpoint.scheme
            if netloc != self.staticmap_api_endpoint.netloc:
                logging.warning(
                    "URL netloc `%s` remapped to `%s`", netloc,
                    self.staticmap_api_endpoint.netloc)
                netloc = self.staticmap_api_endpoint.netloc
            if path != self.staticmap_api_endpoint.path:
                logging.warning(
                    "URL path `%s` remapped to `%s`", path,
                    self.staticmap_api_endpoint.path)
                path = self.staticmap_api_endpoint.path

        if self.client_id is not None:
            query_string = "client_id={client_id}&{query_params}".format(
                client_id=self.client_id, query_params=query)
        elif self.public_key is not None:
            query_string = "key={key}&{query_params}".format(
                key=self.public_key, query_params=query)
        else:
            query_string = "{query_params}".format(query_params=query)

        url_model = "{scheme}://{netloc}{path}?{query_string}"

        if not self.private_key:
            return url_model.format(
                scheme=scheme, netloc=netloc, path=path,
                query_string=query_string)

        # We only need to sign the path+query part of the string
        url_to_sign = path + "?" + query_string

        # Decode the private key into its binary format
        # We need to decode the URL-encoded private key
        decoded_key = base64.urlsafe_b64decode(self.private_key)

        # Create a signature using the private key and the URL-encoded
        # string using HMAC SHA1. This signature will be binary.
        signature = hmac.new(
            decoded_key, str.encode(url_to_sign), hashlib.sha1)

        # Encode the binary signature into base64 for use within a URL
        encoded_signature = base64.urlsafe_b64encode(signature.digest())

        query_string += "&signature={signature}".format(
            signature=encoded_signature.decode())

        # Return signed URL
        return url_model.format(
            scheme=scheme, netloc=netloc, path=path, query_string=query_string)
