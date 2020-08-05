# RPDI Statistic
Random pick and assemble ingredients, count each combination and update the result to targeted Google sheet

## Version 0.9.0
Random ingredients combination statistic
- Set ingredient with configuration file
- Set picking size with configuration file
- Update result to Google Sheet
    1. Raw data
    1. Refined data

## Rules in config
- `Ingredients`
    - key: ingredient name
    - value: ingredient amount 
- `Pick`: amount of ingredient to choose each time
- `Google-Sheet`
    - `cred`: credential file name
    - `id`: target sheet id

## Usage
```
python3 statistic.py
```

## Error Codes:
`11` - Config `FileNotFoundError` from `conf_mod`
`12` - conf_mod `configError` Configuration problem in config file 