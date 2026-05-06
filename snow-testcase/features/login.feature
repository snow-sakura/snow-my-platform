Feature: User Login
  In order to access my personal account
  As a registered user
  I want to log in to the system with my credentials

  Background:
    Given the application is running
    And I open the login page

  # 正向用例：用户名+密码正确，登录成功
  Scenario: Successful login with valid credentials
    Given I have a valid user account
    When I enter username "standard_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should be redirected to the home page
    And I should see a welcome message for user "standard_user"
    And I should see the logout button

  # 异常用例：用户名或密码错误
  Scenario Outline: Login fails with invalid credentials
    When I enter username "<username>"
    And I enter password "<password>"
    And I click the login button
    Then I should remain on the login page
    And I should see an error message "<error_message>"

    Examples:
      | username       | password      | error_message                                         |
      | wrong_user     | secret_sauce  | Username and password do not match any user          |
      | standard_user  | wrong_pass    | Username and password do not match any user          |
      | unknown_user   | wrong_pass    | Username and password do not match any user          |

  # 边界用例：必填字段为空
  Scenario Outline: Login fails when required fields are empty
    When I enter username "<username>"
    And I enter password "<password>"
    And I click the login button
    Then I should remain on the login page
    And I should see a validation message "<validation_message>"

    Examples:
      | username       | password      | validation_message                  |
      |                | secret_sauce  | Username is required                |
      | standard_user  |               | Password is required                |
      |                |               | Username and password are required  |

  # 业务用例：被锁定用户登录失败
  Scenario: Locked out user cannot log in
    Given there is a locked user account "locked_out_user"
    When I enter username "locked_out_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should remain on the login page
    And I should see an error message "Sorry, this user has been locked out."

  # 安全用例：密码错误不暴露具体信息（可选）
  Scenario: Do not expose which field is incorrect
    When I enter username "standard_user"
    And I enter password "wrong_pass"
    And I click the login button
    Then I should see a generic error message "Username and password do not match any user"
    And the error message should not indicate whether username or password is incorrect

  # 会话用例：登录后刷新页面仍然保持登录状态（可选）
  Scenario: Session is preserved after page refresh
    Given I am logged in as "standard_user"
    When I refresh the page
    Then I should still be on the home page
    And I should still see the logout button

  # 登出用例：从登录状态退出成功（可选，但与登录强相关）
  Scenario: Successful logout
    Given I am logged in as "standard_user"
    When I click the logout button
    Then I should be redirected to the login page
    And I should no longer see the logout button

