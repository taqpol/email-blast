# email-blast
simple script that filters and sends emails based on a user-defined phrase found in the body of emails in the inbox

<b>Overview:</b><br>
This script will search an inbox for a user-defined string, and send an email to any email address that sent an email including that string. Uses include notifying a large amount of users of a secret event...and not much else. 

<b>Requirements:</b><br>
-Python 3.x.x. All imports should be included in the base installation.
-An internet connection

<b>Outstanding Issues:</b><br>
-Search efficiency is hindered due to the script searching the entire inbox. This may be prohibitively time-consuming as the inbox grows larger and larger. A fix may be in the works that allows the user to define a date range through which to search.

<b>Usage:</b><br>
Simply run the script from any environment, whether it be an IDE or the command line. The script will guide the user through the entire process, can be terminated at any time within the script, and will provide last-minute confirmation of any actions undertaken.
