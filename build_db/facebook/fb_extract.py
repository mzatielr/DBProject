# -*- coding: utf-8 -*-

import sys
import copy
import facebook
import json


def populate_db():
    with open('data.json') as data_file:
        data = json.load(data_file)

        # See types of event fields here:
        # https://developers.facebook.com/docs/graph-api/reference/event/
        if __name__ == '__main__':
            for event in data.values():

                # Event parameters
                event_id = event.get('id', None)
                event_name = event.get('name', None)
                event_category = event.get('category', None)  # Enum of categories, see API link above
                event_description = event.get('description', None)
                event_start_time = event.get('start_time', None)  # Time format is String here, convert to DB time format..
                event_end_time = event.get('end_time', None)
                event_timezone = event.get('timezone', None)
                event_updated_time = event.get('updated_time', None)
                event_attending_count = event.get('attending_count', None)
                event_declined_count = event.get('declined_count', None)
                event_maybe_count = event.get('maybe_count', None)
                event_noreply_count = event.get('noreply_count', None)
                event_can_guests_invite = event.get('can_guests_invite', None)
                event_guest_list_enabled = event.get('guest_list_enabled', None)
                event_is_canceled = event.get('is_canceled', None)
                event_ticket_uri = event.get('ticket_uri', None)  # Link to buy tickets, string format

                # Events have cover photos
                cover_id = event.get('cover', None).get('id', None)  # Event cover photo id
                cover_url = event.get('cover', None).get('source', None)  # Event cover photo url, need to access and download image raw bytes

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

                else:   # Null out unused params, so they don't get confused with other entries!
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

                with open(event_id + '_comments.json') as comments_file:
                    comments_data = json.load(comments_file)
                    for comment in comments_data['data']:
                        if 'message' not in comment:
                            continue    # Ignore comments with no text for our purpose
                        comment_id = comment['id']              # Comment id, unique for each comment
                        comment_msg = comment['message']        # Comment message data
                        comment_time = comment['updated_time']  # Comment update time

                # ===========================================================
                # TODO: Put your SQL commands of INSERT INTO TABLE etc, here!
                # ===========================================================
                # Example of usage: --- (delete this, replace with SQL:)
                print("Event name: " + event_name)
                print("Event id: " + event_id)
                print("Event category: " + (" None" if event_category is None else event_category))
                print("Place name: " + (" None" if place_name is None else place_name))
                print("Location city: " + (" None" if location_city is None else location_city))
                print("Top comment:" + comments_data['data'][0]['message'])
                print()


def extract_data():
    """
    Fetched using Facebook Python API: http://facebook-sdk.readthedocs.io/en/latest/install.html
    """

    # Get access token from: https://developers.facebook.com/tools/debug/accesstoken/
    user_token = '-- FILL YOUR OWN HERE --'
    app_token = '190441714759199|QdoMmLvHYEUzSeeLyPK4Awg6Zv4'
    graph = facebook.GraphAPI(access_token=app_token, version='2.2')

    event_ids = []

    with open('keywords.txt') as keywords_file:
        for key in keywords_file:
            search_results = graph.request("search",
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
                                              'ticket_uri,updated_time')

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


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Incorrect Usage. Try:")
        print("python db_extract download_data // harvests selected events from facebook to local Json files")
        print("python db_extract populate_db // Populates DB with data stored in Json files")
        exit(1)

    cmd = sys.argv[1]

    if cmd == 'download_data':
        extract_data()
    elif cmd == 'populate_db':
        populate_db()
    else:
        print("Incorrect Usage. Try:")
        print("python db_extract download_data // harvests selected events from facebook to local Json files")
        print("python db_extract populate_db // Populates DB with data stored in Json files")
        exit(1)

