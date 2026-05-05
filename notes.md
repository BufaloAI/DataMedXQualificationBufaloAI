
<first_trial_of_converting_string_sets_to_floats>

Some vital commands:

iloc[row, column] returns data as string.

string.count('[') counts set count in that string

To convert a string consisting of sets, do this:

list version = string.split(',')

Internet search yields those to do so:

df['age'] = df['age'].astype(int)
df = df.astype({'col1': 'float', 'col2': 'int'})

text.replace(a, b) şeklinde de bir çözüm üretilebilir.

</first_trial_of_converting_string_sets_to_floats>
