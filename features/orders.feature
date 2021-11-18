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
    And I set the "item_price" to "5.50"
    And I press the "Create" button
    Then I should see the message "Success"
    # When I copy the "id" field
    # And I press the "Clear" button
    # Then the "id" field should be empty
    # When I paste the "id" field
    # And I press the "Retrieve" button
    # And I should see "7" in the "item_id" field
    # And I should see "cups" in the "item_name"
    # And I should see "5" in the "item_qty"
    # And I should see "5.50" in the "item_price"
    
Scenario: Delete an Order
    When I visit the "Home Page"
    And I set the "order_id" to "1"
    And I press the "Delete" button
    Then I should see the message "Order has been Deleted!"
