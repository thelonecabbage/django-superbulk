Feature: Sequential logged transactions
    Scenario: Testing logging of transactions
        Given the post data is "[{"method":"POST","uri":"/api/v1/invoice/","body":"{\"customer_id\":\"asdf-asdf-asdf-sadf\",\"invoice_no\":\"0001\"}"},{"method":"POST","uri":"/api/v1/invoice/","body":"{\"customer_id\":\"asdf-asdf-asdf-sadf\",\"invoice_nosub\":\"0001\"}"}]"
        And I post the data to "/api/superbulk/"
        Then all individual responses have correct format
