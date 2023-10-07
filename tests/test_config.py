import pytest
from prediction_service.prediction import form_response, api_response, NotInRange, NotInCols


input_data = {
    "incorrect_range": 
        {
            "fixed_acidity": 7897897, 
            "volatile_acidity": 555, 
            "citric_acid": 99, 
            "residual_sugar": 99, 
            "chlorides": 12, 
            "free_sulfur_dioxide": 789, 
            "total_sulfur_dioxide": 75, 
            "density": 2, 
            "pH": 33, 
            "sulphates": 9, 
            "alcohol": 9
        },

    "correct_range":
        {
            "fixed_acidity": 5, 
            "volatile_acidity": 1, 
            "citric_acid": 0.5, 
            "residual_sugar": 10, 
            "chlorides": 0.5, 
            "free_sulfur_dioxide": 3, 
            "total_sulfur_dioxide": 75, 
            "density": 1, 
            "pH": 3, 
            "sulphates": 1, 
            "alcohol": 9
        },

    "incorrect_col":
        {
            "fixed acidity": 5, 
            "volatile acidity": 1, 
            "citric acid": 0.5, 
            "residual sugar": 10, 
            "chlorides": 0.5, 
            "free sulfur dioxide": 3, 
            "total_sulfur dioxide": 75, 
            "density": 1, 
            "pH": 3, 
            "sulphates": 1, 
            "alcohol": 9
        }
}

TARGET_range = {
    "min": 3.0,
    "max": 8.0
}

def test_form_response_correct_range(data = input_data["correct_range"]):
    res = form_response(data)
    assert TARGET_range['min'] <= res <= TARGET_range["max"]

def test_api_response_correct_range(data = input_data["correct_range"]):
    res = api_response(data)
    assert TARGET_range['min'] <= res['response'] <= TARGET_range["max"]

def test_form_response_incorrect_range(data = input_data['incorrect_range']):
    with pytest.raises(NotInRange):
        res = form_response(data)

def test_api_response_incorrect_range(data = input_data["incorrect_range"]):
    res = api_response(data)
    assert NotInRange().message == res['response']

def test_form_response_incorrect_cols(data = input_data['incorrect_col']):
    with pytest.raises(NotInCols):
        res = form_response(data)

def test_api_response_incorrect_col(data = input_data["incorrect_col"]):
    res = api_response(data)
    assert NotInCols().message == res['response']

"""
Explaination :

1. A test case function simply wants all statements within it to run as they are suppose to (i.e all statemets True)
    example:

    def test_addition():
        result = add(2, 3)
        assert result == 5

    ->  This test checks whether the add function correctly adds 2 and 3, expecting the result to be 5.
    ->  If the add function correctly returns 5, the test will pass, and pytest will report it as a successful test.
    ->  If the add function does not return 5, suppose 6 (e.g., it returns a different value or raises an exception), 
        the test will fail, and pytest will report it as a failed test.

So for above test cases : 

TEST 1 :: 

def test_form_response_correct_range(data = input_data["correct_range"]):   ----------- 1
    res = form_response(data)                                               ----------- 2
    assert TARGET_range['min']<= res <= TARGET_range["max"]                 ----------- 3

1.  test_form_response_correct_range method wants all statements should perform as they suppose to (ASSERT TRUE).
    Ie if good input is inserted then no error should come i.e no error raise should happen.
2.  Since we have input of CORRECT RANGE then it is 'EXPECTED' our response will be within range.
    Treat your internal function (form_response in this case) as black box. GARBAGE IN, GARBAGE OUT
3.  assert TARGET_range['min']<= res <= TARGET_range["max"] :: if res is in within range(thinking form_response as a black box),
    then the test has PASSED otherwwise FAIL.

    

TEST 2 ::

def test_api_response_correct_range(data = input_data["correct_range"]):
    res = api_response(data)
    assert TARGET_range['min'] <= res['response'] <= TARGET_range["max"]

    ## Since api_response is structed differently from form_response, it raises EXCEPTION with not_in_range/not_in_cols message in key 'response':str(e) ie 
        def api_response(dict_request):
        try:
            if validate_input(dict_request):
                data = np.array([list(dict_request.values())])
                response = predict(data)
    -->         response = {'response':response}
        except Exception as e:                                                  
            reponse = {'the expected_range': get_schema(), 'response':str(e)}
            return reponse

Same Idea. Just fetch the response from key 'response'.



TEST 3 ::

def test_form_response_incorrect_range(data = input_data['incorrect_range']):   -------- 1
    with pytest.raises(NotInRange):                                             -------- 2            
        res = form_response(data)                                               -------- 3

1.  test_form_response_incorrect_range method wants all statements should perform as they suppose to (ASSERT TRUE). This idea is still true
    but its little tricky here, here since we are feeding incorrect input(GARBAGE IN), the function should raise a perticular ERROR which is Not_in_range.
    So we want this test to raise a ERROR within it.
2.  with pytest.raises(NotInRange) context manager returns ASSERT TRUE (ie Test Success) if pytest.raises ENCOUNTERS that particular error specified in parameters that is NOT_IN_RRANGE in this case.
3.  res = form_response(data) :: Since GARBAGE was feeded to the form_response function, it is SUPPOSE to RAISE not_in_range exception (think form_response as black box)
    As the code is written by us and we know for sure that not_in_range exception was raised. Line 2 CAPTURED not_in_range exception, and line 2 RETURNED
    ASSERT TRUE to Line 1. Hence Test Successfully, ie GARBAGE IN, should raise an ERROR and it did.             

    

TEST 4 ::

def test_api_response_incorrect_range(data = input_data["incorrect_range"]):    ---------- 1
    res = api_response(data)                                                    ---------- 2
    assert NotInRange().message == res['response']                              ---------- 3

1.  test_api_response_incorrect_range method wants all statements should perform as they suppose to (ASSERT TRUE). This idea is still true
    but its little tricky here, here since we are feeding incorrect input(GARBAGE IN), the function should raise a perticular ERROR which is Not_in_range.
    So we want this test to raise a ERROR within it.

    ## Since api_response is structed differently from form_response, it raises EXCEPTION with not_in_range/not_in_cols message in key 'response':str(e) ie 
        def api_response(dict_request):
        try:
            if validate_input(dict_request):
                data = np.array([list(dict_request.values())])
                response = predict(data)
                response = {'response':response}
    --> except Exception as e:                                                  
    -->     reponse = {'the expected_range': get_schema(), 'response':str(e)}
    -->     return reponse

    Hence to check if correct error was raised or not, we just need to check error message.

2.  res = api_response(data)  :: Since incorrect input is given (GARBAGE IN)(incrrect range), it should raise not_in_range ERROR, 
    just check response's error message and match it with not_in_range error message.
3.  assert NotInRange().message == res['response'] :: As a black box, it should raise not_in_range range exception as incorrect range input was given.
    Since we wrote that function, we know it raised a not_in_range exception and we matched it with not_in_range error message with was a TRUE.
    Hence ASSERT TRUE i.e. Test Successful.


    
TEST 5 :: Same Idea as TEST 3 but for not_in_cols exception.



TEST 6 :: Same Idea as TEST 4 but for not_in_cols exception.
"""

