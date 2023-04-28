"""
Main function to get citation of a work
"""

import click
from openalextool.works import Works


@click.command()
@click.option(
    "--cite",
    "-c",
    prompt="input --cite in {ris, bib}",
    help="The citation type to print",
)
@click.argument("doi", nargs=-1)
def main(cite, doi):
    """Main method to get citation of a work"""
    work = Works(doi[0])
    if cite == "ris":
        print(work.ris)
    elif cite == "bib":
        print(work.bibtex)


if __name__ == "__main__":
    main()
