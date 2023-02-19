# How to execute the tests
* Run the tests with major detail level in the messages: for achive it

`python -m unittest -v tests/test_album.py`

* Execute aññ the tests from the folder tests

`python -m unittest discover -s tests -v`

* For get help

`python -m unittest -h`

* It is a method that it is call before call the methods with the tests, it is use for prepared the objets that it will use in the test suite. By default, its implementation does not do some actions.

`setUp()`

* It is a method that it is call together after the call the last instruction in the tests and next save the results, and it is in general using for the methods exception catch with the tests to define what happend when it is executed.

# Methods for tests

`tearDown()`

`assertEqual(a,b)`

`assertNotEqual(a,b)`

`assertTrue(x)`

`assertFalse(x)`

`assertIs(a,b)`

`assertIsNot(a,b)`

`assertIsNone(x)`

`assertIsNotNone(x)`

`assertIn(a,b)`

`assertNotIn(a,b)`

`assertIsInstance(a,b)`

`assertNotIsInstance(a,b)`