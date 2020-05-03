""" Used for adding/removing/updating menu"""
import authenticate
from tabulate import tabulate

DEFAULT_ = "NOT AVAILABLE"
PINK_DEFAULT = "Coffee\nSmoothies\nSalads\nSandwiches"

#MYSQL Connection
connection = authenticate.connection
connection.ping(reconnect=True)
cursor = connection.cursor()


'''
#ONLY USE FOR THE FIRST TIME TO CREATE THE DATABASE
cursor.execute("""CREATE TABLE menu_table(DAY text , BREAKFAST text , LUNCH_KOREAN text , LUNCH_CHEF_SPECIAL text , LUNCH_PINK_STRAW text , DINNER text )""")
connection.commit()
'''

Days= {1:"Sunday",
       2:"Monday",
       3:"Tuesday",
       4:"Wednesday",
       5:"Thursday",
       6:"Friday",
       7:"Saturday"}

# (2, "L-K", " + Wild Vegetable Bibimbap + Soybean Paste soup with cabbage + Fish Cutlet & Tartar Sauce + Fusilli Salad + Kimchi")   
def add_menu(day, time_type, m1=DEFAULT_, m2=DEFAULT_, m3=DEFAULT_):
    if time_type == "L-K":
        cursor.execute("UPDATE menu_table SET LUNCH_KOREAN = %s WHERE DAY = %s",(m1, day))
        connection.commit()
    elif time_type == "L-CS":
        cursor.execute("UPDATE menu_table SET LUNCH_CHEF_SPECIAL = %s WHERE DAY = %s",(m2, day))
        connection.commit()
    else:
        cursor.execute("UPDATE menu_table SET DINNER = %s WHERE DAY = %s",(m3, day))
        connection.commit()
    add_pink_straw()

def add_pink_straw():
    for i in range(1,8):
        day = Days[i]
        cursor.execute("UPDATE menu_table SET LUNCH_PINK_STRAW = %s WHERE DAY = %s",(PINK_DEFAULT, day))
    
# add_particular_menu(1,"L","K", ["rice", "soup", "chicken fries"])
# first int refers to day
def add_particular_menu(day, time, type, menu):
    day = Days[day]
    menu_string = ""
    for items in menu:
        if menu_string == "" or (menu_string != "" and menu[-1] != items):
            menu_string += items + "\n"
        else:
            menu_string += items
    if time == "L":
        if type == "K":
            add_menu(day, "L-K", menu_string)
        if type == "CS":
            add_menu(day, "L-CS", DEFAULT_, menu_string)
    elif time == "D":
        add_menu(day, "D", DEFAULT_, DEFAULT_, menu_string)
    else:
        print("Unrecognized Pattern to add particular menu")

# Resets the weekly menu        
def clear_week_menu():
    for i in range(1,8):
        day = Days[i]
        cursor.execute("UPDATE menu_table SET BREAKFAST = %s, LUNCH_KOREAN = %s, LUNCH_CHEF_SPECIAL = %s, LUNCH_PINK_STRAW = %s,DINNER =  %s WHERE DAY =  %s", (DEFAULT_,DEFAULT_,DEFAULT_,PINK_DEFAULT,DEFAULT_, day))
        connection.commit()

def get_menu(day):
    cursor.execute("SELECT * FROM menu_table WHERE DAY = %s",(day,))
    menu_tuple = cursor.fetchall()[0]
    tidy_list = [["Type", "Menu"]]
    type = ["Day","Breakfast", "Korean (L)", "Chef's Special (L)", "Pink Straw (L)", "Dinner"]
    for i in range(1, len(menu_tuple)):
        tidy_list.append([type[i], menu_tuple[i]])
    return tabulate(tidy_list, headers="firstrow", tablefmt="jira")

def get_weekly_menu():
    to_return = ""
    for i in range(1, 8):
        to_return += Days[i] + ":\n" + get_menu(Days[i]) + "\n"
    return to_return




