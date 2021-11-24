Feature: The order service back-end
    As a API User
    I need a RESTful catalog service
    So that I can keep track of all orders

Background:
    Given the following orders
        | id | cust_id | status     | order_id | item_id    | item_name   | item_qty | item_price   |
        |  1 | 72      | Placed     | 1        | 14         | switch      | 1        | 349.99       |
        |  2 | 11      | Cancelled  | 2        | 7          | cups        | 2        | 5.50         |
        |  3 | 14      | Default    | 3        | 71         | iPhone      | 1        | 849.99       |
        |  4 | 15      | Placed     | 4        | 72         | iPad        | 1        | 1099.50      |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order RESTful Service" in the title
    And I should not see "404 Not Found"


Scenario: Create an Order
    When I visit the "Home Page"    
    And I set the "cust_id" to "616"
    And I set the "item_id" to "7"
    And I set the "item_name" to "cups"
    And I set the "item_qty" to "5"
    And I set the "item_price" to "5.5"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Order_id" field
    And I press the "Clear" button
    Then the "Order_id" field should be empty
    When I paste the "Order_id" field
    And I press the "Retrieve" button
    Then I should see "7" in the "item_id" field
    And I should see "cups" in the "item_name" field
    And I should see "5" in the "item_qty" field
    And I should see "5.5" in the "item_price" field
    
Scenario: Retrieve an Order
    When I visit the "Home Page"    
    And I set the "cust_id" to "100"
    And I set the "item_id" to "1"
    And I set the "item_name" to "IPad"
    And I set the "item_qty" to "1"
    And I set the "item_price" to "999"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Order_id" field
    And I press the "Clear" button
    Then the "Order_id" field should be empty
    When I paste the "Order_id" field
    And I press the "Retrieve" button
    Then I should see "100" in the "cust_id" field
    And I should see "1" in the "item_id" field
    And I should see "IPad" in the "item_name" field
    And I should see "1" in the "item_qty" field
    And I should see "999" in the "item_price" field

Scenario: Delete an Order
    When I visit the "Home Page"
    And I set the "order_id" to "1"
    And I press the "Delete" button
    Then I should see the message "Order has been Deleted!"

Scenario: Order Id not found in Cancel an Order
    When I visit the "Home Page"
    And I set the "Order_id" to "100"
    And I press the "Cancel" button
    Then I should see the message "No orders found!"

Scenario: Cancel an Order
    When I visit the "Home Page"
    And I set the "cust_id" to "100"
    And I set the "item_id" to "1"
    And I set the "item_name" to "IPad"
    And I set the "item_qty" to "1"
    And I set the "item_price" to "999"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Order_id" field
    And I press the "Cancel" button
    Then I should see the message "Order has been Cancelled!"


Scenario: Update an Order
    When I visit the "Home Page"    
    And I set the "cust_id" to "100"
    And I set the "item_id" to "1000"
    And I set the "item_name" to "Apple"
    And I set the "item_qty" to "10"
    And I set the "item_price" to "5"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Order_id" field
    And I press the "Clear" button
    Then the "Order_id" field should be empty
    When I paste the "Order_id" field
    And I press the "Retrieve" button
    Then I should see "100" in the "cust_id" field
    And I should see "1000" in the "item_id" field
    And I should see "Apple" in the "item_name" field
    And I should see "10" in the "item_qty" field
    And I should see "5" in the "item_price" field
    When I set the "cust_id" to "200"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Order_id" field
    And I press the "Clear" button
    Then the "Order_id" field should be empty
    When I paste the "Order_id" field
    And I press the "Retrieve" button
    Then I should see "200" in the "cust_id" field


Scenario: List all order
    When I visit the "Home Page"
    And I press the "List" button
    Then I should see the message "Success"
    And I should see "1" in the search results
    And I should see "2" in the search results
    And I should see "3" in the search results
    And I should see "4" in the search results
    
Scenario: Query an Order by cust_id
    When I visit the "Home Page"    
    And I set the "cust_id" to "72"
    And I press the "Search" button
    Then I should see "72" in the "cust_id" field
    And I should see "switch" in the "item_name" field
    And I should see "14" in the "item_id" field
    And I should see "1" in the "item_qty" field
    And I should see "349.99" in the "item_price" field
