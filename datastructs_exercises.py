# Exercise 1 - mapping + filtering
# Try to use a "list-comprehension" for each of the following exercises
# Docs on list comprehension: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions

# Write a function that computes the length of each string in a list
def lengths(strings):
    return [len(s) for s in strings]

# Write a function that computes the square of each number in a list
def squares(numbers):
    return [x ** 2 for x in numbers]

# Write a function that returns all even numbers in a list 
# A number is even if it's divisible by 2 (i.e. x % 2 == 0)
def even(numbers):
    return [x for x in numbers if x % 2 == 0]

# Write a function that returns all strings from a list that contain the substring "python"
def pythons(strings):
    return [s for s in strings if "python" in s]

# Exercise 1 - Advanced
# You can note that the functions look quite similar. We have two types of functions here
# - "mapping": here we apply a function to each element of the list and keep the list otherwise the same
# - "filtering": here we remove/keep elements of the list based on a boolean condition
# There is a way to generalize these types of functions

# Write a function "my_map" that takes 2 parameters: a list and a function. 
# "my_map" then applies the function to each element in the list and returns the result. 
def my_map(input_list, function):
    return [function(elem) for elem in input_list]

# Write a function "my_filter" that takes 2 parameters: a list and "predicate" function (a function that takes a value and returns a boolean).
# "my_filter" then only returns the elements that pass the predicate. 
def my_filter(input_list, predicate):
    return [elem for elem in input_list if predicate(elem)]

# Try to use my_map/my_filter to implement the initial exercises.
# Check how you can pass the function arguments in a very short syntax: https://towardsdatascience.com/lambda-functions-with-practical-examples-in-python-45934f3653a8

# Exercise 2 - reducing and folding

# Write a function that computes the largest number in a list
# Note: In python you can represent negative infinity by float('-inf'). This number cannot be bigger than any other number in python.
def max_of(numbers):
    current_max = float('-inf')
    for elem in numbers:
        if elem > current_max:
            current_max = elem
    return current_max

# Write a function that computes the smallest number in a list
# Note: In python you can represent infinity by float('inf'). This number cannot be smaller than any other number in python.
def min_of(numbers):
    current_min = float('inf')
    for elem in numbers:
        if elem < current_min:
            current_min = elem
    return current_min

# Write a function that sums the elements of a list
def sum(numbers):
    current_sum = 0
    for elem in numbers:
        current_sum += elem
    return current_sum

# Exercise 2 - Advanced
# Similar to before, the functions again look very similar. They don't return a list. But all of them have a some sort of 
# default value that is used when the input is empty and they accumulate some result based on the elements of the list.

# Write a function "fold" that takes 3 arguments: a list, an accumulator, and an "accumulator" function.
# The accumulator function works on 2 arguments: The current element of the list and the accumulated value up to now. 
# The output of the accumulator function is used to update the accumulator.
def fold(input_list, accumulator, accumulator_function):
    for elem in input_list:
        accumulator = accumulator_function(elem, accumulator)
    return accumulator

# Use fold to implement "reduce". They are related functions with 2 important differences
# - reduce throws an error if the input list is empty
# - reduce only works on the elements of the input list (it doesn't take an accumulator that can be completely different)
def reduce(input_list, reduce_function):
    if not input_list:
        raise Error('empty list is not allowed!')
    else:
        # this is a nice way in newer python versions to get the first element of a list and the remaining list
        first_element, *remaining_elements = input_list
        return fold(remaining_elements, first_element, reduce_function) # use fold here

# Use reduce to implement max_of, min_of
# Use fold to implement sum

# Python built-in ways
# Python provides built-in map, filter and reduce functions
# - map and filter are exactly like the ones we implemented here (the slight difference is that they are more general and don't return a list as the output, but an iterator. 
# But that can easily be transformed to a list by using the list constructor).
# - reduce actually combines the fold and reduce we implemented into one function. That is, if you don't provide an accumulator
# it acts like our reduce (i.e. throws an error on an empty input). If you provide one, it acts like our fold.
# https://towardsdatascience.com/python-map-filter-and-reduce-9a888545e9fc

# In fact, folding is the ultimate function to iterate over lists. Most other functions can be implemented in terms of fold.
# A bit trickier, but try to also implement my_map and my_filter with fold.
def map_via_fold(input_list, function):
  return fold(input_list, [], lambda elem, mapped: [*mapped, function(elem)])

def filter_via_fold(input_list, predicate):
  return fold(input_list, [], lambda elem, filtered: [*filtered, elem] if predicate(elem) else filtered)


# Other functions like sum, min and max are also very common and already built-in in python. 
# They're listed here with other useful common built-in functions
# https://docs.python.org/3/library/functions.html#built-in-functions

# Exercise 3 - lists and dictionaries

# Find the duplicate entries from a list. 
# I.e. an input of [1,1,2,3,4,4,5,6,7] should return [1,4] because 1 and 4 are duplicate elements. 
# The order in the output list does not have to match the order of the input list. 
# A dictionary can help here to find out which elements appear more than 1 time in the list.
# The 'dictionary.get' function can be helpful here as well https://docs.python.org/3/library/stdtypes.html#dict.get
def find_duplicates(input_list):
    counts = {}
    for elem in input_list:
        counts[elem] = counts.get(elem, 0) + 1
    return [elem for elem in counts.keys() if counts[elem] > 1]


