PAGE_LIMIT = 10
REGION_CODES = {
    'AU': '.com.au',
    'BR': '.com.br',
    'CA': '.ca',
    'CN': '.cn',
    'DE': '.de',
    'ES': '.es',
    'FR': '.fr',
    'IN': '.in',
    'IT': '.it',
    'JP': '.co.jp',
    'MX': '.com.mx',
    'NL': '.nl',
    'SG': '.com.sg',
    'UK': '.co.uk',
    'US': '.com'
}

DEFAULT_REGION = "UK"

BASE_URL = 'https://www.amazon'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
GAT_ID = 'tag'
QUERY_BUILD_DICT = {GAT_ID: 'alhs-20'}

# SEARCH_URL = '%s/s/ref=nb_sb_noss?sf=qz&keywords=%s&ie=UTF8&unfiltered=1&page=%s'
SEARCH_URL = '%s/s?k=%s&page=%s'

# /Authentic-Cigarette-Starter-3000mAh-PEACEVAPETM/product-reviews/B079RXYMF8/ref=cm_cr_getr_d_paging_btm_next_3?ie=UTF8&reviewerType=all_reviews&pageNumber=2
REVIEW_URL = "%s/%s/product-reviews/%s/?reviewerType=all_reviews&pageNumber=%s"
