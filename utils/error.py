HTTP_ERROR_CODES = {
    400: "Bad Request - Incorrect parameters.",
    401: "Unauthorized - Wrong Token.",
    404: "Not Found - The specified endpoint could not be found.",
    405: "Method Not Allowed - You tried to access an endpoint with an invalid method.",
    406: "Not Acceptable - Incorrect request format.",
    429: "Too Many Requests – Rate limited, pause requests.",
    500: "Internal Server Error - We had a problem with our server. Try again later.",
    503: "Service unavailable"
}


class HttpClientConnectionError(Exception):
    """
    Used for raising all kind of client errors
    """
    pass
