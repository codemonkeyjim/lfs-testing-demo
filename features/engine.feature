Feature: basic arithmetic
    As a regular user
    I want to input numbers and operations
    So I can see the operations' results

    Scenario: Input numbers
        Given the engine is ready
        When I input 123
        Then the display is 123
