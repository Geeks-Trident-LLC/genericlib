"""
Unit tests for the `genericlib.utils.MiscFunction` class.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/utils/test_misc_function_class.py
    or
    $ python -m pytest tests/unit/utils/test_misc_function_class.py
"""

import pytest
from genericlib.utils import MiscFunction

from tests.unit.utils import DummyClass
from tests.unit.utils import (
    sample_func_displaying_stdout,
    sample_func_displaying_stderr,
    sample_func_displaying_stdout_and_stderr,
    sample_func_args
)


class TestDoSilentInvoke:
    """
    Unit tests for `MiscFunction.do_silent_invoke`.

    Coverage:
    - Captures stdout only.
    - Captures stderr only.
    - Captures both stdout and stderr.
    - Returns callable result correctly.
    - Writes combined output to file when filename is provided.
    - Handles positional and keyword arguments.
    """

    def test_capture_stdout_only(self):
        result = MiscFunction.do_silent_invoke(sample_func_displaying_stdout)
        assert result.result == "return_value"
        assert "hello stdout" in result.output
        assert result.error == ""
        assert result.output_and_error == result.output

    def test_capture_stderr_only(self):
        result = MiscFunction.do_silent_invoke(sample_func_displaying_stderr)
        assert result.result == 9999
        assert result.output == ""
        assert "hello stderr" in result.error
        assert "hello stderr" in result.output_and_error

    def test_capture_both_streams(self):
        result = MiscFunction.do_silent_invoke(sample_func_displaying_stdout_and_stderr)
        assert result.result == "mixed"
        assert "stdout here" in result.output
        assert "stderr here" in result.error
        assert "stdout here" in result.output_and_error
        assert "stderr here" in result.output_and_error

    def test_with_arguments(self):
        result = MiscFunction.do_silent_invoke(sample_func_args, 3, y=4)
        assert result.result == 7
        assert "sum=7" in result.output

    def test_write_to_file(self, tmp_path):
        file_path = tmp_path / "output.txt"
        result = MiscFunction.do_silent_invoke(
            sample_func_displaying_stdout_and_stderr,
            filename=str(file_path)
        )

        # File should contain combined output
        content = file_path.read_text()
        assert "stdout here" in content
        assert "stderr here" in content
        assert content == result.output_and_error



class TestCreateRuntimeError:
    """
    Unit tests for `MiscFunction.create_runtime_error`.

    Coverage:
    - obj=None → defaults to RuntimeError.
    - obj=str → uses string directly as class name.
    - obj=object → class name suffixed with RTError.
    - Exception message is correctly set.
    """

    def test_none_defaults_to_runtime_error(self):
        exc = MiscFunction.create_runtime_error(obj=None, msg="generic failure")
        assert exc.__class__.__name__ == "RuntimeError"
        with pytest.raises(exc.__class__, match="generic failure"):
            raise exc

    def test_string_creates_named_exception(self):
        exc = MiscFunction.create_runtime_error(obj="CustomError", msg="something went wrong")
        assert exc.__class__.__name__ == "CustomError"
        with pytest.raises(exc.__class__, match="something went wrong"):
            raise exc

    def test_object_creates_classname_rt_error(self):
        obj = DummyClass()
        exc = MiscFunction.create_runtime_error(obj=obj, msg="dummy failure")
        assert exc.__class__.__name__ == "DummyClassRTError"
        with pytest.raises(exc.__class__, match="dummy failure"):
            raise exc

    def test_integer_object_creates_int_rt_error(self):
        exc = MiscFunction.create_runtime_error(obj=42, msg="invalid value")
        # int class name is "int" → "IntRTError"
        assert exc.__class__.__name__ == "IntRTError"
        with pytest.raises(exc.__class__, match="invalid value"):
            raise exc

    def test_empty_message_defaults(self):
        exc = MiscFunction.create_runtime_error(obj="EmptyMsgError")
        assert exc.__class__.__name__ == "EmptyMsgError"
        # message should be empty string
        assert str(exc) == ""


class TestRaiseRuntimeError:
    """
    Unit tests for `MiscFunction.raise_runtime_error`.

    Coverage:
    - obj=None → raises RuntimeError with correct message.
    - obj=str → raises custom exception with given name.
    - obj=object → raises exception suffixed with RTError.
    - Message content is correctly propagated.
    """

    def test_none_raises_runtime_error(self):
        with pytest.raises(Exception) as exc_info:
            MiscFunction.raise_runtime_error(obj=None, msg="generic failure")
        exc = exc_info.value
        assert exc.__class__.__name__ == "RuntimeError"
        assert str(exc) == "generic failure"

    def test_string_raises_custom_exception(self):
        with pytest.raises(Exception) as exc_info:
            MiscFunction.raise_runtime_error(obj="CustomError", msg="something went wrong")
        exc = exc_info.value
        assert exc.__class__.__name__ == "CustomError"
        assert str(exc) == "something went wrong"

    def test_object_raises_classname_rt_error(self):
        obj = DummyClass()
        with pytest.raises(Exception) as exc_info:
            MiscFunction.raise_runtime_error(obj=obj, msg="dummy failure")
        exc = exc_info.value
        # DummyClass → DummyClassRTError
        assert exc.__class__.__name__ == "DummyClassRTError"
        assert str(exc) == "dummy failure"

    def test_builtin_object_int_creates_int_rt_error(self):
        with pytest.raises(Exception) as exc_info:
            MiscFunction.raise_runtime_error(obj=42, msg="invalid value")
        exc = exc_info.value
        # int → IntRTError
        assert exc.__class__.__name__ == "IntRTError"
        assert str(exc) == "invalid value"

    def test_empty_message_defaults(self):
        with pytest.raises(Exception) as exc_info:
            MiscFunction.raise_runtime_error("EmptyMsgError")
        exc = exc_info.value
        assert exc.__class__.__name__ == "EmptyMsgError"
        # message should be empty string
        assert str(exc) == ""