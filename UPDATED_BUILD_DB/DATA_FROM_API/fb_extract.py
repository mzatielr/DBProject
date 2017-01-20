#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback
import copy
import facebook
import json
import MySQLdb
from requests.exceptions import ConnectionError
import time

database_hostname = 'localhost'  # For NOVA use: 'mysqlsrv.cs.tau.ac.il'

# A mapping between Facebook Graph API Category ENUMS to our own app's category_id
categories = {
                'BOOK_EVENT': (1, 'Books'),
                'MOVIE_EVENT': (2, 'Movies'),
                'FUNDRAISER': (3, 'Fund Raising'),
                'VOLUNTEERING': (4, 'Volunteering'),
                'FAMILY_EVENT': (5, 'Family Event'),
                'FESTIVAL_EVENT': (6, 'Festival'),
                'NEIGHBORHOOD': (7, 'Neighborhood'),
                'RELIGIOUS_EVENT': (8, 'Religious'),
                'SHOPPING': (9, 'Shopping'),
                'COMEDY_EVENT': (10, 'Comedy'),
                'MUSIC_EVENT': (11, 'Music'),
                'DANCE_EVENT': (12, 'Dancing'),
                'NIGHTLIFE': (13, 'Nightlife'),
                'THEATER_EVENT': (14, 'Threater'),
                'DINING_EVENT': (15, 'Dining'),
                'FOOD_TASTING': (16, 'Food'),
                'CONFERENCE_EVENT': (17, 'Conference'),
                'MEETUP': (18, 'Meetup'),
                'CLASS_EVENT': (19, 'Class Event'),
                'LECTURE': (20, 'Lecture'),
                'WORKSHOP': (21, 'Workshop'),
                'FITNESS': (22, 'Fitness'),
                'SPORTS_EVENT': (23, 'Sports'),
                'ART_EVENT': (24, 'Art'),
                'OTHER': (999, 'Misc')
            }


def category_enum_to_id(category_enum):

    if category_enum is None:
        return 999  # Empty facebook ids are represented by special other id

    category_id, category_name = categories[category_enum.encode('UTF-8')]

    if category_id is None:
        return 999  # Avoid unknown categories by identifying them as other as well

    return category_id


def populate_categories(cur, con):
    """ Populates the database with the category names and ids """

    print('Populating categories..')
    category_fields = 'id,  name'
    insert_query = 'INSERT INTO Category (' + category_fields + ') VALUES (%s, %s)'

    for category_name, (category_id, category_title) in categories.iteritems():
        parameters = (long(category_id),
                      category_title.encode('UTF-8'))
        try:
            cur.execute(insert_query, parameters)
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Category entry: " + str(category_id))

    con.commit()


def populate_timezones(cur, con, timezones):
    """ Populates the database with street entities """

    print('Populating tiemzones..')
    for timezone_name, timezone_id in timezones.iteritems():
        timezone_fields = 'id,  timezone'
        insert_query = 'INSERT INTO Timezone (' + timezone_fields + ') VALUES (%s, %s)'

        parameters = (long(timezone_id),
                      timezone_name.encode('UTF-8') if timezone_name is not None else None)
        try:
            cur.execute(insert_query, parameters)
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Timezone entry: " + str(timezone_id))

    con.commit()


def populate_streets(cur, con, streets):
    """ Populates the database with street entities """

    print('Populating streets..')
    for street_key, (street_id, location_street) in streets.iteritems():
        street_fields = 'id,  name'
        insert_query = 'INSERT INTO Street (' + street_fields + ') VALUES (%s, %s)'

        parameters = (long(street_id),
                      location_street.encode('UTF-8') if location_street is not None else None)
        try:
            cur.execute(insert_query, parameters)
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Street entry: " + str(street_id))

    con.commit()


