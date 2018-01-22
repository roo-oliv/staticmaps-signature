import pytest

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from staticmaps_signature import StaticMapURLSigner

CLIENT_ID = "Zy4aSIA1Q7KXFsGy4ulx1qS0-PQXefghOBcPH2E"
PUBLIC_KEY = "Zy4aSIA1Q7KXFsGy4ulx1qS0-PQXefghOBcPH2E"
PRIVATE_KEY = "cwAPISuAyZSrGwXG-qzjMLPPvRE="


@pytest.fixture('function')
def logging_stub(mocker):
    return mocker.patch("staticmaps_signature.signature.logging")


@pytest.mark.usefixtures('logging_stub')
class TestStaticMapURLSigner(object):
    def test_init(self):
        StaticMapURLSigner()
        StaticMapURLSigner(client_id=CLIENT_ID)
        StaticMapURLSigner(public_key=PUBLIC_KEY)
        StaticMapURLSigner(private_key=PRIVATE_KEY)
        StaticMapURLSigner(client_id=CLIENT_ID, private_key=PRIVATE_KEY)
        StaticMapURLSigner(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)
        StaticMapURLSigner(client_id=CLIENT_ID, public_key=PUBLIC_KEY,
                           private_key=PRIVATE_KEY)

    def test_signature(self):
        # given
        request_url = (
            "https://maps.googleapis.com/maps/api/staticmap"
            "?center=-23.5509518,-46.6921805&markers=-23.5509518,-46.6921805"
            "&zoom=15&size=300x200&maptype=roadmap")
        request_url_with_key = (
            "https://maps.googleapis.com/maps/api/staticmap?key=PUBLIC_KEY"
            "&center=-23.5509518,-46.6921805&markers=-23.5509518,-46.6921805"
            "&zoom=15&size=300x200&maptype=roadmap")
        bad_endpoint_scheme_url = (
            "http://maps.googleapis.com/maps/api/staticmap"
            "?center=-23.5509518,-46.6921805&markers=-23.5509518,-46.6921805"
            "&zoom=15&size=300x200&maptype=roadmap")
        bad_endpoint_netloc_url = (
            "https://maps.google.com/maps/api/staticmap"
            "?center=-23.5509518,-46.6921805&markers=-23.5509518,-46.6921805"
            "&zoom=15&size=300x200&maptype=roadmap")
        bad_endpoint_path_url = (
            "https://maps.googleapis.com/staticmap"
            "?center=-23.5509518,-46.6921805&markers=-23.5509518,-46.6921805"
            "&zoom=15&size=300x200&maptype=roadmap")
        client_id_signer = StaticMapURLSigner(
            client_id=CLIENT_ID, private_key=PRIVATE_KEY)
        public_key_signer = StaticMapURLSigner(
            public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)
        public_key_appender = StaticMapURLSigner(public_key=PUBLIC_KEY)
        generic_signer = StaticMapURLSigner(private_key=PRIVATE_KEY)
        skip_verification_signer = StaticMapURLSigner(
            client_id=CLIENT_ID, private_key=PRIVATE_KEY,
            verify_endpoint=False)

        # when
        client_id_signed = client_id_signer.sign_url(request_url)
        client_id_signed_parsed = urlparse.urlparse(client_id_signed)
        client_id_signed_query = urlparse.parse_qs(
            client_id_signed_parsed.query)
        public_key_signed = public_key_signer.sign_url(request_url)
        public_key_signed_parsed = urlparse.urlparse(public_key_signed)
        public_key_signed_query = urlparse.parse_qs(
            public_key_signed_parsed.query)
        public_key_appended = public_key_appender.sign_url(request_url)
        public_key_appended_parsed = urlparse.urlparse(public_key_appended)
        public_key_appended_query = urlparse.parse_qs(
            public_key_appended_parsed.query)
        generic_signed = generic_signer.sign_url(request_url_with_key)
        generic_signed_parsed = urlparse.urlparse(generic_signed)
        generic_signed_query = urlparse.parse_qs(generic_signed_parsed.query)
        corrected_scheme = client_id_signer.sign_url(bad_endpoint_scheme_url)
        corrected_netloc = client_id_signer.sign_url(bad_endpoint_netloc_url)
        corrected_path = client_id_signer.sign_url(bad_endpoint_path_url)
        uncorrected_netloc = skip_verification_signer.sign_url(
            bad_endpoint_netloc_url)

        # then
        assert client_id_signed_query.get('client_id')[0] == CLIENT_ID
        assert client_id_signed_query.get('signature')[0] is not None
        assert public_key_signed_query.get('key')[0] == PUBLIC_KEY
        assert public_key_signed_query.get('signature')[0] is not None
        assert public_key_appended_query.get('key')[0] == CLIENT_ID
        assert generic_signed_query.get('signature')[0] is not None
        assert (urlparse.urlparse(corrected_scheme).scheme
                == client_id_signer.staticmap_api_endpoint.scheme)
        assert (urlparse.urlparse(corrected_netloc).netloc
                == client_id_signer.staticmap_api_endpoint.netloc)
        assert (urlparse.urlparse(corrected_path).path
                == client_id_signer.staticmap_api_endpoint.path)
        assert (urlparse.urlparse(uncorrected_netloc).netloc
                == urlparse.urlparse(bad_endpoint_netloc_url).netloc)
