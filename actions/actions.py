# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from __future__ import print_function
from rasa_sdk.events import AllSlotsReset
import datetime
from datetime import datetime, timedelta
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle
import joblib
from typing import Text, List, Any, Dict
from rasa_sdk.events import SlotSet
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from joblib import dump, load
import numpy as np
import webbrowser


# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class AddEventToCalendar(Action):

    def name(self) -> Text:
        return "action_add_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        event_name = tracker.get_slot('event')
        time = tracker.get_slot('time')
        new_time = datetime.strptime(time, '%d/%m/%y %H:%M:%S')

        add_event(event_name, new_time)

        dispatcher.utter_message(text="Event Added")

        return [AllSlotsReset()]


# class getEvent(Action):
#
#     def name(self) -> Text:
#         return "action_get_event"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         event_name = get_event()
#
#         print(event_name)
#         # confirmed_event = tracker.get_slot(Any)
#         dispatcher.utter_message(text="got events {name}".format(name=event_name))
#         return []
#
#
 # If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = "D:\SAGE\SAGE_Rendezvous\credentials.json"


def get_calendar_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)
    return service



def add_event(event_name, time):
    # creates one hour event tomorrow 10 AM IST
    service = get_calendar_service()

    #    d = datetime.now().date()
    #    tomorrow = datetime(d.year, d.month, d.day, 10)+timedelta(days=1)
    #    start = tomorrow.isoformat()
    end = (time + timedelta(hours=1)).isoformat()

    event_result = service.events().insert(calendarId='primary',
                                           body={
                                               "summary": event_name,
                                               "description": 'This is a tutorial example of automating google calendar with python',
                                               "start": {"dateTime": time.isoformat(), "timeZone": 'Asia/Kolkata'},
                                               "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                                           }
                                           ).execute()

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])
    return []


# def get_event():
#     service = get_calendar_service()
#     now = datetime.utcnow().isoformat() + 'Z'
#     events = service.events().list(calendarId='primary', timeMin=now,
#                                    maxResults=10, singleEvents=True,
#                                    orderBy='startTime').execute().get("items", [])
#
#     print(events[0]["summary"])
#     return events[0]["summary"]


def do_event():
    service = get_calendar_service()
    now = datetime.utcnow().isoformat() + 'Z'
    events = service.events().list(calendarId='primary', timeMin=now,
                                   maxResults=10, singleEvents=True,
                                   orderBy='startTime').execute().get("items", [])

    print(events[0]["end"])
    return events[0]["end"]


# class ActionDoEvent(Action):
#
#     def name(self) -> Text:
#         return "action_do_event"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         event_name = do_event()
#
#         print(event_name)
#         # confirmed_event = tracker.get_slot(Any)
#         dispatcher.utter_message(text="got events {name}".format(name=event_name))
#         return []




class Redirect_Breathing(Action):
    def name(self) -> Text:
        return "action_breathing_video"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        video_link_breath = 'https://youtube.com/shorts/pdy3Zaw7NqA?feature=shared'
        webbrowser.open(video_link_breath, new=2)
        dispatcher.utter_message(
            text="Here is a video on breathing exercise"
        )
        return []

class Redirect_Grounding(Action):
    def name(self) -> Text:
        return "action_grounding_video"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        video_link_ground = 'https://www.youtube.com/watch?v=1ao4xdDK9iE&ab_channel=TherapyinaNutshell'
        webbrowser.open(video_link_ground, new=2)
        dispatcher.utter_message(
            text="Here is a video on grounding exercise"
        )
        return []

class SpotifyAnxietyPlaylist(Action):
    def name(self) -> Text:
        return "action_play_spotify_anxiety"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        video_link_ground = 'https://open.spotify.com/playlist/7hRK0jbnNo32nOjmCQqUjA?si=1d884ff7de78428e'
        webbrowser.open(video_link_ground, new=2)
        dispatcher.utter_message(
            text="Here is a special music playlist for calming you...Take your time and concentrate on listening."
        )
        return []



###STEIN ML CODES###


