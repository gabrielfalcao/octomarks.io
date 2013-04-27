Feature: The Explore Screen
  As a developer
  I want to explore the most interesting bookmarks

  Background:
    Given the users:
      | username       | theme   | tags                     |
      | anaconda       | github  | python, testing, mock    |
      | redberry       | emacs   | ruby, testing            |
      | cafezinho      | tango   | javascript, coffeescript |
      | roundhouse     | github  | C, C++, GNU, kernel      |
      | batbelt        | github  | C#, F#, sharp-stuff      |
      | xrayvision     | zenburn | IO, rust, alien-stuff    |
      | dbadude        | emacs   | redis, mongodb           |
      | frontendguy    | github  | jQuery, css3             |
      | nineth-element | zenburn | qt, gtk, atk             |
      | decadius       | autumn  | go, tornado, twisted     |


  Scenario: Top Bookmarks
    Given the projects:
      | name       | owner         | tags       | favorited |
      | anaconda   | johnsnake     | python     | 2 times   |
      | redberry   | rubywoods     | ruby       | 2 times   |
      | cafezinho  | jakartarobins | javascript | 3 times   |
      | roundhouse | chucknorris   | C          | 8 times   |
      | batbelt    | batman        | C#         | 5 times   |
      | xrayvision | superman      | io         | 4 times   |
    When an anonymous user goes to "/ranking"
    Then he should see there are "5" top bookmarks in this order:
      | name       | favorited |
      | roundhouse |         8 |
      | batbelt    |         5 |
      | xrayvision |         4 |
      | cafezinho  |         3 |
      | anaconda   |         2 |
