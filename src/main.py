import click
import pandas as pd
from faker import Faker

import json

def map_inputs_to_faker(meta_file: str) -> dict:
    """
    Maps a json metadata file to Faker data types
    :param meta_file: string representing the path of the metadata file
    :return: a dictionary where keys are the column names and values are the corresponding Faker data types
    """
    fake = Faker()
    data_types = {
        # providers
        "bothify": fake.bothify,
        "language_code": fake.language_code,
        "locale": fake.locale,
        "random_digit": fake.random_digit,
        "language_code": fake.language_code,
        # address
        "address": fake.address,
        "city": fake.city,
        "country": fake.country,
        "country_code": fake.country_code,
        "postcode": fake.postcode,
        # company
        "company": fake.company,
        # credit_card
        "credit_card_expire": fake.credit_card_expire,
        "credit_card_number": fake.credit_card_number,
        "credit_card_provider": fake.credit_card_provider,
        "credit_card_security_code": fake.credit_card_security_code,
        # currency
        "pricetag": fake.pricetag,
        # date_time
        "am_pm": fake.am_pm,
        "century": fake.century,
        "date_time": fake.date_time,
        "date_of_birth": fake.date_of_birth,
        "date_this_century": fake.date_this_century,
        "date_this_month": fake.date_this_month,
        "date": fake.date,
        # person
        "name": fake.name,
        "first_name": fake.first_name,
        "last_name": fake.last_name,
        "email": fake.email,
        # phone_number
        "phone_number": fake.phone_number,
        # job
        "job": fake.job,
        "paragraph": fake.paragraph,
        "sentence": fake.sentence,
        "word": fake.word, 
        # python
        "pyint": fake.pyint
    }
    with open(meta_file) as json_file:
        meta_data = json.load(json_file)

    def generate_faker_func(col, faker_type, faker_params=None):
        if faker_params:
            return lambda: getattr(fake, faker_type)(**faker_params)
        return data_types[faker_type]

    mapped_inputs = {}
    for col in meta_data:
        type_ = meta_data[col].get("type", None)
        params = meta_data[col].get("params", None)
        mapped_inputs[col] = generate_faker_func(col, type_, params)
    
    return mapped_inputs



@click.command()
@click.option('--num_records', '-n', type=int, default=1000, help='The number of records to generate.', prompt=True)
@click.option('--file_name', '-f', type=str, help='Name of the output file.', prompt=True)
@click.option('--file_format', '-ft', type=str, default='parquet', help='File format to save the data in - parquet or csv', prompt=True)
@click.option('--meta_file', '-m', type=click.Path(), default='metadata.json', help='metadata file with columns', prompt=True)
def generate_data(num_records, file_name, file_format, meta_file):
    """ Generate fake data and save to a file """
    # Create an empty dataframe with columns specified in the metadata file
    data_types = map_inputs_to_faker(meta_file)
    output_data = pd.DataFrame(columns=data_types.keys())

    # Generate the specified number of fake customer names and addresses
    for _ in range(num_records):
        output_data = output_data.append({col: data_types[col]() for col in output_data.columns}, ignore_index=True)

    # Save the customer data to a file
    if file_format == "parquet":
        output_data.to_parquet(file_name, index=False)
    elif file_format == "csv":
        output_data.to_csv(file_name, index=False)
    else:
        click.echo("Invalid file format, please choose either 'parquet' or 'csv'.")

if __name__ == '__main__':
    generate_data()
