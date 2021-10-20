import logging
import sys
from urllib import parse

import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt

from utils.error import HTTP_ERROR_CODES, HttpClientConnectionError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Configure to now show the tracback while raising error
sys.tracebacklimit = 0


class HttpClientConnection:

    def __init__(self, api_token, base_url, max_retries, timeout):
        self.base_url = base_url
        self.api_token = api_token
        self.max_retries = max_retries
        self.timeout = timeout
        self.session = requests.Session()

    def _get_headers(self):
        logger.debug('Updating headers')
        return {
            'Content-Type': 'application/json',
            'Authorization': self.api_token,
        }

    @retry(stop=stop_after_attempt(3),
           retry=(retry_if_exception_type(requests.exceptions.ConnectionError)
                  | retry_if_exception_type(requests.exceptions.Timeout)
                  | retry_if_exception_type(requests.exceptions.ConnectTimeout)))
    def _make_request(self, http_method, relative_endpoint, data=None):
        """
        Generic function to make requests for different HTTP methods.
        :param http_method: HTTP method for the request
        :param relative_endpoint:
        :param data: Payload to be send with the request
        """
        url = parse.urljoin(self.base_url, relative_endpoint)
        self.session.headers.update(self._get_headers())

        logger.info(f"Requesting url: {url}")

        try:
            response = self.session.request(
                method=http_method,
                url=url,
                timeout=self.timeout,
                json=data
            )
            logger.debug(f"Response: {response.text}")
            json_response = response.json()

            # Handle API errors
            if isinstance(json_response, dict):
                errors = json_response.get('errors', [])
                if errors:
                    for error in errors:
                        logger.error(error.get('message', ''))
                    raise HttpClientConnectionError(errors)

            # Raise the errors so that we can handle them
            # according to error type
            response.raise_for_status()

        except requests.exceptions.HTTPError as e:
            # Handle HTTP errors
            error_code = response.status_code
            if error_code in HTTP_ERROR_CODES:
                logger.info(HTTP_ERROR_CODES[error_code])
                raise HttpClientConnectionError(e)

        except requests.exceptions.TooManyRedirects as e:
            logger.error(e)
            raise HttpClientConnectionError("Too many redirects. Try a new URL")

        except (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ConnectionError
        ) as e:
            # Handle errors which could be fixed with retrying connection
            logger.error(e)
            # Raise the error here as tenacity expects these errors for
            # retrying the request
            raise

        except requests.exceptions.RequestException as e:
            logger.error(e)
            raise HttpClientConnectionError(e) from None

        else:
            return json_response

    def get(self, relative_endpoint, data=None):
        """
        Makes a HTTP GET request
        """
        logger.info(f'Making GET request to {relative_endpoint} endpoint')
        return self._make_request(http_method='GET',
                                  relative_endpoint=relative_endpoint,
                                  data=data)

    def post(self, relative_endpoint, data=None):
        """
        Makes a HTTP POST request
        """
        logger.info(f'Making POST request to {relative_endpoint} endpoint')
        return self._make_request(http_method='POST',
                                  relative_endpoint=relative_endpoint,
                                  data=data)
