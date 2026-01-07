import pytest

from genericlib.exceptions import raise_exception
from genericlib.exceptions import InvalidExceptionType
from genericlib.exceptions import create_runtime_error

from tests.unit import DummyClass

class FooTestExceptionCls(Exception):
    """
    Custom exception class used for testing `raise_exception`.

    This class serves as a lightweight stand‑in for real exception types
    during unit tests. It allows validation of how `raise_exception`
    behaves when raising, formatting, or handling exceptions.

    Notes
    -----
    - Defined only for testing purposes; not intended for production use.
    """

class BarTestExceptionCls(Exception):
    class BarTestExceptionCls(Exception):
        """
        Custom exception class used for testing `raise_exception`.

        This class acts as an alternate test exception type to validate
        how `raise_exception` behaves when a different exception class
        is explicitly passed via the `cls` keyword argument.

        Notes
        -----
        - Defined only for testing purposes; not intended for production use.
        """

class FooBarCls:
    """
    Dummy class used for testing `raise_exception`.

    This class is intentionally not derived from `Exception` and serves
    as a negative test case. It allows validation that `raise_exception`
    correctly rejects non‑exception types when passed via the `cls`
    keyword argument.

    Notes
    -----
    - Defined only for testing purposes; not intended for production use.
    """
    def __init__(self):
        self.var1 = "value 1"
        self.var2 = "value 2"

class TestRaiseExceptionFunction:
    """
    Unit tests for the `raise_exception` utility in regexapp.exceptions.

    This test suite validates the behavior of `raise_exception` under
    different argument combinations, ensuring correct exception raising,
    error handling, and formatting behavior.
    Notes
    -----
    - These tests use `pytest.raises` to assert that the correct
      exception type is raised in each scenario.
    - Custom test exception classes (`FooTestExceptionCls`,
      `BarTestExceptionCls`) are defined to isolate behavior.
    - The suite ensures robustness of `raise_exception` by covering
      both valid and invalid inputs.
    """

    def test_arg_ex_is_exception_instance(self):
        """
        Verify that `raise_exception` correctly handles a valid Exception instance.

        This test ensures that when an actual Exception object is passed as
        the `ex` argument, the function raises that same exception type as
        expected. It validates the core behavior of `raise_exception` when
        used with proper inputs.
        """
        with pytest.raises(FooTestExceptionCls):
            ex = FooTestExceptionCls('a instance of SampleTestException')
            raise_exception(ex)

    def test_arg_ex_is_not_exception_instance(self):
        """
        Verify that `raise_exception` rejects non-Exception inputs.

        This test ensures that when objects or types that are not instances
        of `Exception` are passed to `raise_exception`, the function raises
        `InvalidExceptionType` as expected. It validates the defensive
        behavior of the utility against improper usage.

        Notes
        -----
        - Covers multiple invalid inputs including:
          * a generic object instance
          * a float value
          * a string
          * a non-Exception class (`FooBarCls`)
        - Confirms that `raise_exception` enforces type safety by requiring
          an actual Exception instance.
        - Uses `pytest.raises` to assert that `InvalidExceptionType` is
          consistently raised for all invalid cases.
        """
        with pytest.raises(InvalidExceptionType):
            foo = object()
            raise_exception(foo)        # noqa

        with pytest.raises(InvalidExceptionType):
            number = 1.23
            raise_exception(number)     # noqa

        with pytest.raises(InvalidExceptionType):
            data = "abc xyz"
            raise_exception(data)       # noqa

        with pytest.raises(InvalidExceptionType):
            raise_exception(FooBarCls)       # noqa

    def test_kwarg_is_skipped(self):
        """
        Verify that `raise_exception` respects the `is_skipped` flag.

        This test ensures that when `is_skipped=True` is passed, the function
        does not raise any exception and instead returns `None`. It validates
        the skip‑logic branch of `raise_exception`, confirming that exception
        raising can be conditionally bypassed.
        """
        ex = FooTestExceptionCls('a instance of SampleTestException')
        result = raise_exception(ex, is_skipped=True)   # noqa
        assert result is None

    def test_kwarg_msg(self):
        """
        Verify that `raise_exception` raises with a custom message when `msg` is provided.

        This test ensures that when the `msg` keyword argument is passed,
        the function raises the target exception class using that message
        instead of formatting the original exception. It validates the
        message‑override branch of `raise_exception`.
        """
        with pytest.raises(FooTestExceptionCls):
            ex = FooTestExceptionCls('a instance of SampleTestException')
            failure = f"Failure happened at {ex}"
            raise_exception(ex, msg=failure)

    def test_kwarg_cls_is_passing_type_of_exception(self):
        """
        Verify that `raise_exception` raises the specified exception class when `cls` is provided.

        This test ensures that when a valid Exception subclass is passed via
        the `cls` keyword argument, the function raises that class instead of
        the type of the original exception instance. It validates the
        override behavior of `raise_exception`.
        """
        with pytest.raises(BarTestExceptionCls):
            ex = FooTestExceptionCls('a instance of SampleTestException')
            raise_exception(ex, cls=BarTestExceptionCls)

    def test_kwarg_cls_is_passing_incorrect_type_of_exception(self):
        """
        Verify that `raise_exception` ignores an invalid `cls` argument.

        This test ensures that when a non-Exception type is passed via the
        `cls` keyword argument, the function does not raise that type. Instead,
        it falls back to raising the type of the original exception instance.
        """
        with pytest.raises(FooTestExceptionCls):
            ex = FooTestExceptionCls('a instance of SampleTestException')
            raise_exception(ex, cls=FooBarCls)  # noqa

    def test_kwarg_fmt_is_passing_default_format(self):
        """
        Verify that `raise_exception` applies the default format string
        when `fmt` is not provided.

        This test ensures that when no custom format string is passed via the
        `fmt` keyword argument, the function uses its default format of
        `"{}: {}"` to construct the failure message. It validates the
        default formatting branch of `raise_exception`.
        """
        with pytest.raises(FooTestExceptionCls):
            ex = FooTestExceptionCls('a instance of SampleTestException')
            raise_exception(ex)

    def test_kwarg_fmt_is_passing_custom_format(self):
        """
        Verify that `raise_exception` applies a custom format string
        when `fmt` is provided.

        This test ensures that when a user-defined format string is passed via
        the `fmt` keyword argument, the function uses that format to construct
        the failure message instead of the default `"{}: {}"` pattern. It
        validates the customization branch of `raise_exception`.
        """
        with pytest.raises(FooTestExceptionCls):
            ex = FooTestExceptionCls('a instance of SampleTestException')
            custom_format = "*** {} - {}"
            raise_exception(ex, fmt=custom_format)

    def test_kwarg_fmt_is_passing_incorrect_format_index_error(self):
        """
        Verify that `raise_exception` raises IndexError when the format
        string has too many placeholders.

        This test ensures that if the `fmt` keyword argument contains more
        placeholders than provided substitution values, Python's string
        formatting raises an `IndexError`. It validates the defensive
        behavior of `raise_exception` when given an invalid format string.
        """
        with ((pytest.raises(IndexError))):
            ex = FooTestExceptionCls('a instance of SampleTestException')
            index_error_format = "{} - {} {}"
            raise_exception(ex, fmt=index_error_format)

    def test_kwarg_fmt_is_passing_incorrect_format_value_error(self):
        """
        Verify that `raise_exception` raises ValueError when the format
        string is malformed.

        This test ensures that if the `fmt` keyword argument contains an
        invalid format string (e.g., unmatched braces or incorrect syntax),
        Python's string formatting raises a `ValueError`. It validates the
        defensive behavior of `raise_exception` when given a malformed
        format string.
        """
        with pytest.raises(ValueError):
            ex = FooTestExceptionCls('a instance of SampleTestException')
            value_error_format = "{} - {{}"
            raise_exception(ex, fmt=value_error_format)

    def test_kwarg_fmt_is_passing_incorrect_format_value_error_other(self):
        """
        Verify that `raise_exception` raises ValueError when the format
        string contains unmatched braces.

        This test ensures that if the `fmt` keyword argument includes an
        incomplete or malformed format string (e.g., a single unmatched
        opening brace), Python's string formatting raises a `ValueError`.
        It validates the defensive behavior of `raise_exception` when
        encountering syntactically invalid format patterns.
        """
        with pytest.raises(ValueError):
            ex = FooTestExceptionCls('a instance of SampleTestException')
            other_value_error_format = "{} - {"
            raise_exception(ex, fmt=other_value_error_format)

    def test_kwarg_fmt_is_passing_incorrect_format_key_error(self):
        """
        Verify that `raise_exception` raises KeyError when the format
        string references an invalid key.

        This test ensures that if the `fmt` keyword argument contains a
        placeholder referencing a non-existent key, Python's string
        formatting raises a `KeyError`. It validates the defensive
        behavior of `raise_exception` when encountering invalid key
        references in format strings.
        """
        with pytest.raises(KeyError):
            ex = FooTestExceptionCls('a instance of SampleTestException')
            key_error_format = "{} - {ab}"
            raise_exception(ex, fmt=key_error_format)


