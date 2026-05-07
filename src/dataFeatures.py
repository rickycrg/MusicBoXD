import pandas as pd

def showSorting(file):
    df = pd.read_csv(file, parse_dates=["release date"])
    df["vote"] = pd.to_numeric(df["vote"], errors="coerce")

    while True:
        x = input("select sorting mode to print\n (Descending Opinion (1), Ascending Opinion (2), Release date (3)), type something else to return to the menu: ")
        if x=='1':
            print(df.sort_values(by="vote", ascending=False))
        elif x=='2':
            print(df.sort_values(by="vote", ascending=True))
        elif x=='3':
            print(df.sort_values(by="release date"))
        else:
            return False
            


    




        