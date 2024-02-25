# llm-strings
A lightweight library for message handling with instruction fine-tuned language models.

This module provides two classes: `LMString` and `LMRecordStrings`. 

- `LMString` is a subclass of Python's built-in string class that overides the `format` method to provide more informative feedback about missing formatting arguments.

- `LMRecordStrings` stores multiple string records and formats them according to the input text conversations. You can still format messages after wrapped in a collection, and you have a guarantee over the roles sequence: system (optional), user, assistant, user, assistant,...

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

### More examples

#### Optional[System],(User,Asisstant)*n invariant:

```python
# Initializing a conversation with an opening message
conversation = LMRecordStrings() @ "Hello, {name}. How can I assist you today?"

# Adding more records to the conversation
conversation @ "I need assistance with {topic}." @ "Certainly, what specific aspect of {topic} are you interested in?"

# Formatting the first record with the user's name
conversation = conversation.format(0, name="Alice")

# Formatting the second record (user's message) with the topic
conversation = conversation.format(1, topic="Python programming")

# Formatting the third record (assistant's message) with the same topic
conversation = conversation.format(2, topic="Python programming")

# Adding a user reply to the assistant's question
conversation @ "{aspect} of Python programming sounds challenging."

# Formatting the fourth record (user's message) with the specific aspect
conversation = conversation.format(3, aspect="asynchronous code execution")

# Let's add the assistant's final message
conversation @ "I can help you understand {concept} with some examples and explanations."

# Formatting the fifth record (assistant's message) with the specific concept
conversation = conversation.format(4, concept="asynchronous code execution")

# Print the entire conversation
print(conversation)
```

This will produce an output representing a back-and-forth conversation between the user and the assistant, with roles correctly alternating and messages formatted based on the arguments provided:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 0. System: ***  Hello, Alice. How can I assist you today? ***                                             │
│------------------------------------------------------------------------------------------------------------│
│ 1. User: I need assistance with Python programming.                                                       │
│------------------------------------------------------------------------------------------------------------│
│ 2. Assistant: Certainly, what specific aspect of Python programming are you interested in?                │
│------------------------------------------------------------------------------------------------------------│
│ 3. User: Asynchronous code execution of Python programming sounds challenging.                            │
│------------------------------------------------------------------------------------------------------------│
│ 4. Assistant: I can help you understand asynchronous code execution with some examples and explanations.  │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### V-Formatting
```python
# Initializing a conversation with an opening message
conversation = LMRecordStrings() @ "Hello, {name}. How can I assist you today?"

# Adding more records to the conversation
conversation @ "I need assistance with {topic}." @ "Certainly, what specific aspect of {topic} are you interested in?"

# Adding a user reply to the assistant's question
conversation @ "{aspect} of {topic} sounds challenging."

# Let's add the assistant's final message
conversation @ "I can help you understand {concept} with some examples and explanations."

# Now, we use vformat to apply the formatting arguments to all records
formatted_conversation = conversation.vformat(
    name="Alice",
    topic="Python programming",
    aspect="asynchronous code execution",
    concept="asynchronous code execution"
)

# Print the fully formatted conversation
print(formatted_conversation)
```

This will produce an output similar to the one before, but this time we are formatting all the records in one go at the end, using the `vformat` method:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 0. System: ***  Hello, Alice. How can I assist you today? ***                                             │
│------------------------------------------------------------------------------------------------------------│
│ 1. User: I need assistance with Python programming.                                                       │
│------------------------------------------------------------------------------------------------------------│
│ 2. Assistant: Certainly, what specific aspect of Python programming are you interested in?                │
│------------------------------------------------------------------------------------------------------------│
│ 3. User: Asynchronous code execution of Python programming sounds challenging.                            │
│------------------------------------------------------------------------------------------------------------│
│ 4. Assistant: I can help you understand asynchronous code execution with some examples and explanations.  │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

The `vformat` method is particularly useful when you have multiple records that require similar arguments, and you want to apply the formatting in a single step. It streamlines the process and makes the code cleaner and more concise, especially when dealing with lengthy conversations.