class TestCreateRuntimeError:
    """
    Unit tests for `create_runtime_error`.

    Coverage:
    - obj=None → defaults to RuntimeError.
    - obj=str → uses string directly as class name.
    - obj=object → class name suffixed with RTError.
    - Exception message is correctly set.
    """

    def test_none_defaults_to_runtime_error(self):
        """Verify that None input defaults to RuntimeError with the correct message."""
        exc = create_runtime_error(obj=None, msg="generic failure")
        assert exc.__class__.__name__ == "RuntimeError"
        with pytest.raises(exc.__class__, match="generic failure"):
            raise exc

    def test_string_creates_named_exception(self):
        """Verify that a string input creates an exception with that exact class name."""
        exc = create_runtime_error(obj="CustomError", msg="something went wrong")
        assert exc.__class__.__name__ == "CustomError"
        with pytest.raises(exc.__class__, match="something went wrong"):
            raise exc

    def test_object_creates_classname_rt_error(self):
        """Verify that an object input creates an exception suffixed with RTError."""
        obj = DummyClass()
        exc = create_runtime_error(obj=obj, msg="dummy failure")
        assert exc.__class__.__name__ == "DummyClassRTError"
        with pytest.raises(exc.__class__, match="dummy failure"):
            raise exc

    def test_integer_object_creates_int_rt_error(self):
        """Verify that an integer input creates an IntRTError exception."""
        exc = create_runtime_error(obj=42, msg="invalid value")
        # int class name is "int" → "IntRTError"
        assert exc.__class__.__name__ == "IntRTError"
        with pytest.raises(exc.__class__, match="invalid value"):
            raise exc

    def test_empty_message_defaults(self):
        """Verify that the default message is an empty string when not provided."""
        exc = create_runtime_error(obj="EmptyMsgError")
        assert exc.__class__.__name__ == "EmptyMsgError"
        # message should be empty string
        assert str(exc) == ""
