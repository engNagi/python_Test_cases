# -- FILE: features/Wordpress.feature,

Feature: WordpressTest

  @WrongPassword
  Scenario: WrongPassword
    Given we have navigated to the given URL
    When we click on "Anmelden"
    And enter the wrong admin login data
    Then the login Password isnt succesfull
  
  @WrongUser
  Scenario: WrongUser
    Given we have navigated to the given URL
    When we click on "Anmelden"
    And enter the wrong user login data
    Then the login User isnt succesfull
  
  @AdminLogin
  Scenario: AdminLogin
    Given we have navigated to the given URL
    When we click on "Anmelden"
    And enter the admin login data
    Then we reach the admin dashboard

  @CreateUser
  Scenario: CreateUser
    Given we are logged in as admin
    And navigate to the user list
    When we create the new users 
    | Benutzername | Email                  | Vorname | Nachname  | Passwort     | Rolle         |
    | stweiss_sub  | stweiss_sub@nomail.org | Stephan | Weiss_sub | !NCS2019_sub | Abonnent      |
    | stweiss_con  | stweiss_con@nomail.org | Stephan | Weiss_con | !NCS2019_con | Mitarbeiter   |
    | stweiss_aut  | stweiss_aut@nomail.org | Stephan | Weiss_aut | !NCS2019_aut | Autor         |
    | stweiss_edi  | stweiss_edi@nomail.org | Stephan | Weiss_edi | !NCS2019_edi | Redakteur     |
    | stweiss_adm  | stweiss_adm@nomail.org | Stephan | Weiss_adm | !NCS2019_adm | Administrator |
    Then they are added to the list
    | Benutzername |
    | stweiss_sub  |
    | stweiss_con  |
    | stweiss_aut  |
    | stweiss_edi  |
    | stweiss_adm  |
    And then the Admin logout
  
  @EditUser
  Scenario Outline: EditUser
    Given we have navigated as ADMIN to the Userlist
    When we click on the "<Benutzername>"
    Then we can change the role to "<Rolle>"
    When we click on the "<Benutzername>"
    Then we can change the "<Farbschema>"
    And then the Admin logout

    # mögliche Werte für Farbschema: Standart, Hell, Blau, Kaffee, Ektoplasma, Mitternacht, Meer, Sonnenaufgang
    # mögliche Werte für Rolle: Abonnent, Mitarbeiter, Autor, Redakteur, Administrator
    Examples: Change_Users
    | Benutzername | Rolle         | Farbschema  |
    | stweiss_sub  | Administrator | Ektoplasma  |
    | stweiss_sub  | Abonnent      | Mitternacht |

  @UserLogin
  Scenario Outline: UserLogin
    Given we have navigated to the given URL
    When we click on "Anmelden"
    And enter the users "<Benutzername>" and "<Passwort>"
    Then the "<Benutzername>" should be logged in
    And the "<Benutzername>" is able to logout

    Examples: Users_Login
    | Benutzername | Passwort     |
    | stweiss_sub  | !NCS2019_sub |
    | stweiss_con  | !NCS2019_con |
    | stweiss_aut  | !NCS2019_aut |
    | stweiss_edi  | !NCS2019_edi |
    | stweiss_adm  | !NCS2019_adm |

  @DeleteUser
  Scenario Outline: DeleteUser
    Given we have navigated as ADMIN to the Userlist
    When we search for the "<Benutzername>"
    And find the "<Benutzername>" in the list
    Then we can click on delete button
    And the "<Benutzername>" is deleted
    And then the Admin logout
    
    Examples: Delete_Users
    | Benutzername |
    | stweiss_sub  |
    | stweiss_con  |
    | stweiss_aut  |
    | stweiss_edi  |
    | stweiss_adm  |  