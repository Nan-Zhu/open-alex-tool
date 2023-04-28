"""
Test of openalextool works class
"""

from works import Works


def test_bibtex():
    """Test to get bibtex of a work"""
    work = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert (
        work.bibtex == "@article{doi:10.1021/acscatal.5b00538,\n "
        "author = {John R. Kitchin},\n doi = {10.1021/acscatal.5b00538},\n "
        "eprint = {https://doi.org/10.1021/acscatal.5b00538},\n "
        "journal = {ACS Catalysis},\n number = {6},\n pages = {3894-3899},\n "
        "title = {Examples of Effective Data Sharing in Scientific Publishing},\n "
        "url = {https://doi.org/10.1021/acscatal.5b00538},\n "
        "volume = {5},\n year = {2015}\n}\n"
    )


def test_ris():
    """Test to get ris of a work"""
    work = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert (
        work.ris == "TY  - JOUR\nAU  - John R. Kitchin\nPY  - 2015\n"
        "TI  - Examples of Effective Data Sharing in Scientific Publishing\n"
        "JO  - ACS Catalysis\nVL  - 5\nIS  - 6\nSP  - 3894\n"
        "EP  - 3899\nDO  - https://doi.org/10.1021/acscatal.5b00538\nER  -"
    )
