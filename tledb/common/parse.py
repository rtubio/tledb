
"""
Module with simple methods for string manipulations while parsing files.
"""


import logging


def tle_scientific_2_float(number):
    """
    This method transforms a scientific suffix from the TLE format into a
    string format that can be parsed into a float by Python. The format is the
    following:

    15254-5 = 0.15254 >>> 15254E-5
    -333-3 = -0.333 >>> 333E-3

    @param number String where the decimal is expected
    @returns String that can be parsed by float()
    """
    return float(number[:-2] + 'E-' + number[-1])
