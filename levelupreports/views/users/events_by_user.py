"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from levelupreports.views.helpers import dict_fetch_all
from operator import itemgetter

class UserEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
                SELECT
                    e.id,
                    e.description,
                    e.date,
                    e.organizer_id,
                    g.name AS game_name,
                    u.first_name || " " || u.last_name AS full_name
                FROM
                    levelupapi_event e
                JOIN
                    levelupapi_game g ON g.id = e.game_id
                JOIN
                    levelupapi_gamer gmr ON gmr.id = e.organizer_id
                JOIN
                    auth_user u ON gmr.user_id = u.id
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each gamer.
            # This will be the structure of the events_by_user list:
            #
            # [
            #   {
            #     "gamer_id": 1,
            #     "full_name": "Molly Ringwald",
            #     "events": [
            #       {
            #         "id": 5,
            #         "date": "2020-12-23",
            #         "time": "19:00",
            #         "game_name": "Fortress America"
            #       }
            #     ]
            #   }
            # ]

            events_by_user = []

            for row in dataset:
                # TODO: Create a dictionary called game that includes 
                # the name, description, number_of_players, maker,
                # game_type_id, and skill_level from the row dictionary
                event = {
                    'id': row['id'],
                    'description': row['description'],
                    'date': row['date'],
                    'game_name': row['game_name']
                }
                
                # See if the gamer has been added to the games_by_user list already
                user_dict = None
                for user_event in events_by_user:
                    if user_event['gamer_id'] == row['organizer_id']:
                        user_dict = user_event
                
                
                if user_dict:
                    # If the user_dict is already in the games_by_user list, append the game to the games list
                    user_dict['events'].append(event)
                else:
                    # If the user is not on the games_by_user list, create and add the user to the list
                    events_by_user.append({
                        "gamer_id": row['organizer_id'],
                        "full_name": row['full_name'],
                        "events": [event]
                    })
            #this orders the results from highest gamer id to lowest since reverse=True outside of x definition. Here to test ability to reorder list.
            events_by_user = sorted(events_by_user, key=lambda x: x['gamer_id'], reverse=True)
            # how to sort by games within list without a for loop?
            for user in events_by_user:
                user['events'] = sorted(user['events'], key=lambda x: x['date'], reverse=True)

        # The template string must match the file name of the html template
        template = 'users/list_with_events.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "userevent_list": events_by_user
        }

        return render(request, template, context)
