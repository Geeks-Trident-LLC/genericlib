"""
Unit test package for file utilities.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/file
    or
    $ python -m pytest tests/unit/file
"""

from genericlib.decorators import normalize_return_output_text


@normalize_return_output_text
def get_sample_yaml_data():
    data = """
        location:
          main: San Jose, CA
          branch: Milpitas, CA
        employees:
          employee1:
            name: Jack Brown
            office_location: "{self.location.main}"
          employee2:
            name: Linda Wilson
            office_location: "{self.location.branch}"  
    """
    return data
