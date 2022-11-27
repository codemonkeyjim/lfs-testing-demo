Feature: basic arithmetic
    As a calculator user
    I want to input numbers and operations
    So I can see the operations' results

    Scenario: Perform calculations
        Given the calculator is ready
        When I click 123
        # And I click +
        # And I click 234
        Then the display is 123
