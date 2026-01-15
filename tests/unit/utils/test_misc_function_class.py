"""
Unit tests for the `genericlib.utils.MiscFunction` class.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/utils/test_misc_function_class.py
    or
    $ python -m pytest tests/unit/utils/test_misc_function_class.py
"""

from genericlib.utils import do_silent_invoke

from tests.unit.utils import (
    sample_func_displaying_stdout,
    sample_func_displaying_stderr,
    sample_func_displaying_stdout_and_stderr,
    sample_func_args
)


class TestDoSilentInvoke:
    """
    Unit tests for `do_silent_invoke`.

    Coverage:
    - Captures stdout only.
    - Captures stderr only.
    - Captures both stdout and stderr.
    - Returns callable result correctly.
    - Writes combined output to file when filename is provided.
    - Handles positional and keyword arguments.
    """

    def test_capture_stdout_only(self):
        """
        Verify that stdout is captured correctly when the callable
        prints only to stdout.
        """
        result = do_silent_invoke(sample_func_displaying_stdout)
        assert result.result == "return_value"
        assert "hello stdout" in result.output
        assert result.error == ""
        assert result.output_and_error == result.output

    def test_capture_stderr_only(self):
        """
        Verify that stderr is captured correctly when the callable
        prints only to stderr.
        """
        result = do_silent_invoke(sample_func_displaying_stderr)
        assert result.result == 9999
        assert result.output == ""
        assert "hello stderr" in result.error
        assert "hello stderr" in result.output_and_error

    def test_capture_both_streams(self):
        """
        Verify that both stdout and stderr are captured correctly
        when the callable prints to both streams.
        """
        result = do_silent_invoke(sample_func_displaying_stdout_and_stderr)
        assert result.result == "mixed"
        assert "stdout here" in result.output
        assert "stderr here" in result.error
        assert "stdout here" in result.output_and_error
        assert "stderr here" in result.output_and_error

    def test_with_arguments(self):
        """
        Verify that positional and keyword arguments are passed correctly
        to the callable and that stdout is captured.
        """
        result = do_silent_invoke(sample_func_args, 3, y=4)
        assert result.result == 7
        assert "sum=7" in result.output

    def test_write_to_file(self, tmp_path):
        """
        Verify that combined stdout and stderr output is written to a file
        when a filename is provided.
        """
        file_path = tmp_path / "output.txt"
        result = do_silent_invoke(
            sample_func_displaying_stdout_and_stderr,
            filename=str(file_path)
        )

        # File should contain combined output
        content = file_path.read_text()
        assert "stdout here" in content
        assert "stderr here" in content
        assert content == result.output_and_error
