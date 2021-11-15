# Find Nan values in a column
def nanCount(dataframe,column_name):
    """
    :param dataframe: the dataframe to be used
    :param column_name: Input the column name of a dataframe for which we want to find number of NaN values
    :return: Number of Nan Values in a column in a dataframe
    """
    notNan,areNan = dataframe[column_name].isna().value_counts()
    return areNan
ḍ
