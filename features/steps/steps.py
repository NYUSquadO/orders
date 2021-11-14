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
BASE_URL = getenv('BASE_URL', 'http://localhost:5000/')

@given('the following orders')
def step_impl(context):
	""" Delete all Orders and load new ones """
	headers = {'Content-Type': 'application/json'}
	context.resp = requests.delete(context.base_url + '/orders/reset', headers=headers)
	expect(context.resp.status_code).to_equal(204)
	create_url = context.base_url + '/orders'
	for row in context.table:
		data = {
			"cust_id": row['cust_id'],
			"status": row['status'],
			"order_items": [{
				"id": row['id'],
				"order_id": row['order_id'],
				"item_id": row['item_id'],
				"item_name": row['item_name'],
				"item_qty":	 row['item_qty'],
				"item_price": row['item_price']
				}]
			}
		payload = json.dumps(data)
		context.resp = requests.post(create_url, data=payload, headers=headers)
		expect(context.resp.status_code).to_equal(201)

@when('I visit the "home page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)


@then('I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    expect(context.driver.title).to_contain(message)


@then('I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)