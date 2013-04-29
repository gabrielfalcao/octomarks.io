Feature: The Explore Screen
  As a developer
  I want to explore the most interesting bookmarks

  Background:
    Given the users:
      | username       | theme   | tags                     |
      | johnsnake      | github  | python, testing, mock    |
      | rubywoods      | emacs   | ruby, testing            |
      | jakartarobins  | tango   | javascript, coffeescript |
      | chucknorris    | github  | C, C++, GNU, kernel      |
      | batman         | github  | C#, F#, sharp-stuff      |
      | superman       | zenburn | IO, rust, alien-stuff    |
      | dbadude        | emacs   | redis, mongodb           |
      | frontendguy    | github  | jQuery, css3             |
      | nineth-element | zenburn | qt, gtk, atk             |
      | decadius       | autumn  | go, tornado, twisted     |

    And the projects:
      | name       | owner         |
      | anaconda   | johnsnake     |
      | redberry   | rubywoods     |
      | cafezinho  | jakartarobins |
      | roundhouse | chucknorris   |
      | batbelt    | batman        |
      | xrayvision | superman      |

  Scenario: Top Bookmarks
    Given that the project "anaconda" got `5` favorites
    And that the project "redberry" got `1` favorites
    And that the project "cafezinho" got `3` favorites
    And that the project "roundhouse" got `2` favorites
    And that the project "xrayvision" got `4` favorites
    And that the project "batbelt" got `4` favorites
    When an anonymous user goes to "/explore"
    Then he should see there are "5" top bookmarks in this order:
      | name       | owner         | favorites |
      | anaconda   | johnsnake     |         5 |
      | xrayvision | superman      |         4 |
      | batbelt    | batman        |         4 |
      | cafezinho  | jakartarobins |         3 |
      | roundhouse | chucknorris   |         2 |


  Scenario: Top Users
    And the projects:
      | name       | owner         |
      | anaconda   | johnsnake     |
      | redberry   | rubywoods     |
      | cafezinho  | jakartarobins |
      | roundhouse | chucknorris   |
      | batbelt    | batman        |
      | xrayvision | superman      |
    And that the user "decadius" favorited `5` projects
    And that the user "jakartarobins" favorited `2` projects
    And that the user "johnsnake" favorited `4` projects
    And that the user "dbadude" favorited `1` project
    And that the user "frontendguy" favorited `3` projects
    And that the user "rubywoods" favorited `2` projects
    When an anonymous user goes to "/explore"
    Then he should see there are "5" top users in this order:
      | name          | favorited |
      | decadius      |         5 |
      | johnsnake     |         4 |
      | frontendguy   |         3 |
      | jakartarobins |         2 |
      | rubywoods     |         2 |

  @later
  Scenario: Top Tags
    Given the user "decadius" has the bookmarks:
      | name       | owner         | tags                       |
      | anaconda   | johnsnake     | python, testing, mock      |
      | redberry   | rubywoods     | ruby, testing              |
      | cafezinho  | jakartarobins | javascript, testing, ui    |
      | roundhouse | chucknorris   | C, hacking                 |
      | batbelt    | batman        | C#, enterprise, testing    |
      | xrayvision | superman      | IO, enterprise             |
      | foo1       | baz1          | redis, mongodb, enterprise |
      | foo2       | baz2          | jQuery, css3 , ui          |
      | foo3       | baz3          | qt, gtk, atk, ui           |
      | foo4       | baz4          | go, tornado, twisted, testing |
    When an anonymous user goes to "/explore"
    Then he should see there are "5" top tags in this order:
      | name       | favorited |
      | testing    |         5 |
      | enterprise |         3 |
      | ui         |         3 |
      | hacking    |         2 |
      | python     |         1 |
