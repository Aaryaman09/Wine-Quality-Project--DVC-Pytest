import pytest

class NotInRange(Exception):
    def __init__(self, message = 'Value not in Range'):
        self.message = message
        super().__init__(self.message)

def test_generic():
    a = 5          # Changed from 5 to 13.
    with pytest.raises(NotInRange):
        # with pytest.raises(NotInRange): is a context manager provided by pytest. 
        # It is used to check that the code block inside it raises a specific exception (NotInRange in this case).
        if a not in range(10,20):
            raise NotInRange
            # Inside the context manager, there is an if statement that checks if a is not in the range from 10 to 19. 
            # If it's not in this range, it raises the NotInRange exception.

# CASE 1 : a = 5
# Since the code inside the with pytest.raises(NotInRange): block raises the NotInRange exception as expected, 
# the test will pass, and you will see the result as "PASSED."
# In summary, this code demonstrates a simple pytest test case for checking whether a value (in this case, a) is in a specified range and raises a custom exception (NotInRange) if it's not. 
# The test is designed to pass successfully, as the value 5 is indeed not in the range [10, 19].


# CASE 2 : a = 13
# Now, with a set to 13, let's see how the code behaves:

# 1. pytest enters the test_generic function and executes its code.
# 2. a is assigned the value 13.
# 3. The if statement checks if a is not in the range from 10 to 19. However, in this case, 13 is indeed within the specified range.
# 4. Therefore, the if condition evaluates to False, and the code inside the if block (raise NotInRange) is not executed.

# Since the raise NotInRange statement is not executed, the NotInRange exception is not raised during the test. As a result, 
# the test will fail because it expected the NotInRange exception to be raised, but it wasn't. 
# This failure indicates that the value 13 is within the specified range, and the test case does not behave as expected in this scenario.