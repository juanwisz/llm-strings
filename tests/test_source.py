import pytest
from source import LMString, LMRecordStrings

@pytest.fixture
def sample_lmstring():
    return LMString("Hello, {name}!")

@pytest.fixture
def sample_lmrecord():
    lmstring = LMString("Hello, {name}!")
    return LMRecordStrings() @ lmstring

def test_lmstring_initialization(sample_lmstring):
    assert isinstance(sample_lmstring, LMString)
    assert "name" in sample_lmstring._all_args
  
def test_lmstring_formatting(sample_lmstring):
    formatted = sample_lmstring.format(name="World")
    assert str(formatted) == "Hello, World!"

    with pytest.raises(ValueError):
        LMString("Positional {0} not allowed.")

def test_lmstring_matmul(sample_lmstring):
    record = sample_lmstring @ " Follow-up message."
    assert isinstance(record, LMRecordStrings)
    assert len(record.records) == 2
  
def test_lmrecord_initialization(sample_lmrecord):
    assert len(sample_lmrecord.records) == 1
  
def test_lmrecord_adding_records(sample_lmrecord):
    sample_lmrecord @ "User message" @ "Assistant message"
    assert len(sample_lmrecord.records) == 3
    assert sample_lmrecord.records[1]['role'] == 'user'
    assert sample_lmrecord.records[2]['role'] == 'assistant'
  
def test_lmrecord_str(sample_lmrecord):
    representation = str(sample_lmrecord)
    assert "Hello, {name}!" in representation
    assert "┌" in representation and "└" in representation  # Check borders are present.
  
def test_successful_lmrecord_formatting(sample_lmrecord):
    # Test successful formatting
    formatted_lmrecord = sample_lmrecord.format(0, name="World")
    assert "Hello, World!" in formatted_lmrecord.records[0]['content'], "The formatting did not apply as expected."

def test_lmrecord_formatting_with_out_of_bounds_index(sample_lmrecord):
    # Test formatting with an out-of-bounds index, expecting an IndexError
    with pytest.raises(IndexError) as exc_info:
        sample_lmrecord.format(100, name="Out of bounds")
        
@pytest.fixture
def simple_lmstring():
    return LMString("Simple message")

@pytest.fixture
def complex_lmstring():
    return LMString("Hello, {user_name}. Welcome to {system_name}!")
@pytest.fixture

def empty_lmrecord():
    return LMRecordStrings()

@pytest.fixture
def initialized_lmrecord(complex_lmstring):
    record = LMRecordStrings() @ complex_lmstring
    return record
  
def test_complex_lmstring_initialization(complex_lmstring):
    assert isinstance(complex_lmstring, LMString)
    assert complex_lmstring._all_args == {"user_name", "system_name"}
  
def test_lmstring_partial_formatting(complex_lmstring):
    partially_formatted = complex_lmstring.format(user_name="Alice")
    assert "{system_name}" in partially_formatted
    assert "Alice" in partially_formatted
  
def test_lmrecord_initial_role_assignment(empty_lmrecord):
    empty_lmrecord @ "System initialized"
    assert empty_lmrecord.records[0]['role'] == 'system'
  
def test_sequence_after_system(initialized_lmrecord):
    initialized_lmrecord @ "User starts" @ "Assistant responds"
    roles = [record['role'] for record in initialized_lmrecord.records]
    expected_roles = ['system', 'user', 'assistant']
    assert roles == expected_roles
  
def test_adding_multiple_records_maintains_sequence(empty_lmrecord):
    messages = ["Message 1", "Message 2", "Message 3", "Message 4"]
    for msg in messages:
        empty_lmrecord @ msg
    roles = [record['role'] for record in empty_lmrecord.records]
    expected_roles = ['system', 'user', 'assistant', 'user']
    assert roles == expected_roles
  
def test_record_formatting_updates_content(initialized_lmrecord):
    formatted_record = initialized_lmrecord.format(0, user_name="Bob", system_name="LMSystem")
    assert "Hello, Bob. Welcome to LMSystem!" in formatted_record.records[0]['content']
  
def test_lmstring_positional_arguments_error():
    with pytest.raises(ValueError) as excinfo:
        LMString("Positional {0} not allowed.")
    assert "Positional formatting is not allowed" in str(excinfo.value)
  
