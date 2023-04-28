"""
Class for Open Alex Works
"""

import time
import requests

from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase


class Works:
    """Class of Works for Open Alex"""

    def __init__(self, oaid):
        self.oaid = oaid
        if oaid is not None:
            self.req = requests.get(
                f"https://api.openalex.org/works/{oaid}", timeout=10
            )
            self.data = self.req.json()

    def __repr__(self):
        _authors = [au["author"]["display_name"] for au in self.data["authorships"]]
        authors = ""
        if len(_authors) == 1:
            authors = _authors[0]
        elif len(_authors) > 0:
            authors = ", ".join(_authors[0:-1]) + " and" + _authors[-1]
        title = self.data["title"]
        volume = self.data["biblio"]["volume"]
        issue = self.data["biblio"]["issue"]
        if issue is None:
            issue = ", "
        else:
            issue = ", " + issue
        pages = "-".join(
            [
                self.data["biblio"].get("first_page", "") or "",
                self.data["biblio"].get("last_page", "") or "",
            ]
        )
        year = self.data["publication_year"]
        citedby = self.data["cited_by_count"]
        work_id = self.data["id"]
        description = (
            f"{authors}, {title}, {volume}{issue}{pages}, ({year}),"
            + f'{self.data["doi"]}. cited by: {citedby}. {work_id}'
        )
        return description

    @property
    def bibtex(self):
        """GetBibtex of this work"""
        database = BibDatabase()
        authors = ""
        for author in self.data["authorships"]:
            authors += author["author"]["display_name"] + ", "
        doi = self.data["doi"].replace("https://doi.org/", "")
        database.entries = [
            {
                "author": authors[:-2],
                "title": self.data["title"],
                "journal": self.data["host_venue"]["display_name"],
                "pages": "-".join(
                    [
                        self.data["biblio"]["first_page"],
                        self.data["biblio"]["last_page"],
                    ]
                ),
                "year": str(self.data["publication_year"]),
                "volume": self.data["biblio"]["volume"],
                "number": self.data["biblio"]["issue"],
                "ID": "doi:" + doi,
                "url": self.data["doi"],
                "doi": doi,
                "eprint": self.data["doi"],
                "ENTRYTYPE": "article",
            }
        ]
        writer = BibTexWriter()
        bib = writer.write(database)
        return bib

    @property
    def ris(self):
        """Get ris of the work"""
        fields = []
        if self.data["type"] == "journal-article":
            fields += ["TY  - JOUR"]
        else:
            return ""
        for author in self.data["authorships"]:
            fields += [f'AU  - {author["author"]["display_name"]}']
        fields += [f'PY  - {self.data["publication_year"]}']
        fields += [f'TI  - {self.data["title"]}']
        fields += [f'JO  - {self.data["host_venue"]["display_name"]}']
        fields += [f'VL  - {self.data["biblio"]["volume"]}']
        if self.data["biblio"]["issue"]:
            fields += [f'IS  - {self.data["biblio"]["issue"]}']
        fields += [f'SP  - {self.data["biblio"]["first_page"]}']
        fields += [f'EP  - {self.data["biblio"]["last_page"]}']
        fields += [f'DO  - {self.data["doi"]}']
        fields += ["ER  -"]
        ris = "\n".join(fields)
        return ris
