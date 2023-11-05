def read_data(path_file, cols=None):
    '''Reads data from a CSV file, converts it into a Pandas DataFrame, 
    and optionally selects specific column(s) from the DataFrame based on the 'cols' parameter.

    Args:
        path_file (str): The path to the CSV file to be read.
        cols (str, int, list, optional): The 'cols' parameter is optional and allows you to specify which column(s) to select from the DataFrame.
            - A single column name (as a string) or column index (as an integer) to select a specific column.
            - A list of column names (as strings) or column indices (as integers) to select multiple columns.
            - If 'cols' is not specified or set to None, the entire DataFrame will be returned.

    Returns:
        pd.DataFrame or pd.Series: The function returns a Pandas DataFrame or Series containing the selected data from the CSV file. 
        The DataFrame is indexed by the 'time' column with timezone information removed.
        - If 'cols' specifies a single column, the function returns a Series.
        - If 'cols' specifies multiple columns, the function returns a DataFrame.

    Example:
        To read the entire CSV file:
        >>> df = read_data('data.csv')

        To read and select specific columns by name:
        >>> df = read_data('data.csv', cols='Column1')
        >>> df = read_data('data.csv', cols=['Column1', 'Column2'])

        To read and select specific columns by index:
        >>> df = read_data('data.csv', cols=1)
        >>> df = read_data('data.csv', cols=[0, 2, 3])

    '''
    df = pd.read_csv(path_file)
    df.set_index('time', inplace=True)
    df.index = pd.to_datetime(df.index).tz_localize(None)

    if cols is not None:
        if isinstance(cols, str):
            df = df[cols]
        elif isinstance(cols, int):
            df = df.iloc[:, cols]
        elif isinstance(cols, float):
            raise ValueError("Column should be a string or integer or a list of eighter stings or integers.")
        elif isinstance(cols, list):
            if not (all(isinstance(col, (int)) for col in cols) or all(isinstance(col, (str)) for col in cols)):
                raise ValueError("Column list should only contain strings or integers.")
            if all(isinstance(col, int) for col in cols):
                df = df.iloc[:, cols]
            elif all(isinstance(col, str) for col in cols):
                df = df[cols]

    return df
