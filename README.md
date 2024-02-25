# llm-strings
A lightweight library for message handling with instruction fine-tuned language models.

This module provides two classes: `LMString` and `LMRecordStrings`. 

- `LMString` is a subclass of Python's built-in string class that overides the `format` method to provide more informative feedback about missing formatting arguments.

- `LMRecordStrings` stores multiple string records and formats them according to the input text conversations.

# Usage

## LMString Class 

### Initialize the `LMString`

```python
template = LMString("Hello, {name}. Today is {day}.")
# Output: Template String initialized successfully. Required args: {'day', 'name'}
```

In this example, we create an `LMString` that expects two arguments: `name` and `day`.

### Format the `LMString`

```python
template.format(name="Alice")
# Output: Template String has been partially formatted successfully. Required args now: ['day']
```

If only a subset of the required arguments are provided, `format` will return an `LMString` that only expects the remaining ones.

```python
template.format(name="Alice", day="Monday")
#Output: "Hello, Alice. Today is Monday."
```

When all required arguments are provided, `format` will return an ordinary string.

### Compose `LMString` with another string

```python
template @ "How are you?"
# Output: "Hello, {name}. Today is {day}. How are you?"
```

The `@` operator can be used to concatenate an `LMString` with another string. The resulting `LMString` will expect all arguments that the original `LMString` expected.

## LMRecordStrings Class 

### Initialize the `LMRecordStrings`

```python
record = LMRecordStrings("Hello, {name}.")
```

In this example, we create an `LMRecordStrings` that expects one argument: `name`.

### Compose `LMRecordStrings` with another string or `LMRecordStrings`

```python
record @ "Today is {day}."
record @ LMRecordStrings("How are you?")
```

The `@` operator can be used to concatenate an `LMRecordStrings` with another string or `LMRecordStrings`. The resulting `LMRecordStrings` will expect all arguments that the original `LMRecordStrings` expected.

### Format the `LMRecordStrings`

```python
record.format(0, name="Alice")
# Output: 0. Record formatted succesfully. Formatted args: {'name'}. Required args now: set()
```

The `format` method formats a specific record in the `LMRecordStrings`. The first argument is the index of the record to format, and the remaining arguments are the formatting arguments.

```python
record.vformat(name="Alice", day="Monday")
# Output: Records formatted succesfully!
```

The `vformat` method formats all records in the `LMRecordStrings` that expect the provided arguments.

### Print the `LMRecordStrings`

```python
print(record)
```

The `__str__` method returns a string representation of the `LMRecordStrings` that can be printed to the console. The string representation includes a border and separates each record with a line.

```python
record = LMRecordStrings("Hello, {name}.") @ "Today is {day}." @ LMRecordStrings("How are you?")
record = record.format(0, name="Alice").vformat(day="Monday")
print(record)
```

This would output:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 0. System: ***  Hello, Alice. ***                                                                         │
│------------------------------------------------------------------------------------------------------------│
│ 1. User: Today is Monday.                                                                                 │
│------------------------------------------------------------------------------------------------------------│
│ 2. Assistant: How are you?                                                                                │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
