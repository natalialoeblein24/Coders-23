from extract import extract
from unite import unite_pl

if __name__ == "__main__":
    extract(
        "unanimad/corona-virus-brazil",
        "../data/",
    )

    unite_pl("../data/")
