import pandas as pd

# Function to show the music in the order that the user prefer
def showSorting(file):
    df = pd.read_csv(file, parse_dates=["release date"])
    while True:
        x = input("select sorting mode to print\n (Descending Opinion (1), Ascending Opinion (2), Release date (3)), type something else to return to the menu: ")
        if x=='1':
            print(df.sort_values(by = "vote", ascending = False, kind='mergesort'))
        elif x=='2':
            print(df.sort_values(by = "vote", kind='mergesort'))
        elif x=='3':
            print(df.sort_values(by = "release date", kind='mergesort'))
        else : 
            return False
            


    




        