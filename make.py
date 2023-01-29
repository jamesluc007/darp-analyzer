import os

"""
This script downloads darp DATA.
It simly calls a shell script provided by the hackathon organization
TODO: Implment downloading using python only, it might avoid syncronization issues in the future
"""


def update_data():
    os.system("sh ./data/load_data.sh")


if __name__ == "__main__":
    update_data()
