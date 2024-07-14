Feature: Home Page

Scenario: Check the number of player is valid
    Given I build a new player
    When I visit '/'
    Then I should see 0 players and 0 games
    When I save the new player
    And I visit '/'
    Then I should see 1 players and 0 games
    When I create 5 new players
    And I visit '/'
    Then I should see 6 players and 0 games