def populate_places(cur, con, places):
    """ Populates the database with place entities """

    print('Populating places..')
    for place_id, (place_name, street_id, location_city_id, location_country_code, \
             location_zipcode, location_latitude, location_longitude) in places.iteritems():

        place_fields = 'id,  name, street_id, city_id, country_id, zip, latitude, longitude'
        insert_query = 'INSERT INTO Place (' + place_fields + ') VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

        parameters = (long(place_id),
                      place_name.encode('UTF-8') if place_name is not None else None,
                      long(street_id),
                      long(location_city_id),
                      long(location_country_code),
                      location_zipcode,
                      location_latitude,
                      location_longitude)
        try:
            cur.execute(insert_query, parameters)
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Place entry: " + str(place_id))

    con.commit()


def populate_cities(cur, con, cities):
    """ Populates the database with city entities """

    print('Populating cities..')
    for location_city, (city_id, country_id) in cities.iteritems():
        city_fields = 'id,  name, country_id'
        insert_query = 'INSERT INTO City (' + city_fields + ') VALUES (%s, %s, %s)'

        parameters = (long(city_id),
                      location_city.encode('UTF-8') if location_city is not None else None,
                      long(country_id))
        try:
            cur.execute(insert_query, parameters)
        except MySQLdb.IntegrityError:
            print("Skipping duplicate City entry: " + str(city_id))

    con.commit()


def populate_countries(cur, con, countries):
    """ Populates the database with country entities """

    print('Populating countries..')
    for location_country, country_id in countries.iteritems():
        country_fields = 'id,  name'
        insert_query = 'INSERT INTO Country (' + country_fields + ') VALUES (%s, %s)'

        parameters = (long(country_id),
                      location_country.encode('UTF-8') if location_country is not None else None)
        try:
            cur.execute(insert_query, parameters)
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Country entry: " + str(country_id))

    con.commit()


def populate_owners(cur, con, owners):
    """ Populates the database with owner entities """

    batch_size = 0

    print('Populating owners..')
    for owner_id, owner_name in owners.iteritems():
        owner_fields = 'id,  name'
        insert_query = 'INSERT INTO Owner (' + owner_fields + ') VALUES (%s, %s)'

        parameters = (long(owner_id),
                      owner_name.encode('UTF-8') if owner_name is not None else None)
        try:
            cur.execute(insert_query, parameters)
            batch_size += 1
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Owner entry: " + str(owner_id))

        # Commit in batches, to avoid errors on huge commits that may waste time..
        if batch_size >= 1000:
            con.commit()
            batch_size = 0

    if batch_size > 0:
        con.commit()


def populate_events(cur, con, events):
    """ Populates the database with the category names and ids """

    batch_size = 0

    print('Populating events..')
    for event_id, (event_attending_count, event_declined_count, event_maybe_count,event_interested_count, \
            event_noreply_count, event_is_canceled, event_description, event_category, event_owner_id, place_id, \
            event_can_guests_invite, cover_url, event_guest_list_enabled, cover_id, cover_offset_x, cover_offset_y, \
            event_start_time, event_name, event_end_time, event_updated_time, event_timezone, event_type) \
            in events.iteritems():

        event_fields = 'id,  attending_count, declined_count, maybe_count, interested_count, ' \
                       'noreply_count, is_canceled, description, category_id, owner_id, place_id, ' \
                       'can_guest_invite, cover_source, guest_list_enabled, cover_id, ' \
                       'cover_offset_x, cover_offset_y, start_time, name, ' \
                       'end_time, update_time, timezone_id, event_type'

        # MSQLdb doesn't treat this string as a normal Python SQL string, so all fields are considered %s
        # (this is not a mistake..)
        insert_query = 'INSERT INTO Event (' + event_fields + ') ' \
                       'VALUES (%s, %s, %s, %s, %s, %s, %s, ' \
                       '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
                       '%s, %s, %s, %s, %s, %s)'

        parameters = (long(event_id),
                      event_attending_count,
                      event_declined_count,
                      event_maybe_count,
                      event_interested_count,
                      event_noreply_count,
                      event_is_canceled,
                      event_description.encode('UTF-8') if event_description is not None else None,
                      category_enum_to_id(event_category),
                      long(event_owner_id) if event_owner_id is not None else 0,
                      long(place_id) if place_id is not None else 0,
                      event_can_guests_invite,
                      cover_url.encode('UTF-8') if cover_url is not None else None,
                      event_guest_list_enabled,
                      long(cover_id) if cover_id is not None else 0,
                      cover_offset_x,
                      cover_offset_y,
                      str(event_start_time),
                      event_name.encode('UTF-8') if event_name is not None else None,
                      str(event_end_time),
                      str(event_updated_time),
                      str(event_timezone),  # string
                      event_type.encode('UTF-8') if event_type is not None else None)

        try:
            cur.execute(insert_query, parameters)
            batch_size += 1
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Event entry: " + str(event_id))
            tb = traceback.format_exc()
            print(tb)

        # Commit in batches, to avoid errors on huge commits that may waste time..
        if batch_size >= 1000:
            con.commit()
            batch_size = 0

    if batch_size > 0:
        con.commit()


