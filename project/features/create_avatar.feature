Feature: Avatar management

Scenario: Create automatically an avatar if None is provided
    When a new player is created without an avatar
    Then the player's avatar is generated
