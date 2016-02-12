# -*- coding: utf-8 -*-
@upgrade_to_1.2.7 @debonix

Feature: upgrade to 1.2.7

  Scenario: upgrade application version
    Given I update the module list
    Given I install the required modules with dependencies:
      | name                 |
    Then my modules should have been installed and models reloaded

    Given I set the version of the instance to "1.2.7"
