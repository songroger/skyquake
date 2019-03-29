from config import DEFAULT_REGION, REGION_CODES, BASE_URL


def build_base_url(region=DEFAULT_REGION):
    find_region = region.upper()
    if find_region not in REGION_CODES.keys():
        raise ValueError('%s is an invalid region' % (repr(region)))

    return BASE_URL + REGION_CODES[find_region]