def test_lmrecord_matmul_unsupported_type(empty_lmrecord):
    with pytest.raises(TypeError) as excinfo:
        empty_lmrecord @ 123  # Attempt to concatenate an integer
    assert "Unsupported type for composition" in str(excinfo.value)
  
def test_lmrecord_formatting_invalid_index(initialized_lmrecord):
    with pytest.raises(IndexError) as excinfo:
        initialized_lmrecord.format(99, name="Alice")  # Non-existent record index
    assert "Invalid position for formatting" in str(excinfo.value)
  
def test_lmrecord_partial_then_full_formatting(initialized_lmrecord):
    partially_formatted = initialized_lmrecord.format(0, user_name="Alice")
    fully_formatted = partially_formatted.format(0, system_name="LMSystem")
    final_content = fully_formatted.records[0]['content']
    assert final_content == "Hello, Alice. Welcome to LMSystem!"
  
def test_concatenating_lmrecordstrings(empty_lmrecord):
    first_record = empty_lmrecord @ "First system message" @ "First user response"
    second_record = LMRecordStrings() @ "Second system message" @ "Second user response"
    concatenated_records = first_record @ second_record
    assert len(concatenated_records.records) == 4
    assert concatenated_records.records[2]['content'] == "Second system message"
import time

def test_lmrecord_adding_performance(empty_lmrecord):
    start_time = time.time()
    for _ in range(1000):  # Add a thousand records
        empty_lmrecord @ "Performance test message"
    end_time = time.time()
    duration = end_time - start_time
    assert duration < 1  # The operation should take less than 1 second
  
def test_lmrecord_composition_with_lmstring_and_raw_string(initialized_lmrecord):
    initialized_lmrecord @ "Additional raw string message" @ LMString("Formatted {term} message", _is_formatting=True)
    assert len(initialized_lmrecord.records) == 3
    assert initialized_lmrecord.records[1]['content'] == "Additional raw string message"
    assert "{term}" in initialized_lmrecord.records[2]['content']
  
def test_argument_retention_after_partial_formatting(complex_lmstring):
    partially_formatted = complex_lmstring.format(user_name="Charlie")
    assert "user_name" not in partially_formatted._missing_args
    assert "system_name" in partially_formatted._missing_args
  
def test_repeated_formatting_resilience(initialized_lmrecord):
    first_format = initialized_lmrecord.format(0, user_name="Dave", system_name="TestSystem")
    second_format = first_format.format(0, user_name="Dave", system_name="TestSystem")
    assert first_format.records[0]['content'] == second_format.records[0]['content']
  
def test_formatting_with_extra_unused_arguments(complex_lmstring):
    formatted = complex_lmstring.format(user_name="Eve", system_name="AnotherSystem", unused_arg="Should be ignored")
    assert "Eve" in formatted and "AnotherSystem" in formatted and "Should be ignored" not in formatted
  
def test_invariant_properties_preserved_during_non_modifying_operations(initialized_lmrecord):
    original_missing_args = {tuple(record['content']._missing_args) for record in initialized_lmrecord.records if isinstance(record['content'], LMString)}
    initialized_lmrecord @ "Non-modifying string"
    updated_missing_args = {record['content']._missing_args for record in initialized_lmrecord.records if isinstance(record['content'], LMString)}
    assert original_missing_args == updated_missing_args
  
def test_error_propagation_from_lmstring_to_lmrecord(complex_lmstring, empty_lmrecord):
    empty_lmrecord @ complex_lmstring
    with pytest.raises(ValueError) as excinfo:
        empty_lmrecord.format(0, invalid_arg="This should fail")
    assert "not allowed" in str(excinfo.value)  # Assuming the error message includes "not allowed"
  
def test_edge_cases_for_string_composition(empty_lmrecord):
    edge_case_string = "{}"  # Could be confused with an unfilled placeholder
    empty_lmrecord @ edge_case_string
    assert empty_lmrecord.records[0]['content'] == edge_case_string

    empty_string = ""
    empty_lmrecord @ empty_string
    assert empty_lmrecord.records[1]['content'] == empty_string
  
def test_formatting_completeness(complex_lmstring):
    fully_formatted = complex_lmstring.format(user_name="Frank", system_name="SecureSystem")
    assert not fully_formatted._missing_args
