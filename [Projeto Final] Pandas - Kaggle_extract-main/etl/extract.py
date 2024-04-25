import os

from decorators.utils import log_function, time_function


@time_function
@log_function
def extract(dataset_name: str, download_path: str):
    return os.system(
        " ".join(
            [
                "kaggle",
                "datasets",
                "download",
                "-d",
                dataset_name,
                "-p",
                download_path,
                "--unzip",
            ]
        )
    )


if __name__ == "__main__":
    extract(
        "unanimad/corona-virus-brazil",
        "../data/",
    )
