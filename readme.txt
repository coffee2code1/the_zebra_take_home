

===== The Zebra automation suite =====

This automation suite is designed the front end UI of thezebra.com website

Requirements
Python 3.7
selenium
pytest
chromedriver 84 (included
installed Chrome browser 84

Instructions
- Open terminal
- navigate to directory containing "test_the_zebra.py" file
- type in 'pytest'

Test description
- TestTheZebraMain -  this test reads expected elements list from page_text_main.json and assures that those elements
are present on the main page

- TestTheZebraHomeQuote - tests insurance quote UX flow for house quotas. It reads pipe delimited house/buyer info
from homes.txt and each line of information triggers one test run


Files
chromedriver 84 - necessary for driving chrome browser
homes.txt - contains a list of pipe delimited houses which can be easily manipulated and expanded by non engineers
page_text_main.json - lists elements which test suite tries to find on the main page. Each element is listed under
its container name
settings.json - provides an easy and convenient way to change some of the key settings of this test suite
