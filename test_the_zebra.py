

import time
import pytest
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


# load program settings from json file
settings = json.load(open("settings.json"))
page_text_main = json.load(open('page_text_main.json'))

# load list of homes for which we will get insurance quotes
homes = []
homes_list = open('homes.txt').readlines()
keys = homes_list[0].split('|')

# build a list of dictionaries where each dictionary is one home's properties
for line in homes_list[1:]:

    values = line.split('|')
    h = {}

    for index in range(len(keys)):
        h[keys[index]] = values[index]

    homes.append(h)

options = Options()


@pytest.fixture(scope='class')
def setup_function(request):

    browser = webdriver.Chrome(executable_path='./chromedriver',
                               options=options)

    browser.maximize_window()
    browser.implicitly_wait(10)
    request.cls.driver = browser
    yield
    browser.quit()


@pytest.mark.usefixtures('setup_function')
class TestTheZebraMain:

    # assures that correct url loads
    def test_page_load(self):
        self.driver.get(settings['url'])
        assert self.driver.current_url == settings['url']

    # assures that text strings are present in correct container
    @pytest.mark.parametrize('text_main_header', page_text_main['header'])
    def test_text_main_page_header(self, text_main_header):
        assert text_main_header in self.driver.find_element_by_class_name('header').text, \
            f'Could not find this text in main page header - {text_main_header}'

    # assures that text strings are present in correct container
    @pytest.mark.parametrize('text_main_hero', page_text_main['hero'])
    def test_text_main_page_hero(self, text_main_hero):
        assert text_main_hero in self.driver.find_element_by_class_name('hero').text, \
            f'Could not find this text in main page hero headline- {text_main_hero}'

    # assures that text strings are present in correct container
    @pytest.mark.parametrize('text_main_how', page_text_main['how-zebra-works-container'])
    def test_text_main_page_how(self, text_main_how):
        assert text_main_how in self.driver.find_element_by_class_name('how-zebra-works-container').text, \
            f'Could not find this text in How zebra works container - {text_main_how}'


