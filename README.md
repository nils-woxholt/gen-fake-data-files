# gen-fake-data-files

A command line app to generate fake data files as parquet or csv by providing a metadata file which defines the data.
(this is an early commit and still work in progress so expect updates!)

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

Create a json file where the keys will be the column names and the values will be the data types

```json
{
    "Name": "name",
    "Address": "address",
    "Date": "date",
    "BookingDate": "date_this_month",
    "DestinationCity": "city",
}
```

The values can be any Faker provider (currently only providers with no additional paramaters are supported).
These are coded in the `map_inputs_to_faker` function so you can add more there.

## Run

```bash
cd src

python main.py -n 1000 -f output.csv -ft csv -m metadata.json
```
