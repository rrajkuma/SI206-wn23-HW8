# Your name: Rachel Rajkumar
# Your student id: 7099 6834
# Your email: rrajkuma@umich.edu
# List who you have worked with on this homework: N/A

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    rest_dict = {}
    cur.execute("SELECT COUNT() FROM restaurants")
    len = int(cur.fetchone()[0])
    for i in range(1, len+1):
        temp = {}
        name_query = "SELECT name FROM restaurants where id = "  + '"' + str(i) + '"' 
        cur.execute(name_query)
        name = cur.fetchone()[0]
        rate_query = "SELECT rating FROM restaurants where id = "  + '"' + str(i) + '"' 
        cur.execute(rate_query)
        rate = cur.fetchone()[0]
        cat_query = "SELECT category FROM categories JOIN restaurants ON categories.id = restaurants.category_id WHERE restaurants.id = " + '"' + str(i) + '"' 
        cur.execute(cat_query)
        cat = cur.fetchone()[0]
        build_query = "SELECT building FROM buildings JOIN restaurants ON buildings.id = restaurants.building_id WHERE restaurants.id = " + '"' + str(i) + '"' 
        cur.execute(build_query)
        build = cur.fetchone()[0]
        temp["category"] = cat
        temp["building"] = build
        temp["rating"] = rate
        rest_dict[name] = temp
    return(rest_dict)


def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    temp_dict = {}
    cur.execute("SELECT COUNT() FROM restaurants")
    len = int(cur.fetchone()[0])
    for i in range(1, len+1):
        cat_query = "SELECT category FROM categories JOIN restaurants ON categories.id = restaurants.category_id WHERE restaurants.id = " + '"' + str(i) + '"' 
        cur.execute(cat_query)
        cat = cur.fetchone()[0]
        temp_dict[cat] = temp_dict.get(cat, 0) + 1
    temp = sorted(temp_dict.items(), key = lambda x:x[1])
    cat_dict = dict(temp)
    names = list(cat_dict.keys())
    values = list(cat_dict.values())
    plt.barh(names, values)
    plt.title('Number of restaurants in South University by type')
    plt.xlabel('Restaurants')
    plt.ylabel("Number of restaurants")
    plt.savefig('rest_bar.png')
    return cat_dict




def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    build_list = []
    query = "SELECT name FROM restaurants JOIN buildings on restaurants.building_id = buildings.id where buildings.building = " + '"' + str(building_num) + '"' + "ORDER BY restaurants.rating DESC"
    res = cur.execute(query)
    for row in res:
        build_list.append(row[0])
    return build_list

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    load_rest_data('South_U_Restaurants.db')
    plot_rest_categories('South_U_Restaurants.db')
    find_rest_in_building(1140, 'South_U_Restaurants.db')
    #pass


class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    '''
    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)
    '''
if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)