# Write a function that counts the occurrences of distinct words in the lyrics to
# Never gonna give you up https://www.youtube.com/watch?v=dQw4w9WgXcQ. 
# The function should return a list of tuples (word, number of occurrences) ordered by the number of occurrences in descending order.
#
# The lyrics are provided as a list of strings where each string represents a line of the lyrics. 
# One possible approach to do this:
# - get a list of words from each line
#   - check str.split() for how to split up a single line into different words https://docs.python.org/3/library/stdtypes.html#str.split
# - "flatten" the list of "words lists" into a single list containing all words
#   - check the provided helper function 
# - go over that list and use a dictionary to keep track of the occurrences of each word
# - you can also try to do a simple "normalization" (https://en.wikipedia.org/wiki/Text_normalization) of each word
#   - check the provided helper function 
import itertools

# This returns a list of strings. Each string represents a line of the lyrics. 
def load_lyrics():
    import requests
    resp = requests.get("https://raw.githubusercontent.com/obreit/redi/master/files/never_gonna_give_you_up.txt")
    return [line.decode('UTF-8') for line in resp.iter_lines()]

# flatmap applies a function to each element of a list. The output of applying the function
# returns another list. flatmap then combines the "list of lists" into a single list.   
def flatmap(func, input_list):
    return list(itertools.chain.from_iterable(map(func, input_list)))

# This function applies some very basic normalization on an input string
def normalize(word):
    return word.strip().lower()

def never_gonna_give_you_up_count():
    lyrics = load_lyrics()
    word_counts = {}
    words = flatmap(lambda line: line.split(), lyrics)
    cleaned_words = map(normalize, words)
    for word in cleaned_words:
        word_counts[word] = word_counts.get(word, 0) + 1
    return sorted(word_counts.items(), key=lambda item: item[1], reverse=True)

# Python built-in way
# Python provides a Counter abstraction that can simplify all sort of counting use cases 
# https://docs.python.org/3/library/collections.html#collections.Counter

# Exercise 4 - Relation to Pandas
# Now we've looked a lot at different ways to modify lists and got an idea on how to use dictionary for useful stuff like 
# counting words in song lyrics. On a very basic level, a dictionary can also be used as a plain "data record".
# Look at this example of using a dictionary to define some basic info about football players

# We use this helper function to simplify and not having to repeat all the keys over and over
def footballer(name, age, team, strong_foot):
    return {'name': name, 'age': age, 'team': team, 'strong_foot': strong_foot}

# If you look at this dummy dataset of footballers you maybe already notice some similarity to a pandas DataFrame.
footballers_list = [
    footballer('lionel messi', 34, 'psg', 'left'),
    footballer('kylian mbappe', 22, 'psg', 'right'),
    footballer('robert lewandowski', 33, 'bayern munich', 'right'),
    footballer('christiano ronaldo', 36, 'manunited', 'right')
]

# In fact, on a conceptual level you can imagine that a DataFrame is like a list of dictionaries. This is of course a 
# simplification, because a DataFrame is a highly optimized and abstracted data structure that is useful in a variety of data analytics use cases.
# You should never use a list of dictionaries instead of a DataFrame. But to get an understanding and maybe a feeling of what happens
# behind the scenes, it's a useful comparison. 

# Let's set up a DataFrame based on the dummy dataset
import pandas as pd

footballers_df = pd.DataFrame.from_records(footballers_list)

# Check some operations and see how you'd do it on a simple list of dictionaries

# To get a certain "row" (i.e. footballer) in the dataset, you have to index the list
footballers_list[2]
footballers_df.iloc[2]

# To get a certain "column" (i.e. attribute) in the dataset, you have extract the field you're interested in by mapping over the list
list(map(lambda footballer: footballer['team'], footballers_list))
footballers_df['team']

# Get the team of the 3rd player
footballers_list[2]['team']
footballers_df.loc[2, 'team'] 

# Get all players of psg
list(filter(lambda player: player['team'] == 'psg', footballers_list))
footballers_df[footballers_df['team'] == 'psg']

# Get the oldest player
ages = list(map(lambda player: player['age'], footballers_list))
max_age_index = ages.index(max(ages))
oldest_player = footballers_list[max_age_index]

max_age_index = footballers_df['age'].idxmax()
footballers_df.iloc[max_age_index]

# Try to compute the average age of each team. For the computation on the list, you can return a list of tuples (team, average age).
team_age_sum_count = {}
for player in footballers_list:
    current_sum, current_count = team_age_sum_count.get(player['team'], (0, 0))
    team_age_sum_count[player['team']] = (current_sum + player['age'], current_count + 1)
average_team_ages = [(team, age_sum / age_count) for team, age_sum, player_count in team_age_sum_count.items()]

footballers_df.groupby('team').mean('age')
    

