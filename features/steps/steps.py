"""
Order Steps
Steps file for orders.feature
"""
from os import getenv
import json
import requests
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

WAIT_SECONDS = 120
#BASE_URL = getenv('BASE_URL', 'http://localhost:5000/')

@when('I visit the "home page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)
	# Uncomment next line to take a screenshot of the web page
    context.driver.save_screenshot('home_page.png')


@then('I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    print(context.driver.title)
    expect(context.driver.title).to_contain(message)


@then('I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)

@given('the following orders')
def step_impl(context):
	""" Delete all Orders and load new ones """
	headers = {'Content-Type': 'application/json'}
	# list all of the orders and delete them one by one
	context.resp = requests.get(context.base_url + '/orders', headers=headers)
	expect(context.resp.status_code).to_equal(200)
	for order in context.resp.json():
		context.resp = requests.delete(context.base_url + '/orders/' + str(order["id"]), headers=headers)
		expect(context.resp.status_code).to_equal(204)

	# load the database with new orders
	create_url = context.base_url + '/orders'
	for row in context.table:
		
		data = {
			"cust_id": int(row['cust_id']),
			"status": row['status'],
			"order_items": [{
				"id": int(row['id']),
				"order_id": int(row['order_id']),
				"item_id": int(row['item_id']),
				"item_name": row['item_name'],
				"item_qty":	 int(row['item_qty']),
				"item_price": float(row['item_price'])
				}]
			}
		#print(create_url)
		payload = json.dumps(data)
		context.resp = requests.post(create_url, data=payload, headers=headers)
		expect(context.resp.status_code).to_equal(201)
		#print(context.resp.status_code)

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'

    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.element_to_be_clickable(
            (By.ID, button_id)
        )
    )
    element.click()

@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    expect(found).to_be(True)

