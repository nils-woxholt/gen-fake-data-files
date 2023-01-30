# gen-fake-data-files

A command line app to generate fake data files as parquet or csv by providing a metadata file which defines the data.

## Setup

```bash
# Create a Python virtual environment
python -m venv .venv
# Activate
source ./.venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```

## Create a metadata file

In the `/src` folder, create a json file where the keys will be the column names and the values will be the data types and any Faker parameters that you want to use.

```json
{
    "Name": {"type": "name"},
    "Email": {"type": "email"},
    "ContactNumber": {"type": "phone_number"},
    "DOB": {"type": "date_of_birth"},
    "BookingDate": {"type": "date_this_month"},
    "DestinationCity": {"type": "city"},
    "TicketNumber": {"type":"bothify", "params": {"text":"????-########", "letters":"ABCDEFGHIJ"}}
}
```

The values can be any [Faker provider](https://faker.readthedocs.io/en/master/providers.html).

## Run

```bash
# run from the src folder
cd src

# optionally set a local - default is en_US
export FAKER_LOCALE=en_GB

# let the program prompt you for inputs
python main.py
# OR
# pass the inputs at runtime
python main.py -f 10 -n 20 -fn output -ft csv -m metadata.json
# OR
# more verbose
python main.py --num_files 10 --num_rows 20 --file_name output --file_format csv --meta_file metadata.json
```

## Notes

- the app appends the appropriate extension to the output filename (.parquet, .csv, .json)
- Faker localization support is different per locale and provider ([see here for more](https://faker.readthedocs.io/en/master/locales.html))
