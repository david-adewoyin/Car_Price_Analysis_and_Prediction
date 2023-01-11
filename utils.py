from urllib.parse import urlparse


BLOCK_RESOURCE_NAMES = [
    'adzerk',
    'analytics',
    'cdn.api.twitter',
    'doubleclick',
    'exelator',
    'facebook',
    'fontawesome',
    'google',
    'google-analytics',
    'googletagmanager',
]

BLOCK_RESOURCE_TYPES = [
    'beacon',
    'csp_report',
    'font',
    'image',
    'imageset',
    'media',
    'object',
    'texttrack',
]

def intercept_route(route, block_resource_types=BLOCK_RESOURCE_TYPES, block_resource_names=BLOCK_RESOURCE_NAMES):
    """intercept all requests and abort blocked ones"""
    if route.request.resource_type in BLOCK_RESOURCE_TYPES:
        #print(f'blocking background resource {route.request} blocked type "{route.request.resource_type}"')
        return route.abort()
    if any(key in route.request.url for key in BLOCK_RESOURCE_NAMES):
        #print( f"blocking background resource {route.request} blocked name {route.request.url}")
        return route.abort()
    return route.continue_()



