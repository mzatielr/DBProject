#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import copy
import facebook
import json
import MySQLdb

database_hostname = 'localhost'  # For NOVA use: 'mysqlsrv.cs.tau.ac.il'

# A mapping between Facebook Graph API Category ENUMS to our own app's category_id
categories = {
                'BOOK_EVENT': 1,
                'MOVIE_EVENT': 2,
                'FUNDRAISER': 3,
                'VOLUNTEERING': 4,
                'FAMILY_EVENT': 5,
                'FESTIVAL_EVENT': 6,
                'NEIGHBORHOOD': 7,
                'RELIGIOUS_EVENT': 8,
                'SHOPPING': 9,
                'COMEDY_EVENT': 10,
                'MUSIC_EVENT': 11,
                'DANCE_EVENT': 12,
                'NIGHTLIFE': 13,
                'THEATER_EVENT': 14,
                'DINING_EVENT': 15,
                'FOOD_TASTING': 16,
                'CONFERENCE_EVENT': 17,
                'MEETUP': 18,
                'CLASS_EVENT': 19,
                'LECTURE': 20,
                'WORKSHOP': 21,
                'FITNESS': 22,
                'SPORTS_EVENT': 23,
                'ART_EVENT': 24,
                'OTHER': 999
            }


def category_enum_to_id(category_enum):

    if category_enum is None:
        return 777  # Empty facebook ids are represented by special 777 id

    category_id = categories[category_enum.encode('UTF-8')]

    if category_id is None:
        return 777  # Avoid unknown categories by identifying them as empty as well

    return category_id


def populate_categories(cur, con):
    """ Populates the database with the category names and ids """

    category_fields = 'id,  name'
    insert_query = 'INSERT INTO Category (' + category_fields + ') VALUES (%s, %s)'

    for category_name, category_id in categories.iteritems():
        parameters = (long(category_id),
                      category_name.encode('UTF-8'))
        cur.execute(insert_query, parameters)
    con.commit()

def populate_db():

    with open('data.json', 'r') as data_file:
        data = json.load(data_file)

        # Connect to Database
        con = MySQLdb.connect(database_hostname, 'DbMysql08', 'DbMysql08', 'DbMysql08')
        with con:
            cur = con.cursor(MySQLdb.cursors.DictCursor)

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
                    place_id = event['place'].get('id', None)

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

                comment_id = None
                comment_msg = None
                comment_time = None
                comments_data = None
                try:
                    with open('COMMENTS/' + event_id + '_comments.json', 'r') as comments_file:
                        comments_data = json.load(comments_file)
                        for comment in comments_data['data']:
                            if 'message' not in comment:
                                continue  # Ignore comments with no text for our purpose
                            comment_id = comment['id']  # Comment id, unique for each comment
                            comment_msg = comment['message']  # Comment message data
                            comment_time = comment['updated_time']  # Comment update time
                except:
                    comment_id = None
                    comment_msg = None
                    comment_time = None

                # ===============================================================
                # -------- Database populated from this point onwards -----------
                # ===============================================================

                populate_categories(cur, con)  # Populate Category table

                # Populate Event table
                event_fields = 'id,  attending_count, declined_count, maybe_count, interested_count, ' \
                               'noreply_count, is_canceled, description, category_id, owner_id, place_id, ' \
                               'can_guest_invite, cover_source, guest_list_enabled, cover_id, ' \
                               'cover_offset_x, cover_offset_y, start_time, name, ' \
                               'end_time, update_time, timezone_id, event_type'

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
                              event_type.encode('UTF-8'))
                cur.execute(insert_query, parameters)

        con.commit()

        # ===========================================================
        # Example of usage: --- (delete this, replace with SQL:)
        # print('Event name: ' + event_name)
        # print('Event category: ' + (' None' if event_category is None else event_category))
        # print('Place name: ' + (' None' if place_name is None else place_name.encode('utf8')))
        # print('Location city: ' + (' None' if location_city is None else location_city.encode('utf8')))
        # if(comments_data is not None):
        #	if(len(comments_data['data'])>0):
        #		if(comments_data['data'][0].get('message',None) is not None):
        #			#print('Top comment: ' + comments_data['data'][0].get('message',None).encode('utf8'))
        # print()

def extract_data():
    '''
    Fetched using Facebook Python API: http://facebook-sdk.readthedocs.io/en/latest/install.html
    '''

    # Get access token from: https://developers.facebook.com/tools/debug/accesstoken/
    user_token = 'EAACtNKrCNh8BAHUsS3u9xUU7F4lKFcmkZC4WzNueIu1JaVFMfhqiIBNxeGHqRE3hrjYqjIiF9ajzRumlNNK61Taq9gRESIfV6kDC7Hmrmb02Yf5FM0A2dgPuBjkwUglBjZBL3xT2BZCBZAGfq0b1MW0ZAFkdlUzPpnkX6h74usAZDZD'
    app_token = '190441714759199|QdoMmLvHYEUzSeeLyPK4Awg6Zv4'
    graph = facebook.GraphAPI(access_token=app_token, version='2.2')

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
