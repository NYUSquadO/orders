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