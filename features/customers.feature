Feature: The pet store service back-end
    As a Customer Servicing Team
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
     | id    | name   | user_name | password |
     | 1     | name1  | uname1    | pwd1     |
     | 2     | name2  | uname2    | pwd2     |
     | 3     | name3  | uname3    | pwd3     |


Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customers Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "name" to "Alex Mical"
    And I set the "user_name" to "ajmical"
    And I set the "password" to "password"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "name" field should be empty
    And the "user_name" field should be empty
    And the "password" field should be empty
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "Alex Mical" in the "name" field
    And I should see "ajmical" in the "user_name" field
    And I should see "password" in the "password" field


Scenario: Update a Customer
    When I visit the "Home Page"
    And I set the "name" to "Alex Mical"
    And I set the "user_name" to "ajmical"
    And I set the "password" to "password"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "name" field should be empty
    And the "user_name" field should be empty
    And the "password" field should be empty
    When I paste the "id" field
    And I set the "name" to "Marcella Leith"
    And I set the "user_name" to "mcleith"
    And I set the "password" to "password123"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "name" field should be empty
    And the "user_name" field should be empty
    And the "password" field should be empty
    When I paste the "id" field   
    And I press the "Retrieve" button
    Then I should see "Marcella Leith" in the "name" field
    And I should see "mcleith" in the "user_name" field
    And I should see "password123" in the "password" field


Scenario: Delete a Customer
    When I visit the "Home Page"
    And I set the "id" to "1"
    And I press the "Search" button
    Then I should see "name1" in the "name" field
    And I should see "uname1" in the "user_name" field
    When I press the "Delete" button
    Then I should see the message "Customer has been Deleted!"
    When I set the "id" to "1"
    And I press the "Search" button
    Then I should not see "name1" in the results
    

Scenario: Read a Customer
    When I visit the "Home Page"
    And I set the "name" to "Sue Smith"
    And I set the "user_name" to "ssmith"
    And I set the "password" to "password123"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "name" field should be empty
    And the "user_name" field should be empty
    And the "password" field should be empty
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "Sue Smith" in the "name" field
    And I should see "ssmith" in the "user_name" field
    And I should see "password123" in the "password" field



Scenario: Unlock a Customer(Action)
    When I visit the "Home Page"
    And I set the "name" to "Alex Mical"
    And I set the "user_name" to "ajmical"
    And I set the "password" to "password"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "name" field should be empty
    And the "user_name" field should be empty
    And the "password" field should be empty
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "True" in the "locked" dropdown
    When I press the "Unlock" button
    And I press the "Clear" button
    And I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "False" in the "locked" dropdown


Scenario: Lock a Customer (Action)
    When I visit the "Home Page"
    And I set the "name" to "Alex Mical"
    And I set the "user_name" to "ajmical"
    And I set the "password" to "password"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "name" field should be empty
    And the "user_name" field should be empty
    And the "password" field should be empty
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "True" in the "locked" dropdown
    When I press the "Unlock" button
    And I press the "Clear" button
    And I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "False" in the "locked" dropdown
    When I press the "Lock" button
    And I press the "Clear" button
    And I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "True" in the "locked" dropdown


Scenario: List all customers
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "1" in the results
    And I should see "2" in the results
    And I should see "3" in the results
    And I should see "name1" in the results
    And I should see "name2" in the results
    And I should see "name3" in the results
    And I should see "uname1" in the results
    And I should see "uname2" in the results
    And I should see "uname3" in the results


Scenario: List all customers with the name "name1" (Query)
    When I visit the "Home Page"
    And I set the "name" to "name1"
    And I press the "Search" button
    Then I should see "1" in the results
    And I should see "name1" in the results
    And I should see "uname1" in the results
    And I should not see "2" in the results
    And I should not see "name2" in the results
    And I should not see "uname2" in the results
    And I should not see "3" in the results
    And I should not see "name3" in the results
    And I should not see "uname3" in the results