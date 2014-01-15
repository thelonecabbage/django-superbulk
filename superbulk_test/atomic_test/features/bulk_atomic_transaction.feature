Feature: Bulk atomic transaction
    #Scenario: Testing atomicity when both inserts are valid
    #    Given the post data is "[{"method":"POST","uri":"/api/v1/customer/","body":"{\"id\":\"test-test-test\",\"name\":\"Justin\"}"},{"method":"POST","uri":"/api/v1/invoice/","body":"{\"customer_id\":\"test-test-test\",\"invoice_no\":\"0001\"}"}]"
    #    And I post the data to "/api/superbulk_transactional/"
    #    Then both inserts are inside the database

    Scenario: Testing atomicity when one insert fails
        Given the post data is "[{"method":"POST","uri":"/api/v1/customer/","body":"{\"id\":\"test1-test1-test1\",\"name\":\"Justin\"}"},{"method":"POST","uri":"/api/v1/invoice/","body":"{\"customer_id\":\"test1-test1-test1\",\"invoice_no_field\":\"0002\"}"}]"
        And I post the data to "/api/superbulk_transactional/"
        Then transaction failed atomically