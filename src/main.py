import click
import pandas as pd
from faker import Faker
from dotenv import load_dotenv
import json
import os

load_dotenv()


def map_inputs_to_faker(meta_file: str) -> dict:
    """
    Maps a json metadata file to Faker data types
    :param meta_file: string representing the path of the metadata file
    :return: a dictionary where keys are the column names and values are the corresponding Faker data types
    """
    fake = Faker(locale=os.getenv("FAKER_LOCALE", "en_US"))

    with open(meta_file) as json_file:
        meta_data = json.load(json_file)

    def generate_faker_func(col, faker_type, faker_params=None):
        if faker_params:
            # is there are parameters to pass to the faker method, this adds them
            return lambda: getattr(fake, faker_type)(**faker_params)
        return getattr(fake, faker_type)

    mapped_inputs = {}
    for col in meta_data:
        type_ = meta_data[col].get("type", None)
        params = meta_data[col].get("params", None)
        mapped_inputs[col] = generate_faker_func(col, type_, params)

    return mapped_inputs


@click.command()
@click.option("--num_files", "-f", type=int, default=10, help="The number of files to generate.", prompt=True)
@click.option("--num_records", "-n", type=int, default=100, help="The number of records to generate.", prompt=True)
@click.option("--file_name", "-fn", type=str, help="Name of the output file.", prompt=True)
@click.option(
    "--file_format",
    "-ft",
    type=str,
    default="parquet",
    help="File format to save the data in - parquet or csv or json",
    prompt=True,
)
@click.option(
    "--meta_file", "-m", type=click.Path(), default="metadata.json", help="metadata file with columns", prompt=True
)
def generate_data(num_files, num_records, file_name, file_format, meta_file):
    """ Generate fake data and save to a file """

    # Create an empty dataframe with columns specified in the metadata file
    data_types = map_inputs_to_faker(meta_file)

    for file in range(num_files):

        output_data = pd.DataFrame(columns=data_types.keys())

        # Generate the specified number of fake customer names and addresses
        for _ in range(num_records):
            output_data = output_data.append({col: data_types[col]() for col in output_data.columns}, ignore_index=True)

        # Save the customer data to a file
        output_file = f"{file_name}-{file + 1}"
        if file_format == "parquet":
            output_data.to_parquet(f"{output_file}.parquet", index=False)
        elif file_format == "csv":
            output_data.to_csv(f"{output_file}.csv", index=False)
        elif file_format == "json":
            output_data.to_json(f"{output_file}.json", index=False)
        else:
            click.echo("Invalid file format, please choose either 'parquet' or 'csv'.")


if __name__ == "__main__":
    generate_data()
