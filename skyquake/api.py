from lxml import html as html_module
from config import DEFAULT_REGION, SEARCH_URL, PAGE_LIMIT
from utils import build_base_url


class AmzSearch(object):
    _products = []
    _indexes = []

    _urls = []

    """
        Whilst it may appear that multiple different arguments can be passed
        to the constructor this is not the case in terms of outcome. The arguments
        follow the following hierarchy:

        (query, [page], [region])
                   |
                 (url)
                   |
                (html)
                   |
            (html_element)
                   |
              (products)

        That is to say that if arguments are passed at more than one level, the
        arguments at the highest level will be used to override the arguments passed
        on other levels. For example, if a url was passed as well as a query, the url
        would be ignored and generated from the query.

        Optional Args:
            query (str): A search query to look up on Amazon.
            page (int*): The page number of the query (defaults to 1).
            region (str): The Amazon region/country to search. For a list of countries
              to country code see the [regions table](../regions.md) (defaults to UK).
            url (str*): An Amazon search url (not recommended).
            html (str*): The HTML code from an Amazon search page (not recommended).
            html_element (LXML root*): The LXML root generated from the HTML off of an
              Amazon search page (not recommended).
            products (list*): A list of AmzProducts.

        Note: All arg types marked with a "*" can be an iterable of that type. In other
        words, a page can either be an int or a list or range, etc. of ints to be searched.
        The same is true for url, html, html_elements and products.

    """

    def __init__(self, query=None, page=1, region=DEFAULT_REGION, url=None, html=None, html_element=None, products=None):
        self._urls = [self.build_url(query=query, page_num=p, region=region)
                      for p in range(1, page + 1)] if page < PAGE_LIMIT else []

    def __repr__(self):
        out = []
        max_index_len = 10
        for index, product in self.items():
            temp_repr = repr(index) + ':' + max_index_len * ' '
            temp_repr = temp_repr[:max_index_len] + repr(product)
            temp_repr = temp_repr.replace('\n', '\n' + max_index_len * ' ')

            out.append(temp_repr)
        out.append('<' + self.__class__.__name__ + ' object>')
        return '\n'.join(out)

    def __iter__(self):
        return iter(self._indexes)

    def __len__(self):
        return len(self._products)

    def __getitem__(self, key):
        return self.get(key, default=None, raise_error=True)

    def build_url(url=None, query='', page_num=1, region=DEFAULT_REGION):

        base = build_base_url(region)
        url = SEARCH_URL % (base, query, page_num)

        return url

    def _set_repr_max_len(self, val):
        """
        Private Method - Recursively sets the maximum repr width length for
        products.
        """
        for product in self:
            if hasattr(product, 'REPR_MAX_LEN'):
                product.REPR_MAX_LEN = val

    def get(self, key, default=None, raise_error=False):
        """
        Gets the AmzProduct by index, default is returned if the index is not found or an
        error is raised if raise_error=True. Indexing the AmzSear object is equivalent to
        calling this method with raise_error=True.

        Args:
            key (str): The index number of the product in the AmzSear object.

        Optional Args:
            default: The default value, should raise_error=False.
            raise_error (bool): If True, an error will be raised if the key cannot be found.

        Returns:
            The AmzProduct at the key, otherwise the default value.
        """
        key = str(key)
        if key not in self._indexes:
            if raise_error:
                raise KeyError('The key %s not exist' % (repr(key)))
            else:
                return default

        return self._products[self._indexes.index(key)]

    def rget(self, key, default=None, raise_error=False):
        """
        "Relative get" - Gets the nth key of the the object.

        For example, if the index method returns the list ['0', '2', '4', '7'],
        calling rget with key=1 will return the AmzProduct at index '2', whereas
        calling rget with key=-1 will return the AmzProduct at index '7'.

        Args:
            key (int): The relative index of the desired product.

        Optional Args:
            default: The default value, should raise_error=False.
            raise_error (bool): If True, an error will be raised if the index is out of range.

        Returns:
            The AmzProduct at the relative index, otherwise the default value.
        """
        if raise_error:
            return self._products[key]
        else:
            try:
                return self._products[key]
            except IndexError:
                return default

    def aget(self, key, default=None, raise_error=False):
        """
        "All get" - gets a list of attributes values from one or more attribute keys.

        Args:
            key (str or list): A single attribute name or a list of attributes.

        Optional Args:
            default: The default value, should raise_error=False and the attribute
              name be unavailable for a product.
            raise_error (bool): If True, an error will be raised if the value of key
              or any of the values of key are not found.

        Returns:
            list: List of tuples in product order of the AmzSear.
        """
        if not isinstance(key, list):
            key = [key]

        data = []
        for i, k in enumerate(key):
            data.append([])
            curr_out = data[i]

            for index, prod in self.items():
                if hasattr(prod, k):
                    curr_out.append(getattr(prod, k))
                elif raise_error:
                    raise ValueError('The key %s is not available at index %s' %
                                     (repr(k), repr(index)))
                else:
                    curr_out.append(default)

        return list(zip(*data))

    def items(self):
        """
        An iterator yielding a tuple of an index and a AmzProduct for each iteration.

        Returns:
            zip: A generator to be iterated over.
        """
        return zip(self._indexes, self._products)

    def indexes(self):
        """
        A list of all all indexes in the current object.

        Returns:
            list: A list of all the indexes in the object.
        """
        return list(x for x in self)

    def products(self):
        """
        A list of all products in the current object.

        Returns:
            list: A list of AmzProduct objects.
        """
        return list(y for x, y in self.items())

    keys = indexes
    values = products

    def to_dataframe(self, recursive=True, flatten=False):
        """
        Pandas must be installed for this method to be called. It will convert the
        object to a Pandas DataFrame using the same possible recursive and flattening
        options of the AmzBase to_dict method.

        Optional Args:
            recursive (bool): See [AmzBase to dict](AmzBase.mdto_dict) method.
            flatten (bool): See [AmzBase to dict](AmzBase.mdto_dict) method.

        Returns:
            Pandas DataFrame: A dataframe with each product in a series with
            it's index.
        """
        from pandas import DataFrame
        return DataFrame([y.to_series(recursive=recursive, flatten=flatten) for x, y in self.items()],
                         index=self._indexes)


if __name__ == '__main__':
    amz = AmzSearch('keyboard', page=5, region='UK')
    last_item = amz.rget(-1)
    print(amz._urls)