@pytest.mark.usefixtures('setup_function')
class TestTheZebraHomeQuote:

    @pytest.mark.parametrize('home', homes)
    def test_get_home_quote(self, home):

        self.driver.implicitly_wait(10)
        explicit_wait = 1

        # load main page
        self.driver.get('https://www.thezebra.com/')
        time.sleep(explicit_wait)

        # enter zip code
        self.driver.find_element_by_class_name('zipcode-text-input').send_keys(home['zip'])

        # click on home insurance button
        for i in self.driver.find_elements_by_class_name('radio-button-label'):
            if 'Home' in i.text:
                i.click()
                break

        time.sleep(explicit_wait)

        # click start
        self.driver.find_element_by_class_name('form-inline-submit-button').click()
        time.sleep(explicit_wait)

        # make sure browser moved on to the next page
        assert "We'll make this fast & simple." in self.driver.find_element_by_class_name('section-page-enter-done').text

        # accepted home types -  SINGLE_FAMILY, CONDO, RENTAL, MOBILE_HOME
        if home["type"] not in ['SINGLE_FAMILY', 'CONDO', 'RENTAL', 'MOBILE_HOME']:
            raise Exception('Invalid home type - SINGLE_FAMILY, CONDO, RENTAL, MOBILE_HOME ')

        # select residence type
        self.driver.find_element_by_id(f'residence_type-{home["type"]}').send_keys(Keys.ENTER)
        time.sleep(explicit_wait)

        # enter address, zip code
        self.driver.find_element_by_id('address1Input').click()
        self.driver.find_element_by_id('address1Input').send_keys(home['address'])
        self.driver.find_element_by_id('address1Input').send_keys(Keys.ENTER)
        self.driver.find_element_by_id('zipcode-input').send_keys(home['zip'])

        # select ownership, accepted input - OWN, PENDING, REFINANCING, JUST_LOOKING
        if home['ownership'] not in ['OWN', 'PENDING', 'REFINANCING', 'JUST_LOOKING']:
            raise Exception("Wrong ownership status, accepted input - OWN, PENDING, REFINANCING, JUST_LOOKING")

        ownership_status_button = self.driver.find_element_by_id(f'home_purchase_status-{home["ownership"]}')
        self.driver.execute_script("arguments[0].scrollIntoView();", ownership_status_button)
        ownership_status_button.send_keys(Keys.ENTER)
        time.sleep(explicit_wait)

        # enter purchase date
        purchase_date_input = self.driver.find_element_by_id('purchase_date-input')
        self.driver.execute_script("arguments[0].scrollIntoView();", purchase_date_input)
        purchase_date_input.send_keys(home['purchase_date'])

        # press save and continue
        self.driver.find_element_by_class_name('btn-continue').click()
        time.sleep(explicit_wait)

        # make sure we are on a different page
        assert "Let's build your protection from the foundation, up!" in self.driver.page_source

        # enter year of construction
        self.driver.find_element_by_id('year_built-input').send_keys(home['year_built'])

        time.sleep(explicit_wait)

        # select foundation type
        self.driver.find_element_by_xpath('//*[@id="foundation_type"]/div[2]/div/span').click()

        time.sleep(explicit_wait)

        foundation_indexes = {
            'Slab': 1,
            'Crawl space': 2,
            'Basement': 3,
            'Pier and beam': 4,
            'Other': 5
        }

        if home['foundation'] == 'Slab':
            self.driver.find_element_by_xpath(
            f'/html/body/div[1]/div/div[3]/main/div/form/div[1]/div[2]/div/div[2]/div/div/div['
            f'{foundation_indexes[home["foundation"]]}]').click()

        time.sleep(explicit_wait)

        # select frame type
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[3]/main/div/form/div[1]/div[3]/div/div[2]/div').click()

        time.sleep(explicit_wait)

        frame_indexes = {
            'Wood frame': 1,
            'Masonry': 2,
            'Concrete': 3,
            'Log': 4,
            'Other': 5
        }

        self.driver.find_element_by_xpath(
            f'/html/body/div[1]/div/div[3]/main/div/form/div[1]/div[3]/div/div[2]/div/div/div['
            f'{frame_indexes[home["frame"]]}]').click()

        # select number of stories
        stories_dropdown = self.driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[3]/main/div/form/div[1]/div[4]/div/div[2]/div/span")

        stories_dropdown.click()

        time.sleep(explicit_wait)

        if int(home['stories']) <= 4:
            stories = int(home['stories'])

        else:
            stories = 4

        self.driver.find_element_by_xpath(
            f'//*[@id="number_of_stories"]/div[2]/div/div/div[{stories}]').click()

        time.sleep(explicit_wait)

        # select heating type
        heater_types = {
            "Forced air": 1,
            "Electric": 2,
            "Boiler": 3,
            "Wood stove": 4,
            "No central heat source": 5,
            "Other": 6
        }

        self.driver.find_element_by_xpath('//*[@id="heat_type"]/div[2]/div').click()
        time.sleep(explicit_wait)
        self.driver.find_element_by_xpath(f'//*[@id="heat_type"]/div[2]/div/div/div[{heater_types[home["heating"]]}]').click()
        time.sleep(explicit_wait)

        # select roof material
        roof_materials = {
            'Asphalt composition': 1,
            'Wood': 2,
            'Tile': 3,
            'Metal': 4,
            'Slate': 5,
            'Other': 6
        }

        self.driver.find_element_by_xpath('//*[@id="roof_material"]/div[2]/div/span').click()
        time.sleep(explicit_wait)
        self.driver.find_element_by_xpath(f'//*[@id="roof_material"]/div[2]/div/div/div[{roof_materials[home["roof_material"]]}]').click()
        time.sleep(explicit_wait)

        # enter roof year
        self.driver.find_element_by_id('roof_improvement_year-input').send_keys(home['roof_installed'])
        time.sleep(explicit_wait)

        # enter square footage
        self.driver.find_element_by_id('square_footage-input').send_keys(home['square_footage'])
        time.sleep(explicit_wait)

        # enter rebuild cost
        self.driver.find_element_by_id('replacement_amount-input').send_keys(home['rebuild_cost'])
        time.sleep(explicit_wait)

        # select flood zone
        if home['flood_zone'] == 'Yes':
            self.driver.find_element_by_xpath('//*[@id="is_in_flood_zone"]/div[2]/label[1]/div/span[2]').click()

        elif home['flood_zone'] == 'No':
            self.driver.find_element_by_xpath('//*[@id="is_in_flood_zone"]/div[2]/label[2]/div/span[2]').click()

        time.sleep(explicit_wait)

        # select fire hydrant distance
        hydrant_choices = {
            'Yes': 1,
            'No': 2,
            "I'm not sure": 3
        }

        self.driver.find_element_by_xpath(
            f'//*[@id="is_fire_hydrant_available"]/div[2]/label[{hydrant_choices[home["fire_hydrant"]]}]/div/span[2]').click()

        time.sleep(explicit_wait)

        # select fire station distance
        fire_station = {
            '1-5 miles': 1,
            '5-10 miles': 2,
            '10+ miles': 3
        }

        self.driver.find_element_by_xpath(
            f'//*[@id="fire_station_proximity"]/div[2]/label[{fire_station[home["fire_station"]]}]/div/span[2]').click()

        time.sleep(explicit_wait)

        # click save & continue
        self.driver.find_element_by_class_name('btn-continue').click()
        time.sleep(explicit_wait)

        # make sure we moved onto next page
        assert "Let's personalize your quotes!" in self.driver.page_source

        # enter first and name, dob, email
        self.driver.find_element_by_id('first_name-input').send_keys(home['first_name'])
        time.sleep(explicit_wait)

        self.driver.find_element_by_id('last_name-input').send_keys(home['last_name'])
        time.sleep(explicit_wait)

        self.driver.find_element_by_id('date_of_birth-input').send_keys(home['dob'])
        time.sleep(explicit_wait)

        self.driver.find_element_by_id('email-input').send_keys(home['email'])
        time.sleep(explicit_wait)

        self.driver.find_element_by_class_name('btn-continue').click()
        time.sleep(explicit_wait)

        # make sure correct page is displayed while quotes are being requested
        assert 'Searching for the best rates for you.' in self.driver.page_source

        time.sleep(12)

        # make sure user can get to quotes page
        assert "Your quotes from top companies!" in self.driver.page_source

        # make sure at least one carrier quote is shown
        quote_boxes = self.driver.find_elements_by_class_name('carrier-info')
        assert len(quote_boxes) > 0

