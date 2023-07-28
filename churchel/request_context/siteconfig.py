import json
from os.path import join, dirname


def site_info(request):
    # basic site information for the frontend/templates
    with open(join(dirname(__file__), 'data/site_config.json')) as f:
        return json.load(f)
