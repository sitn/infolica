from pyramid.view import view_config
import pyramid.httpexceptions as exc

""" Return httpok"""
@view_config(route_name='api_test', request_method='GET')
def suivi_mandats_view(request):
    # Check if the api is working successfully
    return exc.HTTPOk("Yeah, api is working!")

