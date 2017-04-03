from errbot.version import VERSION
from errbot.utils import version2array
if version2array(VERSION) >= [1, 6, 0]:
  from errbot import botcmd, BotPlugin
else:
  from errbot.botplugin import BotPlugin
  from errbot.jabberbot import botcmd
from funbotconfig import weatherKey, yelpConsumer, yelpSecret, yelpToken, yelpTokenSecret, indeedID
import datetime
import time
import os
import json
import requests
import urllib
from xml.dom import minidom
from requests_oauthlib import OAuth1




__author__ = "Anthony Lazam"


class FunBot(BotPlugin):

    @botcmd
    def weather(self, mess, args):
        """ List the weather.
        Example: !weather cavite
        """
        hours_left = ((24 - datetime.datetime.now().hour) % 3 ) + 4
        base_url = "http://api.openweathermap.org/data/2.5/weather?q=" + args + "&APPID=" + weatherKey +"&units=Metric"
        days_base_url = "http://api.openweathermap.org/data/2.5/forecast?q=" + args + "&APPID=" + weatherKey +"&units=Metric"
        rqst = requests.get(base_url)
        days_rqst = requests.get(days_base_url)
        message = "The weather in " + args + " is " + str(rqst.json()['main']['temp']) + "C with a " + str(rqst.json()['weather'][0]['description']) + ".\n" + \
            "Here's temperature for the next few days in " + args + ".\n " + \
            "For " + str(days_rqst.json()['list'][hours_left]['dt_txt']).split()[0].split()[0] + " the temperature is " + str(days_rqst.json()['list'][hours_left]['main']['temp']) + "C with a " + str(days_rqst.json()['list'][hours_left]['weather']).split('\'')[9] + "\n" \
            "For " + str(days_rqst.json()['list'][hours_left+8]['dt_txt']).split()[0].split()[0] + " the temperature is " + str(days_rqst.json()['list'][hours_left+8]['main']['temp']) + "C with a " + str(days_rqst.json()['list'][hours_left+8]['weather']).split('\'')[9] + "\n" \
            "For " + str(days_rqst.json()['list'][hours_left+16]['dt_txt']).split()[0].split()[0] + " the temperature is " + str(days_rqst.json()['list'][hours_left+16]['main']['temp']) + "C with a " +  str(days_rqst.json()['list'][hours_left+16]['weather']).split('\'')[9] + "\n"
        return message

    @botcmd(split_args_with=None)
    def food(self, mess, args):
        """ List the food available in particular area
        Example: !food pizza bacoor
        """
        message = "```"
        message += self.yelp_request(args[0], args[1])
        message += "```"
        return message

    def yelp_request(self, term, location):
        message = ""
        auth = OAuth1(yelpConsumer, yelpSecret, yelpToken, yelpTokenSecret)
        base_url = 'https://api.yelp.com/v2/search'
        params = {
            "term": term,
            "location": location,
        }
        rqst = requests.get(base_url, auth=auth, params=params)
        for i in rqst.json()["businesses"]:
            message += "\n" + str((i["name"])) + " (" + str((i["rating"])) + " rating)\n" + \
            ''.join(str(e) + " " for e in (i["location"]["display_address"])) + "\n"
        return message

    @botcmd(split_args_with=None)
    def job(self, mess, args):
        """ List the job available in particular area.
        Usage: !job $query $country or !job $query $country $city
        Example: !job linux ph or !job linux ph makati
        """
        message = ""
        if len(args) == 3:
            message += self.indeed_request(args[0], args[1], args[2])
        elif len(args) == 2:
            message += self.indeed_request(args[0], args[1])
        else:
            return "Wrong Input. Please see help."
        return message

    #def indeed_request(self, query, country, location):
    def indeed_request(*args):
        message = ""
        base_url = "http://api.indeed.com/ads/apisearch?publisher=%s&v=2" % (indeedID)
        params = {
            "q": args[1],
            "co": args[2],
            "limit": '25',
            "format": 'json',
        }
        if len(args) == 4:
            params['l'] = args[3]
        rqst = requests.get(base_url, params=params)
        for i in rqst.json()["results"]:
            message += "\n `Job Title:` " + str(i["jobtitle"]) + \
                       "\n `Company:` " + str(i["company"]) + \
                       "\n `City:` " + str(i["city"]) + \
                       "\n `URL:` " + str(i["url"])
        return message
