# Python-WebHarvester
Using BeautifulSoup in Python allows you to send bulk requests to a website for information and capture its responses. So for example, you have a list of phone numbers and you want the associated names, you can simply send off every number you have to a whitepages type website and gather the responses automatically and quickly. Now your partial list is complete!

To achieve this you simply must point the value_search values to wherever the response data is within the html. Then push a large dictionary (wordlist) towards the website in order to recieve your desired results.

It's nothing you can't already do with burpsuite, but I feel there are times its nice to have your own unique bespoke tool for a singular task.

You want to use it? Go for it, just modify the html parser and go!

Note this has threading and will run itself 10 times by default.

This code is not really optimised or fully tested, I made it for a CTF and left it once I got what I wanted.
