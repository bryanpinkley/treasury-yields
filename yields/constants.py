# URL for the US Dept of Treasury XML Feed.
XML_URL = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml?data=daily_treasury_yield_curve&field_tdr_date_value="

# A constant to convert terms from months to a string representation.
TERM_CHOICES = {
    1: "1 Mo",
    2: "2 Mo",
    3: "3 Mo",
    4: "4 Mo",
    6: "6 Mo",
    12: "1 Yr",
    24: "2 Yr",
    36: "3 Yr",
    60: "5 Yr",
    84: "7 Yr",
    120: "10 Yr",
    240: "20 Yr",
    360: "30 Yr",
}
