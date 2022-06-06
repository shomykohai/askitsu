"""
The MIT License (MIT)

Copyright (c) 2022-present ShomyKohai

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from colorama import Fore, Style


class AskitsuException(Exception):
    """
    Base class for most of the library errors

    .. versionadded:: 0.4.0
    """

    pass


class HTTPError(AskitsuException):
    """
    Represents a generic HTTP error.

    Parameters
    -----------
    msg: :class:`str`
        Error message
    status: :class:`int`
        Code of the HTTP response
    """

    def __init__(self, msg: str, status: int) -> None:
        self.status = status
        super().__init__(msg)


class InvalidArgument(AttributeError):
    """
    Raises when an invalid entry gets passed

    Parameters
    -----------
    msg: :class:`str`
        Error message to pass
    """

    def __init__(self, msg) -> None:
        super().__init__(msg)


class NotAuthenticated(HTTPError):
    """
    Raises when an Authenticated API request
    get place without being authenticated

    .. versionadded:: 0.3.0
    """

    def __init__(self) -> None:
        super().__init__(
            f"{Fore.RED}You are not authenticated.\n"
            f"Check if the called API request need authentication "
            f"or if you passed valid credentials{Style.RESET_ALL}",
            401
        )


class BadApiRequest(HTTPError):
    """
    Raises when a 400 error code takes place

    .. versionadded:: 0.4.0
    """

    def __init__(self, response: str) -> None:
        super().__init__(
            f"{Fore.RED}An error occured.\n"
            f"{response['detail']} - Response code: {400}{Style.RESET_ALL}",
            400
        )
