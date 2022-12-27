from algoliasearch_django import algolia_engine


def get_client():
    return algolia_engine.client


def get_index(index_name="cfe_Place"):
    client = get_client()
    index = client.init_index(index_name)
    return index


def perform_search(qeury, **kwargs):
    index = get_index()
    params = {"hitsPerPage": 100}
    index_filters = [f"{k}:{v}" for k, v in kwargs.items() if v]
    if len(index_filters) != 0:
        params["facetFilters"] = index_filters
    results = index.search(qeury, params)
    return results
