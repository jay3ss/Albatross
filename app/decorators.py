from functools import wraps
from typing import Callable

from flask import redirect, request, url_for, Response
from flask_login import current_user


def own_resource_required(redirect_route: str) -> Callable:
    """
    Decorator to require that a user accessing a resource must be the owner of
    that resource. If the user is not the owner of the resource, they are
    redirected to the given redirect route.

    Args:
        redirect_route (str): The route to redirect the user to if they are not
        the owner of the resource.

    Returns
        Callable: The decorated route function.
    """
    def decorator(route: Callable) -> Callable:
        """
        Inner decorator function

        Args:
            route (Callable): The route function to be decorated.

        Returns:
            Callable: The decorated route function.
        """
        @wraps(route)
        def wrapped_route(*args, **kwargs) -> Response:
            """
            Inner wrapped route function.

            Returns:
                Response: The result of the route function if the
                user is the owner of the resource, else a redirect response
            """
            username = request.view_args["username"].lower()
            if not current_user.username.lower() == username:
                return redirect(url_for(redirect_route))
            return route(*args, **kwargs)
        return wrapped_route

    return decorator
