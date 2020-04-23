Feature: The pet store service back-end
    As a Customer Servicing Team
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
        | id           | name   | user_name | password |
        | id1          | name1  | uname1    | pwd1     |
        | id2          | name2  | uname2    | pwd2     |
        | id3          | name3  | uname3    | pwd3     |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "id" to "alexmical"
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
    Then I should see "alexmical" in the "id" field
    And I should see "Alex Mical" in the "name" field
    And I should see "ajmical" in the "user_name" field
    And I should see "password" in the "password" field


Scenario: Update a Customer
    When I visit the "Home Page"
    And I set the "id" to "id1"
    And I press the "Search" button
    Then I should see "name1" in the "name" field
    And I should see "uname1" in the "user_name" field
    And I should see "pwd1" in the "password" field
    When I change "name" to "changed_name"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    And I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "changed_name" in the "name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "changed_name" in the results
    Then I should not see "name1" in the results


Scenario: Delete a Customer
    When I visit the "Home Page"
    And I set the "id" to "id1"
    And I press the "Search" button
    Then I should see "name1" in the "name" field
    And I should see "uname1" in the "user_name" field
    And I press the "Delete" button
    Then I should see the message "Success."
    And I set the "id" to "id1"
    And I press the "Search" button
    Then I should not see "name1" in the results
    

Scenario: Read a Customer
    When I visit the "Home Page"
    And I set the "id" to "id1"
    And I press the "Retrieve" button
    Then I should see "name1" in the "name" field
    And I should see "uname1" in the "user_name" field
    And I should see "pwd1" in the "password" field
    And I should not see "name2" in the "name" field
    And I should not see "uname2" in the "user_name" field
    And I should not see "pwd2" in the "password" field
    And I should not see "name3" in the "name" field
    And I should not see "uname3" in the "user_name" field
    And I should not see "pwd3" in the "password" field

Scenario: Unlock a Customer(Action)
    When I visit the "Home Page"
    And I set the "id" to "id1"
    And I press the "Retrieve" button
    Then I should see "true" in the locked dropdown
    Then I press the "Unl   ock" button
    And I press the "Clear" button
    And I set the "id" to "id1"
    And I press the "Retrieve" button
    And I should see "false" in the results



Scenario: Lock a Customer (Action)
    When I visit the "Home Page"
    And I set the "id" to "id1"
    And I press the "Retrieve" button
    Then I should see "false" in the locked dropdown
    Then I press the "Lock" button
    And I press the "Clear" button
    And I set the "id" to "id1"
    And I press the "Retrieve" button
    And I should see "true" in the results



Scenario: List all customers
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "id1" in the results
    And I should see "id2" in the results
    And I should not see "id3" in the results
    And I should not see "name1" in the results
    And I should not see "name2" in the results
    And I should not see "name3" in the results
    And I should not see "uname1" in the results
    And I should not see "uname2" in the results
    And I should not see "uname3" in the results


Scenario: List all customers with the name "name1" (Query)
    When I visit the "Home Page"
    And I set the "name" to "name1"
    And I press the "Search" button
    Then I should see "id1" in the results
    And I should see "name1" in the results
    And I should see "uname1" in the results
    And I should see "pwd1" in the results
    And I should not see "id2" in the results
    And I should not see "name2" in the results
    And I should not see "uname2" in the results
    And I should not see "pwd2" in the results
    And I should not see "id3" in the results
    And I should not see "name3" in the results
    And I should not see "uname3" in the results
    And I should not see "pwd3  " in the results