##login form

Talkative_opt = ['Talkative ','Reserved']
pref_list = ['Yes','No']
energ_drain_list = ['Energized ', 'Drained']
persuasion_list  = ['I like persuasion', 'Am not fond but ok with persuasion', 'I don’t like persuasion']
personal_invo_list = ['Low ', 'Medium ', 'High']

class AskForTalkativeAction(Action):
    def name(self) -> Text:
        return "action_ask_talk_or_resv"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
                text=f"Are you a talkative or reserved person?",
                buttons=[{"title": p, "payload": p} for p in Talkative_opt],
            )
        return []

class AskForPrefListAction(Action):
    def name(self) -> Text:
        return "action_ask_list_or_obsv"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
                text=f"Are you someone who prefers listening and observing more than actively participating in conversation?",
                buttons=[{"title": p, "payload": p} for p in pref_list],
            )
        return []

class AskForEnergisedOrDrainedAction(Action):
    def name(self) -> Text:
        return "action_ask_energ_or_drain"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
                text=f"Do you feel energized or drained after extended period of interaction?",
                buttons=[{"title": p, "payload": p} for p in energ_drain_list],
            )
        return []

class AskForPersuationAction(Action):
    def name(self) -> Text:
        return "action_ask_persuasion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
                text=f"Do you like being persuaded to do things?",
                buttons=[{"title": p, "payload": p} for p in persuasion_list],
            )
        return []

class AskForPrsnlInvolvAction(Action):
    def name(self) -> Text:
        return "action_ask_prsnl_invol"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
                text=f"How much of a personal involvement do you prefer from your friends while engaging in a conversation??",
                buttons=[{"title": p, "payload": p} for p in personal_invo_list],
            )
        return []

class ValidateUserProfileForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_profile_info_form"

    def validate_talk_or_resv(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `talk_or_resv` value."""
        return {"talk_or_resv": slot_value}

    def validate_list_or_obsv(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `list_or_obsv` value."""
        return {"list_or_obsv": slot_value}

    def validate_energ_or_drain(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `energ_or_drain` value."""
        return {"energ_or_drain": slot_value}

    def validate_persuasion(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `persuasion` value."""
        return {"persuasion": slot_value}

    def validate_prsnl_invol(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `prsnl_invol` value."""
        return {"prsnl_invol": slot_value}

##Classify User
talk_resrv_dict = {'Talkative':0,'Reserved':1}
prefers_listening_dict = {'Yes':1,'No':0}
Energised_or_Drained_dict = {'Drained':0,'Energized':1}
Persuasion_dict = {'I don’t like persuasion': 0,'Am not fond but ok with persuasion':1,'I like persuasion':2}
personal_involvement_dict	= {'Low':0,'Medium':1,'High':2}


inv_label_dict = {3:'Formal', 2:'Moderate', 1:'Personal'}
##mod1
class ClassifyUser(Action):
    def name(self) -> Text:
        return "action_classify_user"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        talk = tracker.get_slot('talk_or_resv')
        list_obsv = tracker.get_slot('list_or_obsv')
        energy_or_drain = tracker.get_slot('energ_or_drain')
        persuasion_or_not = tracker.get_slot('persuasion')
        prsnl_invol_or_not = tracker.get_slot('prsnl_invol')
        ftr_list = [talk_resrv_dict[talk], prefers_listening_dict[list_obsv],
                    Energised_or_Drained_dict[energy_or_drain], Persuasion_dict[persuasion_or_not],
                    personal_involvement_dict[prsnl_invol_or_not]]
        featurelist = np.array(ftr_list)
        featurelist = featurelist.reshape(1, 5)
        clf = joblib.load("D:\SAGE\SAGE_Rendezvous\SAGE_RECOMMENDER.joblib")

        def Classifier(feature_list):
            prediction_label = clf.predict(feature_list)
            prediction = inv_label_dict[prediction_label[0]]
            return prediction

        personality_val = Classifier(featurelist)
        return [SlotSet("personality", f'{personality_val}')]
