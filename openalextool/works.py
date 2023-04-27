import requests
import time
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

class Works:
    def __init__(self, oaid):
        self.oaid = oaid
        if oaid != None:
            self.req = requests.get(f'https://api.openalex.org/works/{oaid}')
            self.data = self.req.json()
            self.bibtex = self.getBibtex()
    
    def __repr__(self):
        _authors = [au['author']['display_name'] for au in self.data['authorships']]
        authors =""
        if len(_authors) == 1:
            authors = _authors[0]
        elif len(_authors) > 0:
            authors = ', '.join(_authors[0:-1]) + ' and' + _authors[-1]
            
        title = self.data['title']
        
        journal = self.data['host_venue']['display_name']
        volume = self.data['biblio']['volume']
        
        issue = self.data['biblio']['issue']
        if issue is None:
            issue = ', '
        else:
            issue = ', ' + issue

        pages = '-'.join([self.data['biblio'].get('first_page', '') or '',
                          self.data['biblio'].get('last_page', '') or ''])
        year = self.data['publication_year']
        citedby = self.data['cited_by_count']
        
        oa = self.data['id']
        s = f'{authors}, {title}, {volume}{issue}{pages}, ({year}), {self.data["doi"]}. cited by: {citedby}. {oa}'
        return s

    def citing_works(self):
        cworks = []
        cworks_data = requests.get(self.data['cited_by_api_url']).json()
        for cw_data in cworks_data['results']:
            cw = Works(cw_data['doi'])
            if cw_data['doi'] == None:
                cw.data = cw_data
            cworks += [cw]
            time.sleep(0.101)
        return cworks
    
    def references(self):
        rworks = []
        for rw_url in self.data['referenced_works']:
            rw = Works(rw_url)
            rworks += [rw]
            time.sleep(0.101)
        return rworks
    
    def getBibtex(self): 
        db = BibDatabase()
        authors = ""
        for author in self.data['authorships']:
            authors += author["author"]["display_name"] + ", "
        doi = self.data["doi"].replace("https://doi.org/", "")
        db.entries = [
            {'author': authors[:-2],
             'title': self.data['title'],
             'journal': self.data['host_venue']['display_name'],
             'pages': '-'.join([self.data['biblio']['first_page'], self.data['biblio']['last_page']]),
             'year': str(self.data['publication_year']),
             'volume': self.data["biblio"]["volume"],
             'number': self.data["biblio"]["issue"],
             'ID': 'doi:' + doi,
             'url': self.data["doi"],
             'doi': doi,
             'eprint':  self.data["doi"],
             'ENTRYTYPE': 'article'}]
        writer = BibTexWriter()
        return writer.write(db)