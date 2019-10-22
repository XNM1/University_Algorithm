from faker import Faker
from faker.providers import lorem
fake = Faker('en_US')
fake.add_provider(lorem)

with open('in.txt', 'w', encoding='utf-8') as output_file:
    for i in range(100):
	    output_file.write(str(fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None)) + ('\n' if i != 99 else ''))