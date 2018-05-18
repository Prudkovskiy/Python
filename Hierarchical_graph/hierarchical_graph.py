import pandas as pd
import numpy as np
import sys


def graph_traversal(matrix, issuer, own):
    """"""
    company = {}
    owner = {}
    own_comp = {}

    # create dict helping to indexing
    # companies in matrix
    for key in issuer:
        company[issuer[key]] = key
    for key in own:
        owner[own[key]] = key

    row = 0
    while row < len(matrix):
        col = 0
        while col < len(matrix[row]):
            if matrix[row, col] > 0.5:
                tmp = None
                # if the company in turn is the owner too,
                # change the owner of these companies
                if company[col] in own_comp:
                    tmp = own_comp.pop(company[col])

                # If there is no such owner in the answers,
                # then add it as a dictionary key
                if owner[row] not in own_comp:
                    own_comp[owner[row]] = [company[col]]
                # Otherwise, add another company to the
                # dictionary with this key
                else:
                    own_comp[owner[row]].append(company[col])

                # add the companies, which are
                # subordinate to the company, in owner
                if tmp is not None:
                    own_comp[owner[row]].extend(tmp)
                # reset the column to exclude
                # fake-owners of this company
                for i in range(len(matrix)):
                    matrix[i, col] = 0
                # if the company in turn is the owner too,
                # move all values from the company line
                # to the new owner line
                if company[col] in own:
                    row_idx = own[company[col]]
                    for i in range(len(matrix[0])):
                        matrix[row, i] += matrix[row_idx, i]
                        matrix[row_idx, i] = 0
                col = -1  # begin to cross the row again
            col += 1
        row += 1

    return own_comp


def make_matrix(df, col, row):
    """
    Create the adjacency matrix from the df data
    :param df: data
    :type: df: pd.DataFrame
    :param col: num of cols in matrix
    :param row: num of rows in matrix
    :return: matrix: adjacency matrix
    """
    n = len(row)
    m = len(col)
    matrix = np.zeros((n, m))
    for k in df.index:
        value = df.iloc[k].Percentage
        row_idx = row[df.iloc[k].Owner]
        col_idx = col[df.iloc[k].Issuer]
        matrix[row_idx, col_idx] = value
    return matrix


def make_keys(d):
    """
    Create values to the empty dictionary
    :param d: empty dict
    :type d: dict
    :return:
    """
    i = 0
    for key in d:
        d[key] = i
        i += 1


def main(input_file):
    # initialize the table using pandas lib
    df = pd.read_csv(input_file)
    df['Percentage'] = round(
        df['Percentage'].str.rstrip('%').astype('float') / 100,
        len(df.Percentage)
    )

    # create two dictionaries with unique
    # owner companies and issuer companies
    row = dict.fromkeys(set(df.Owner))
    col = dict.fromkeys(set(df.Issuer))

    # assign each value in dict a number of
    # row or column in the adjacency matrix
    # like {'OOO Материк': 0, 'OOO Лес': 1}
    make_keys(row)
    make_keys(col)
    # make adjacency matrix
    matrix = make_matrix(df, col, row)
    # get the result from our matrix
    # like { owner1: [comp1, comp2,...], owner2: [comp]...}
    result = graph_traversal(matrix, col, row)

    # create owner-company table
    comp_own = pd.DataFrame({
        'Company': [],
        'Owner': []
    })

    # full table with company
    for key in result:
        values = result.get(key)
        for val in values:
            df = pd.DataFrame({
                'Company': [val],
                'Owner': [key]
            })
            comp_own = comp_own.append(df, ignore_index=True)
    print(comp_own)
    # write the result table to the csv-file
    comp_own.to_csv('output.csv')


if __name__ == '__main__':

    if len(sys.argv) > 1:
        main(sys.argv[1].lower())

    else:
        print('invalid option. please use "python hierarchical_graph.py <input_file>"')
