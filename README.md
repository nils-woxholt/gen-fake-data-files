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

The values can be any Faker provider.
These are coded in the `map_inputs_to_faker` function so you can add more there.

## Run

```bash
# run from the src folder
cd src
# let the program prompt you for inputs
python main.py
# OR
# pass the inputs at runtime
python main.py -n 10 -f output.csv -ft csv -m metadata.json
```
