import pytest   # noqa

from genericlib import DictObject
from genericlib import DotObject
from genericlib import substitute_variable

from yaml import safe_load


class TestDictObject:
    """Test class for DictObject."""
    def test_initialization1(self):
        """Test dict object initialization 1"""
        node = DictObject({'first': 'cherry', 'last time': 'berry'})
        assert node

    def test_initialization2(self):
        """Test dict object initialization 2"""
        node = DictObject({'last time': 'berry'}, first='cherry')
        assert node

    def test_initialization3(self):
        """Test dict object initialization 3"""
        node = DictObject([('first', 'cherry'), ('last time', 'berry')])
        assert node

    def test_initialization4(self):
        """Test dict object initialization 4"""
        node = DictObject([('True', True), ('False', False)])
        assert node

    def test_getter(self):
        """Test getter"""
        data = {'first': 'cherry', 'last item': 'berry', 'True': True, 'False': False}
        node = DictObject(data)

        assert node.first == 'cherry'
        assert node.True_ is True
        assert node.False_ is False

    def test_setter(self):
        """Test setter"""
        node = DictObject()
        node.first = 'cherry'
        assert node['first'] == 'cherry'

        node['last_item'] = 'berry'
        assert node.last_item == 'berry'


class TestDotObject:
    """Test class for testing DotObject."""

    def test_getter(self):
        """Test getter"""
        node = DotObject(
            person1=dict(name='Jack Brown', location='USA', gender='Male'),
            person2=dict(name='Mary Smith', location='USA', gender='Female'),
            person3=dict(name='Linda Johnson', location='USA', gender='Female')
        )

        assert node.person1.name == 'Jack Brown'
        assert node.person1.gender == 'Male'
        assert node.person2.name == 'Mary Smith'
        assert node.person2.gender == 'Female'
        assert node.person3.name == 'Linda Johnson'
        assert node.person3.gender == 'Female'

    def test_setter(self):
        """Test setter"""
        node = DotObject()
        node.person1 = dict(name='Jack Brown', location='USA', gender='Male')
        node.person2 = dict(name='Mary Smith', location='USA', gender='Female')
        node.person3 = dict(name='Linda Johnson', location='USA', gender='Female')

        assert node.person1.name == 'Jack Brown'
        assert node.person1.gender == 'Male'
        assert node.person2.name == 'Mary Smith'
        assert node.person2.gender == 'Female'
        assert node.person3.name == 'Linda Johnson'
        assert node.person3.gender == 'Female'


class TestSubstitutingVariable:

    def test_case1(self):
        data = """
            full_name: "{self.first_name} {self.last_name}"
            first_name: Jack
            last_name: Brown
            other_full_name: "{self.last_name}, {self.first_name}"
        """

        node = safe_load(data)
        result = DotObject(substitute_variable(node))

        assert result.full_name == 'Jack Brown'
        assert result.other_full_name == 'Brown, Jack'

    def test_case2(self):
        data = """
            employee2:
                name: Linda Wilson
                location: "{self.common_info.other_location}"

            common_info:
                main_location: "San Jose, CA"
                other_location: "Milpitas, CA"
            
            employee1:
                name: Jack Brown
                location: "{self.common_info.main_location}"
        """

        node = safe_load(data)
        result = DotObject(substitute_variable(node))

        assert result.employee1.name == 'Jack Brown'
        assert result.employee1.location == 'San Jose, CA'

        assert result.employee2.name == 'Linda Wilson'
        assert result.employee2.location == 'Milpitas, CA'
