import datetime
import requests

import xml.etree.ElementTree as ET

from yields.constants import XML_URL


def get_text(tag: str, properties: ET.Element, ns: dict) -> str | None:
    """
    Helper function to retrieve the content of an XML element from the properties.

    :param tag: The name of the XML tag to search for.
    :param properties: The XML properties element to search within.
    :param ns: A dictionary mapping XML namespaces.
    :return: The text content of the found XML element, or None if the element
        does not exist.
    """
    el = properties.find(f"d:{tag}", ns)
    return el.text if el is not None else None


def get_yield_data() -> dict:
    """
    Fetch the current treasury yields from the US Dept of Treasury XML feed.
    The data will be from the most recent date available.

    :return: A dictionary containing yield data.
    """
    now = datetime.date.today()
    yyyy = now.strftime("%Y")
    complete_url = f"{XML_URL}{yyyy}"
    response = requests.get(complete_url, timeout=30)
    response.raise_for_status()

    # Parse XML into an Element Tree. The entries are nodes in the tree.
    root = ET.fromstring(response.content)

    # The XML uses namespaces. The default namespace is "atom".
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
        "d": "http://schemas.microsoft.com/ado/2007/08/dataservices",
    }

    # Get a list of all the entries by matching the "entry" tag with the "atom" namespace.
    entries = root.findall("atom:entry", ns)

    # Pick the last entry. The assumption is that the entries are in chronological order.
    latest_entry = entries[-1]

    # Get the properties for the entry, since that contains the yield data.
    properties = latest_entry.find(".//m:properties", ns)

    data = {
        "date": get_text("NEW_DATE", properties, ns)[:10],
        "1 Mo": get_text("BC_1MONTH", properties, ns),
        "2 Mo": get_text("BC_2MONTH", properties, ns),
        "3 Mo": get_text("BC_3MONTH", properties, ns),
        "4 Mo": get_text("BC_4MONTH", properties, ns),
        "6 Mo": get_text("BC_6MONTH", properties, ns),
        "1 Yr": get_text("BC_1YEAR", properties, ns),
        "2 Yr": get_text("BC_2YEAR", properties, ns),
        "3 Yr": get_text("BC_3YEAR", properties, ns),
        "5 Yr": get_text("BC_5YEAR", properties, ns),
        "7 Yr": get_text("BC_7YEAR", properties, ns),
        "10 Yr": get_text("BC_10YEAR", properties, ns),
        "20 Yr": get_text("BC_20YEAR", properties, ns),
        "30 Yr": get_text("BC_30YEAR", properties, ns),
    }

    return data
