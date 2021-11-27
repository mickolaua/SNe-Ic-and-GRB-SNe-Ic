"""
Provides python interface to the Open Supernova Catalog API
https://github.com/astrocatalogs/OACAPI
https://github.com/astrocatalogs/schema
Allows to make queries and obtain tables of objects, photometry and spectra.
Author: N. Pankov (mickolaua)
Github: https://github.com/mickolaua/SNe-Ic-and-GRB-SNe-Ic
"""

import json
from io import StringIO

import certifi
from numpy import asarray
from pandas import read_csv, DataFrame
from urllib3 import PoolManager

__all__ = ('API_URL', 'get_response',)
API_URL = "https://api.astrocats.space"


def get_response(request: str, headers: dict = {}, decode: bool = True,
                 decfmt: str = 'utf-8', kws={}) -> str:
    """
    Obtain a response from a request.

    :param request: request body
    :param headers: optional headers
    :param decode: try to decode raw content?
    :param decfmt: response decoding format
    :param kws: optional keywords to requests.get as a dictionary
    :return: a response data
    :rtype: str
    """
    data = ''
    with PoolManager(cert_reqs='CERT_REQUIRED',
                     ca_certs=certifi.where()) as http:
        response = http.request('GET', request, headers=headers, **kws)
        # Successful response
        if response.status == 200:
            data = response.data

    # Decode content if needed
    return data.decode(decfmt) if decode else data


def osc_json_normalize(data, quantity, cols):
    """
    Normalize an OSC json file data from a response in such way that pandas can
    read it properly.

    :param data: OSC response data
    :param quantity: a response quantity
    :param cols: a response columns
    :return: a table of objects or quantity
    """
    json_data = json.loads(data)
    columns = ['event'] + list(cols)
    values = []
    for event, attrs in json_data.items():
        # Request quantity like photometric or spectral points
        if quantity in attrs:
            n = len(attrs[quantity])
            for i in range(n):
                values.append([event] + attrs[quantity][i])
        else:
            # Request list of objects with attributes
            curr_values = [event]
            for attr_value in attrs.values():
                # According API https://github.com/astrocatalogs/schema
                # value field of an attribute must be specified
                actual_value = attr_value[0]['value'] if attr_value else None
                curr_values.append(actual_value)
            values.append(curr_values)

    return DataFrame({k: v for k, v in zip(columns, asarray(values).T)})


def get_table(events: tuple = ('catalog',), quantity: str = '',
              cols: tuple = ('lumdist', 'claimedtype'),
              required_cols: tuple = tuple(),
              fmt: str = 'json', closest: bool = False, complete: bool = True,
              first: bool = False, **attrs) -> DataFrame:
    """
    Get a table of objects, photometry or spectra from the OSC catalog.

    :param events: list of catalog objects (special value 'catalog' means all)
    :param quantity: which quantity to return (photometry, spectra) for
    events != 'catalog', empty string means retrieve objects, not quantity
    :param cols: which columns to return
    :param required_cols: value of these columns must be presented
    :param fmt: table format (json, csv or tsv)
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

    # Request body
    request = f"{API_URL}/{'+'.join(events)}" \
              f"{'/' + quantity + '/' if quantity else '/'}"\
              f"{'+'.join(cols)}{'?' + '&'.join(required_cols)}" \
              f"{'&' + attrs if attrs else ''}&format={fmt}"\
              f"{'&closest' if closest else ''}" \
              f"{'&complete' if complete else ''}{'&first' if first else ''}"

    print(request)

    # Headers only contain content type as of now DOES NOT WORK properly
    # for json-format
    # headers = {'Content-Type': f'application/{fmt}'}
    data = get_response(request)

    # According to OSC API, there are three possible formats: json, csv and tsv
    objects = []
    if fmt in ['csv', 'tsv']:
        delimiter = {'csv': ',', 'tsv': '\t'}[fmt]
        objects = read_csv(StringIO(data), delimiter=delimiter)
    else:
        objects = osc_json_normalize(data, quantity, cols)

    return objects


def test_json_normalize_photometry():
    from numpy import isin
    obj = 'ASASSN-14de'
    quantity = 'photometry'
    cols = ['time', 'magnitude', 'e_magnitude']
    request = f'{API_URL}/{obj}/{quantity}/{"+".join(cols)}?format=json'
    data = get_response(request)
    df = osc_json_normalize(data, quantity, cols)
    has_cols = all(isin(cols, df.columns))
    assert has_cols, f'Returned table has not {cols} columns'
    assert len(df) == 1, f'Table has {len(df)} row(s), but 1 row expected'


def test_json_normalize_catalog():
    from numpy import isin
    cols = ['redshift', 'claimedtype']
    request = f'{API_URL}/catalog/{"+".join(cols)}?claimedtype=ic&format=json'
    # headers = {'Content-Type': 'application/json'}
    data = get_response(request)
    df = osc_json_normalize(data, '', cols)
    has_cols = all(isin(cols, df.columns))
    assert has_cols, f'Returned table has not {cols} columns'
    assert len(df) > 0, f'Table has {len(df)} rows, but > 0 row(s) expected'
