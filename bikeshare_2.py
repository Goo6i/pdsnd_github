import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    This function will Ask user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    global city_input
    global day_input
    global month_input
    day = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    month = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    city = ['chicago', 'new york city', 'washington']

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_input = input('Select one city from the following: Chicago, New York City, or Washington').lower()
        if city_input not in city:
            print('Please choose one of the mentioned cities and check your spelling then try again.', end = '')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month_input = input('Select one month from the following: January, February, March, April, May, June, All').lower()
        if month_input not in month:
            print('Please choose one of the mentioned months and check your spelling then try again.', end = '')
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_input = input('Select one day from the following: sunday, monday, tuesday, wednesday, thursday, friday, saturday, All').lower()
        if day_input not in day:
            print('Please choose one of the mentioned days and check your spelling then try again.', end = '')
            continue
        else:
            break

    print('-'*40)
    return city_input, month_input, day_input


def load_data(city, month, day):
    """
    This function will load data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day to create the new dataframe
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """This function will display statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # displays the most common month
    common_month = df['month'].mode()[0]
    print('Most common month is: ', common_month)

    # displays the most common day of week
    common_day =  df['day_of_week'].mode()[0]
    print('Most common day of the week is: ', common_day)
    # displays the most common start hour
    common_hour =  df['hour'].mode()[0]
    print('Most common start hour is: ', common_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """This function will display statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # displays most commonly used start station
    common_st_station = df.loc[:,'Start Station'].mode()[0]

    print('Most commonly used start station is: ', common_st_station)
    # displays most commonly used end station
    common_end_station = df.loc[:,'End Station'].mode()[0]
    print('Most commonly used end station is: ', common_end_station)
    # displays most frequent combination of start station and end station trip
    common_st_end = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most common combination of start station and end station is: ', common_st_end)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """This function will display statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Trip Duration'] = df['End Time'] - df['Start Time']

    # displays total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is: ', total_travel_time)
    # displays mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('The average travel time is: ', average_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """This function will display statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    # Displays counts of gender
    if 'Gender' not in df.columns:
        print('There are no genders in this dataframe')

    else:
        gender_count = df['Gender'].value_counts()
        print('Gender count: ', gender_count)


    # Displays earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print('There are no birth years in this dataframe')

    else:
        min_birth = df['Birth Year'].min()
        print('Earliest date of birth:', min_birth)


    if 'Birth Year' not in df.columns:
        print('There are no Birth years in this dataframe')

    else:
        max_birth = df['Birth Year'].max()
        print('Most recent birth year is:', max_birth)


    if 'Birth Year' not in df.columns:
        print('There are no birth years in this dataframe')

    else:
        birth_count = df['Birth Year'].mode()[0]
        print('Most common birth year', birth_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
