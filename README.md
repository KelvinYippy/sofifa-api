# SOFIFA-API

The SOFIFA-API is a Python API for the sofifa.com website. It provides features such as getting information on teams, players, player ratings for certain positions, and best lineups based on given formation.

## Code Structure
The API is structured into three main folders.

- Models hold the structure of the main data types of SOFIFA. 
- Routes hold the logic for the possible endpoints that can be called. 
- Tests are pytests meant to ensure the rigidity of the program. 

There are also three main files to look out for.

- dependencies.py holds abstracted logic commonly found throughout the program.
- utils.py contains various helper functions. 
- main.py holds the main router that runs the entire API.

## Dependencies

Your device should be able to support running Python programs. To ensure the program runs successfully, you may also need to run the following commands:

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip3 install requests
pip3 install bs4
pip3 install fastapi
pip3 install pedantic
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
