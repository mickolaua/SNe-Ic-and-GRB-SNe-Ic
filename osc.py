"""
Provides python interface to the OSC API
(https://github.com/astrocatalogs/OACAPI)
Allows to make queries and obtain tables of objects, photometry and spectra.
Author: N. Pankov (mickolaua)
Github: https://github.com/mickolaua/SNe-Ic-and-GRB-SNe-Ic
"""

from io import StringIO
from urllib3 import PoolManager
from pandas import read_csv, read_json, DataFrame

__all__ = ('API_URL', 'get_response',)
API_URL = "https://api.astrocats.space"


def get_response(request: str, headers: dict = {},
                 decfmt: str = 'utf-8') -> str:
    """
    Obtain a response from a request.

    :param request: request body
    :param headers: optional headers
    :param decfmt: response decoding format
    :return: a response
    :rtype: str
    """
    response = ''
    with PoolManager() as http:
        response = http.request(
            'GET', request, headers=headers).data.decode(decfmt)
    return response


def get_table(events: tuple = ('catalog',), quantity: str = '',
              cols: tuple = ('lumdist', 'claimedtype'),
              fmt: str = 'json', closest: bool = False, complete: bool = True,
              first: bool = False, **attrs) -> DataFrame:
    """
    Get a table of quantities (objects, photometry, spectra) from the OSC
    catalog.

    :param events: list of catalog quantities
    :param quantity: which quantity to return (photometry, spectra),
                     empty string means retrieve objects, not quantity
    :param cols: which columns to return
    :param fmt: table format (JSON, CSV or TSV)
    :param closest: return the quantities with the closest value to the
                    specified attributes
    :param complete: return only quantities containing all of the requested
                     attributes
    :param first: return only the first of each of the listed quantities
    :param attrs: optional attributes for query (e.g, claimedtype='Ia')
    :return: an object table in form of pd.DataFrame
    """
    # If no optional attributes passed, retrieve ALL metadata
    attrs = '&'.join([f'{k}={v}' for k, v in attrs.items()]) if attrs else ''
    if closest:
        attrs += '&closest'
    if complete:
        attrs += '&complete'
    if first:
        attrs += '&first'

    # Request body
    request = f"{API_URL}/{'+'.join(events)}" \
              f"{'/' + quantity + '/' if quantity else ''}"\
              f"{'+'.join(cols)}?{attrs}" \
              f"&format={fmt}{'&closest' if closest else ''}" \
              f"{'&complete' if complete else ''}{'&first' if first else ''}"

    # Headers only contain content type as of now
    headers = {'Content-Type': f'application/{fmt}'}

    # Wrap response into StringIO to feed to the pandas reader
    response = StringIO(get_response(request, headers=headers))

    # According to OSC API, there are three possible formats: json, csv and tsv
    objects = []
    if fmt == 'csv':
        objects = read_csv(response)
    elif fmt == 'tsv':
        objects = read_csv(response, delimiter='\t')
    else:
        # Any other format specification returns JSON
        objects = read_json(response)

    return objects
