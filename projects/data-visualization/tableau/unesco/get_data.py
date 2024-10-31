import pandas as pd


def main():
    data = get_data()
    dump_sites_by_region(data[2])
    dump_sites_by_country(data[7])


def get_data():
    # specifying the encoding allows to handle special characters
    data = pd.read_html("https://whc.unesco.org/en/list/stat/", encoding="utf-8")
    return data


def dump_sites_by_region(df):

    # remove non-breaking space characters followed by an asterisk using regular expressions
    df.replace("\u00A0\*", "", regex=True, inplace=True)
    df.to_csv("sites_by_region.csv", index=False)


def dump_sites_by_country(df):

    # clean up some country names
    df.replace("Netherlands (Kingdom of the)", "Netherlands", inplace=True)
    df.replace("Türkiye", "Turkey", inplace=True)

    df.to_csv("sites_by_country.csv", index=False)


if __name__=="__main__":
    main()
