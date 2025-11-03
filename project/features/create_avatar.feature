Feature: Avatar management

Scenario: Create automatically an avatar if None is provided on build + save
    Given I build a new player
    And It doesn't have an avatar
    When I save the new player
    Then It does have an avatar

Scenario: Create automatically an avatar if None is provided on create
    Given I create a new player
    Then It does have an avatar
