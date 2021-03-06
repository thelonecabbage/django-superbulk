Feature: Single transactions for bulk requests.
    Scenario: Testing atomicity when both inserts are valid
        Given the post data is "[{"method":"POST","uri":"/api/v1/invoice/","body":"{\"customer_id\":\"test-test-test\",\"invoice_no\":\"0001\"}"},{"method":"POST","uri":"/api/v1/invoice/","body":"{\"customer_id\":\"test-test-test\",\"invoice_no\":\"0002\"}"}]"
        And I post the data to "/api/superbulk_transactional/"
        Then both inserts are inside the database

    Scenario: Testing atomicity when one insert fails
        Given the post data is "[{"method":"POST","uri":"/api/v1/invoice/","body":"{\"customer_id\":\"test1-test1-test1\",\"invoice_no\":\"0003\"}"},{"method":"POST","uri":"/api/v1/invoice/","body":"{\"customer_id\":\"test1-test1-test1\",\"invoice_no_field\":\"0004\"}"}]"
        And I post the data to "/api/superbulk_transactional/"
        Then transaction failed atomically

    Scenario: Testing failfast option in transaction
        Given the post data is "{"failfast": "True", "content": [{"method":"POST","uri":"/api/v1/invoice/","body":"{\"customer_id\":\"test2-test2-test2\",\"invoice_no\":\"0005\"}"},{"method":"POST","uri":"/api/v1/invoice/","body":"{\"customer_id\":\"test2-test2-test2\",\"invoice_no_field\":\"0006\"}"},{"method":"POST","uri":"/api/v1/invoice/","body":"{\"customer_id\":\"test5-test5-test5\",\"invoice_no\":\"0009\"}"}]}"
        And I post the data to "/api/superbulk_transactional/"
        Then transaction stops after first failure