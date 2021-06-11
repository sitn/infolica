from zope.interface import implementer

from pyramid.authentication import RemoteUserAuthenticationPolicy as PyramidRemoteUserAuthenticationPolicy
from pyramid.interfaces import IAuthenticationPolicy
import os


@implementer(IAuthenticationPolicy)
class RemoteUserAuthenticationPolicy(PyramidRemoteUserAuthenticationPolicy):
    """ A :app:`Pyramid` :term:`authentication policy` which
is inherited from the default Pyramid remote user authentication policy.
All calls through Apache (mod_wsgi) will have a REMOTE_USER variable,
if not it means that the current user is running on the pserve mode,
thus we connect him using his server/computer login.
"""

    def authenticated_userid(self, request):
        """ The ``Remote-User`` value found within the ``environ``."""

        username = request.headers.get(self.environ_key)

        if request.environ.get(self.environ_key) is None \
            and os.environ.get('LOCAL_DEV_USERNAME', '') != '':
            username = os.environ.get('LOCAL_DEV_USERNAME')

        # username may be None because of Satisfy any in the Apache SSPI conf
        if username:
            username = username.lower().split('\\')[-1]

        return username