def populate_comments(cur, con, comments):
    """ Populates the database with comment entities """

    batch_size = 0

    print('Populating comments..')
    for comment_id, (comment_msg, comment_time, event_id) in comments.iteritems():
        comment_fields = 'id,  message, updated_time, event_id'
        insert_query = 'INSERT INTO Comment (' + comment_fields + ') VALUES (%s, %s, %s, %s)'

        parameters = (comment_id,
                      comment_msg.encode('UTF-8') if comment_msg is not None else None,
                      str(comment_time),
                      event_id)
        try:
            cur.execute(insert_query, parameters)
            batch_size += 1
        except MySQLdb.IntegrityError:
            print("Skipping duplicate Comment entry: " + str(comment_id))

        # Commit in batches, to avoid errors on huge commits that may waste time..
        if batch_size >= 1000:
            con.commit()
            batch_size = 0

    if batch_size > 0:
        con.commit()


def populate_db():

    # Connect to Database - we test the connection as early as possible.
    # We don't mind holding the connection open during parsing of Json files
    # since this is a one-time operation (in production code that runs on
    # the web-server we wouldn't do that, since that might create a bottleneck).
    con = MySQLdb.connect(database_hostname, 'DbMysql08', 'DbMysql08', 'DbMysql08', charset='utf8')
    with con:

        # These dictionaries accumulate meta data that multiple events may share, so we cache it until we're
        # done iterating our fetched events and comments.
        # Why we keep data in dictionaries: we want to avoid duplicate entries in the database.
        # Although the columns are defined as "UNIQUE" in sql, inserting duplicate primary keys will
        # trigger an integrity error, which we may catch and ignore.
        # Another alternative is do execute a COUNT query every time we want to insert a new city / country / etc
        # and check if it already exists in the database.
        # Both methods may prolong the population process since we execute additional queries to the db.
        # Instead we chose a simple solution of caching and inserting all at once.
        # Our chosen method requires modifications if it scales to huge amounts of data
        # (program may run out of heap memory, etc).
        places = {}
        streets = {}
        cities = {}
        countries = {}
        timezones = {}
        owners = {}

        # Also cache events and comments due to foreign key constraints. Must build above entities first.
        comments = {}
        events = {}

        with open('data.json', 'r') as data_file:
            data = json.load(data_file)

            # See types of event fields here:
            # https://developers.facebook.com/docs/graph-api/reference/event/
            for event in data.values():

                # Event parameters
                event_id = event.get('id', None)
                event_name = event.get('name', None)
                event_category = event.get('category', None)  # Enum of categories, see API link above
                event_description = event.get('description', None)
                event_start_time = event.get('start_time',
                                             None)  # Time format is String here, convert to DB time format..
                event_end_time = event.get('end_time', None)
                event_timezone = event.get('timezone', None)
                event_updated_time = event.get('updated_time', None)
                event_attending_count = event.get('attending_count', None)
                event_declined_count = event.get('declined_count', None)
                event_interested_count = event.get('interested_count', None)
                event_maybe_count = event.get('maybe_count', None)
                event_noreply_count = event.get('noreply_count', None)
                event_can_guests_invite = event.get('can_guests_invite', None)
                event_guest_list_enabled = event.get('guest_list_enabled', None)
                event_is_canceled = event.get('is_canceled', None)
                event_ticket_uri = event.get('ticket_uri', None)  # Link to buy tickets, string format
                event_owner = event.get('owner', None)

                if 'owner' in event:
                    event_owner_id = event_owner.get('id', None)
                    event_owner_name = event_owner.get('name', None)

                event_type = event.get('type', None)

                # Events have cover photos
                if (event.get('cover', None) is not None):
                    cover_id = event.get('cover', None).get('id', None)  # Event cover photo id
                    cover_offset_x = event.get('cover', None).get('offset_x', None)
                    cover_offset_y = event.get('cover', None).get('offset_y', None)

                    # Event cover photo url, need to access and download image raw bytes
                    cover_url = event.get('cover', None).get('source',
                                                             None)

                # Each event has a unique place it occurs in, multiple events can share places
                if 'place' in event:
                    place_id = event['place'].get('id', None)
                    place_name = event['place'].get('name', None)
                    place_rating = event['place'].get('overall_rating', None)

                    # Each place has a location, which describes it's geographical data
                    if 'location' in event['place']:
                        location_name = event['place']['location'].get('name', None)
                        location_region = event['place']['location'].get('region', None)
                        location_region_id = event['place']['location'].get('region_id', None)
                        location_city = event['place']['location'].get('city', None)
                        location_city_id = event['place']['location'].get('city_id', None)
                        location_country = event['place']['location'].get('country', None)
                        location_country_code = event['place']['location'].get('country_code', None)
                        location_latitude = event['place']['location'].get('latitude', None)
                        location_longitude = event['place']['location'].get('longitude', None)
                        location_street = event['place']['location'].get('street', None)
                        location_zipcode = event['place']['location'].get('zip', None)
                    else:  # Null out unused params, so they don't get confused with other entries!
                        location_name = None
                        location_region = None
                        location_region_id = None
                        location_city = None
                        location_city_id = None
                        location_country = None
                        location_country_code = None
                        location_latitude = None
                        location_longitude = None
                        location_street = None
                        location_zipcode = None

                else:  # Null out unused params, so they don't get confused with other entries!
                    place_id = None
                    place_name = None
                    place_rating = None
                    place_id = None
                    location_name = None
                    location_region = None
                    location_region_id = None
                    location_city = None
                    location_city_id = None
                    location_country = None
                    location_country_code = None
                    location_latitude = None
                    location_longitude = None
                    location_street = None
                    location_zipcode = None

                comment_msg = None
                comment_time = None
                comments_data = None
                try:
                    with open('COMMENTS/' + event_id + '_comments.json', 'r') as comments_file:
                        comments_data = json.load(comments_file)
                        if (comments_data is not None) and\
                           (len(comments_data['data']) > 0):
                            for comment in comments_data['data']:
                                if 'message' not in comment:
                                    continue  # Ignore comments with no text for our purpose

                                # Facebook's comment id is a string, we want ids to be integers so we
                                # generate our own sequential ids for comments.
                                comment_id = len(comments)  # Comment id, unique for each comment
                                comment_msg = comment['message']  # Comment message data
                                comment_time = comment['updated_time']  # Comment update time
                                comments[comment_id] = (comment_msg, comment_time, event_id)
                except:
                    pass  # Silently ignore, some events have no comment files

                # Country codes are no longer retrieved by facebook.
                # We have to generate an id of our own instead..
                if (location_country not in countries) and (location_country is not None):
                    country_id = len(countries)
                    countries[location_country] = country_id

                # Some attributes are not assigned ids by facebook so we have to assign them by ourselves.
                # The first time we populate the database, we treat those names as "keys" that belong to the same
                # ids in the database. In reality, the moment we're done populating the database, these names are
                # no longer keys and users may add additional streets with similar names (but not the
                # same ids).
                country_id = countries[location_country] if location_country in countries else -1
                if (location_city not in cities) and (location_city is not None):
                    city_id = len(cities)
                    cities[location_city] = (city_id, country_id)

                city_id = cities[location_city] if location_city in cities else -1
                street_key = (country_id, city_id, location_street)
                if (street_key not in streets) and (location_street is not None):
                    street_id = len(streets)
                    streets[street_key] = (street_id, location_street)  # Assign sequential ids

                if (place_id not in places) and (place_id is not None):
                    is_key_valid = (location_country_code is not None) \
                        and (location_city_id is not None) and (location_street is not None)
                    street_id = streets[street_key][0] if is_key_valid else -1
                    country_id = countries[location_country] if location_country in countries else -1
                    city_id = cities[location_city_id] if location_city_id in cities else -1
                    places[place_id] = (place_name, street_id, city_id, country_id, \
                                        location_zipcode, location_latitude, location_longitude)

                if (event_timezone not in timezones) and (event_timezone is not None):
                    timezones[event_timezone] = len(timezones)  # Assign sequential ids

                if (event_owner_id not in owners) and (event_owner_id is not None):
                    owners[event_owner_id] = event_owner_name

                if event_id is not None:
                    events[event_id] = (event_attending_count,
                                        event_declined_count,
                                        event_maybe_count,
                                        event_interested_count,
                                        event_noreply_count,
                                        event_is_canceled,
                                        event_description,
                                        event_category,
                                        event_owner_id,
                                        place_id,
                                        event_can_guests_invite,
                                        cover_url,
                                        event_guest_list_enabled,
                                        cover_id,
                                        cover_offset_x,
                                        cover_offset_y,
                                        event_start_time,
                                        event_name,
                                        event_end_time,
                                        event_updated_time,
                                        event_timezone,
                                        event_type)

            # ================================================================
            # ---- Most of the database populated from this point onwards ----
            # ================================================================

        # Create cursor for executing INSERT queries..
        cur = con.cursor(MySQLdb.cursors.DictCursor)

        try:
            populate_categories(cur, con)  # Populate Category table
        except Exception as err:
            print('Error populating categories entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_events(cur, con, events)
        except Exception as err:
            print('Error populating event entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_countries(cur, con, countries)
        except Exception as err:
            print('Error populating country entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_cities(cur, con, cities)
        except Exception as err:
            print('Error populating city entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_streets(cur, con, streets)
        except Exception as err:
            print('Error populating street entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_places(cur, con, places)
        except Exception as err:
            print('Error populating place entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_timezones(cur, con, timezones)
        except Exception as err:
            print('Error populating timezone entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_owners(cur, con, owners)
        except Exception as err:
            print('Error populating owner entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_events(cur, con, events)
        except Exception as err:
            print('Error populating event entities')
            tb = traceback.format_exc()
            print(tb)

        try:
            populate_comments(cur, con, comments)
        except Exception as err:
            print('Error populating comment entities')
            tb = traceback.format_exc()
            print(tb)

        print('Database population process done!')


def extract_data():
    '''
    Fetched using Facebook Python API: http://facebook-sdk.readthedocs.io/en/latest/install.html
    '''

    # Get access token from: https://developers.facebook.com/tools/debug/accesstoken/
    user_token = 'EAACtNKrCNh8BAPnr7PyzbBaJcwNq4ZA9h3KCGSRGXZBDbJZAZCt3pvWPcmWhjiz3KToTcZBv6zO4ttZCZCLZAElmaTiyQ93kg55kVqhZAVI4A0ko9VEZBmz12eykuwdUX2247W1jeVCC3BpwkBoIgE61ZA7GSYuN8ElSiMZD'
    app_token = '190441714759199|QdoMmLvHYEUzSeeLyPK4Awg6Zv4'
    graph = facebook.GraphAPI(access_token=app_token, version='2.2')

    print('Connected successfully to Facebook-GraphAPI..')
    print('Initiating event search queries by keywords:')

    event_ids = []
    with open('keywords.txt') as keywords_file:
        for key in keywords_file:
            print(key)
            search_results = graph.request('search',
                                           {'access_token': user_token,
                                            'q': key,
                                            'type': 'event'})['data']
            for entry in search_results:
                event_id = entry['id']
                if event_id not in event_ids:
                    event_ids.append(event_id)

    events = None

    print('Fetching comments from feed of each event..:')

    # A maximum of 50 ids is allowed per query, divide to multiple queries
    while len(event_ids) > 0:
        event_ids_batch = event_ids[:49]
        new_events = graph.get_objects(ids=event_ids_batch,
                                       fields='id,name,category,description,cover,' +
                                              'start_time,end_time,timezone,place,' +
                                              'attending_count,declined_count,maybe_count,' +
                                              'noreply_count,interested_count,' +
                                              'can_guests_invite,guest_list_enabled,is_canceled,' +
                                              'ticket_uri,updated_time,' +
                                              'owner,type')

        if events is None:
            events = copy.deepcopy(new_events)
        else:
            events.update(new_events)

        for event_id in event_ids_batch:
            try:
                # Ignore paging, fetch only a single page of comments
                comments = graph.get_connections(id=event_id, connection_name='feed')
                with open(event_id + '_comments.json', 'w') as comments_file:
                    json.dump(comments, comments_file, sort_keys=True, indent=4)
            except facebook.GraphAPIError:
                continue
            except ConnectionError:
                # Could happen when we exceed the max retries count..
                # Rest for one minute, then continue trying..
                print('Max retries exceeded with url.. Resting for 1 minute before retrying..')
                time.sleep(60)
                print('Retrying to fetch comments..')
                try:
                    # Ignore paging, fetch only a single page of comments
                    comments = graph.get_connections(id=event_id, connection_name='feed')
                    with open(event_id + '_comments.json', 'w') as comments_file:
                        json.dump(comments, comments_file, sort_keys=True, indent=4)
                except facebook.GraphAPIError:
                    print ('Facebook-graph error on feed for event: ' + str(event_id))
                    tb = traceback.format_exc()
                    print(tb)
                    continue
                except Exception:
                    print('General error on feed for event ' + str(event_id) + '.. Could not retry :(')
                    print('Proceeding to dump data.json, some comments may be missing')
                    tb = traceback.format_exc()
                    print(tb)
            except Exception:
                print('General error on feed for event ' + str(event_id))
                print('Proceeding to dump data.json, some comments may be missing')


        event_ids = event_ids[50:]

    # Each given id maps to an object the contains the requested fields.
    with open('data.json', 'w') as events_file:
        json.dump(events, events_file, sort_keys=True, indent=4)


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print('Incorrect Usage. Try:')
        print('python db_extract download_data // Harvests selected events from facebook to local Json files')
        print('python db_extract populate_db   // Populates DB with data stored in Json files')
        exit(1)

    cmd = sys.argv[1]

    if cmd == 'download_data':
        extract_data()
    elif cmd == 'populate_db':
        populate_db()
    else:
        print('Incorrect Usage. Try:')
        print('python db_extract download_data // Harvests selected events from facebook to local Json files')
        print('python db_extract populate_db   // Populates DB with data stored in Json files')
        exit(1)
