import authenticate
from tabulate import tabulate

DEFAULT_ = "NOT AVAILABLE"
PINK_DEFAULT = "Coffee, Smoothies, Salads, Sandwiches"

#MYSQL Connection
connection = authenticate.connection
connection.ping(reconnect=True)
cursor = connection.cursor()


'''
#ONLY USE FOR THE FIRST TIME TO CREATE THE DATABASE
cursor.execute("""CREATE TABLE menu_table(DAY text DEFAULT (DEFAULT_), BREAKFAST text DEFAULT (DEFAULT_), LUNCH_KOREAN text DEFAULT (DEFAULT_), LUNCH_CHEF_SPECIAL text DEFAULT (DEFAULT_), LUNCH_PINK_STRAW text DEFAULT (PINK_DEFAULT), DINNER text DEFAULT (DEFAULT_))""")
connection.commit()
'''

Abbr= {1:"Sunday",
       2:"Monday",
       3:"Tuesday",
       4:"Wednesday",
       5:"Thursday",
       6:"Friday",
       7:"Saturday"}

# (2, "L-K", " + Wild Vegetable Bibimbap + Soybean Paste soup with cabbage + Fish Cutlet & Tartar Sauce + Fusilli Salad + Kimchi")   
def add_menu(day, time_type, m1=DEFAULT_, m2=DEFAULT_, m3=DEFAULT_):
    if time_type == "L-k":
        cursor.execute("UPDATE menu_table SET LUNCH_KOREAN = %s WHERE DAY = %s",(m1, day))
        connection.commit()
    elif time_type == "L-CS":
        cursor.execute("UPDATE menu_table SET LUNCH_CHEF_SPECIAL = %s WHERE DAY = %s",(m2, day))
        connection.commit()
    else:
        cursor.execute("UPDATE menu_table SET DINNER = %s WHERE DAY = %s",(m3, day))
        connection.commit()
    
# add_particular_menu(1,"L","K", ["rice", "soup", "chicken fries"])
# first int refers to day
def add_particular_menu(day, time, type, menu):
    day = Abbr[day]
    menu_string = ""
    for items in menu:
        menu_string += " + " + items
    if time == "L":
        if type == "K":
            add_menu(day, "L-K", menu_string)
        if type == "CS":
            add_menu(day, "L-CS", DEFAULT_, menu_string)
        elif time == "D":
            add_menu(day, "D", DEFAULT_, DEFAULT_, menu_string)
        else:
            print("Unrecognized Pattern to add particular menu")
            


def get_menu(day):
    cursor.execute("SELECT * from menu_table WHERE DAY = %s",(day,))
    untidy_list = cursor.fetchall()
    tidy_list = [["Type", "Menu"]]
    print(untidy_list)
    """
    for items in untidy_list:
        tidy_list.append
    """