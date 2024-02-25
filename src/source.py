import string
import copy

class LMString(str):
    def __new__(cls, content, _is_formatting=False):
        instance = super(LMString, cls).__new__(cls, content)
        instance._all_args = set()

        for literal_text, field_name, format_spec, conversion in string.Formatter().parse(content):
            if field_name is not None:
                if field_name.isdigit() or field_name == '':
                    raise ValueError("Positional formatting is not allowed. Please use named arguments.")
                instance._all_args.add(field_name)

        if not _is_formatting:
            print("Template String initialized successfully. Required args:", instance._all_args)
        instance._missing_args = instance._all_args
        return instance

    def format(self, **kwargs):
        if not kwargs:
            print(f"No kwargs has been passed, current args now: {self._all_args}")
            return self
        self._missing_args = self._all_args - kwargs.keys()
        safe_kwargs = {key: kwargs[key] for key in kwargs if key in self._all_args}
        safe_kwargs.update({arg: '{' + arg + '}' for arg in self._missing_args})
        if self._missing_args:
            print("Template String has been partially formatted successfully. Required args now:", sorted(list(self._missing_args)))
        return LMString(super().format(**safe_kwargs), _is_formatting=True)

    def __matmul__(self, other):
        if isinstance(other, str):
            return LMRecordStrings(self) @ other
        raise TypeError("Unsupported type for composition. Must be str.")
        
class LMRecordStrings:
    def __init__(self, initial_message=None):
        self.records = []
        if initial_message is not None:
            self @ initial_message

    def __matmul__(self, other):
        if isinstance(other, LMRecordStrings):
            if self.records and other.records:
                # Merge system messages and append other records, adjusting roles as needed.
                if self.records[-1]['role'] == other.records[0]['role']:
                    # If the last record of 'self' and the first record of 'other' have the same role, merge their content
                    self.records[-1]['content'] += " " + other.records[0]['content']
                    # Then append the rest of the records from 'other'
                    self.records += other.records[1:]
                else:
                    # If the roles are different, simply append all records from 'other'
                    self.records += other.records
            elif other.records:
                # If 'self' has no records, just take all records from 'other'
                self.records = other.records
        elif isinstance(other, str):
            # Determine the next role based on the last record in 'self'
            next_role = 'system' if not self.records else ('assistant' if self.records[-1]['role'] == 'user' else 'user')
            # Append a new record with the determined role and the string content
            self.records.append({'role': next_role, 'content': other})
        else:
            raise TypeError("Unsupported type for composition. Must be LMRecordStrings or str.")
        return self

    def __str__(self):
        border_width = 100
        top_border = f"┌{'─' * border_width}┐\n"
        bottom_border = f"└{'─' * border_width}┘"
        message_separator = f"│{'-' * (border_width)}│\n"

        conversation = top_border
        for index, record in enumerate(self.records):
            prefix = f"{index}. "
            
            if record['role'] == 'system':
                speaker = "System"
                formatted_message = f"{prefix}{speaker}: ***  {record['content']} ***"
            elif record['role'] == 'user':
                speaker = "User"
                formatted_message = f"{prefix}{speaker}: {record['content']}"
            else:
                speaker = "Assistant"
                formatted_message = f"{prefix}{speaker}: {record['content']}"

            line_length = border_width - 4
            lines = [formatted_message[i:i+line_length] for i in range(0, len(formatted_message), line_length)]
            for line_index, line in enumerate(lines):
                if line_index > 0:
                    line = f"{' ' * len(prefix)}{line}"
                conversation += f"│ {line.ljust(line_length)} │\n"

            if index < len(self.records) - 1:
                conversation += message_separator

        conversation += bottom_border
        return conversation

    def format(self, position: int, *args, **kwargs):
        if position < 0 or position >= len(self.records):
            raise IndexError("Invalid position for formatting.")
        current_missing_args = self.records[position]['content']._missing_args
        new_instance = copy.deepcopy(self)
        formatted_content = new_instance.records[position]['content'].format(*args, **kwargs)
        new_instance.records[position]['content'] = formatted_content
        print(f"{position}. Record formatted succesfully. Formatted args: {current_missing_args-formatted_content._missing_args}. Required args now: {formatted_content._missing_args}")
        return new_instance

    def vformat(self, *args, **kwargs):
        positions = list(range(1, len(self.records)))
        for position in positions:
            if position < 0 or position >= len(self.records):
                raise IndexError("Invalid position for formatting.")
        new_instance = copy.deepcopy(self)
        for position in positions:
            if not isinstance(self.records[position]['content'], LMString):
                continue
            current_missing_args = self.records[position]['content']._missing_args
            formatted_content = new_instance.records[position]['content'].format(*args, **kwargs)
            new_instance.records[position]['content'] = formatted_content
            print(f"{position}. Record formatted succesfully. Formatted args: {current_missing_args-formatted_content._missing_args}. Required args now: {formatted_content._missing_args}")
        print(new_instance)
        print("Records formatted succesfully!")
        return new_instance
