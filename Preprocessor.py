import json
from pprint import pprint
import numpy as np
import pandas as pd


def main():
    df = pd.read_json("./data/nys_tweets_filtered_2017_0.json", lines=True)
    pprint(df.lines)
    pass


if __name__ == '__main__':
    main()
