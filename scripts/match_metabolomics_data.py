#!/usr/bin/env python

import collections
import csv
import pandas

# Parse (HMDB_ID => SAS_NAME) from metadata.
def parse_metadata(filename):
  relevant_metadata = {}
  with open(filename, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      hmdb_id = row['HMDB_ID']
      if hmdb_id.startswith('HMDB'):
        sas_name = row['SAS_NAME'].upper()
        if sas_name.startswith('_'):
          sas_name = 'X' + sas_name
        relevant_metadata[hmdb_id] = sas_name
  return relevant_metadata

# Prune dataset.  Keep first column and specified SAS names.
def prune_data(dataset, sas_names):
  with open(dataset + '.csv', 'rb') as csv_in:
    reader = csv.DictReader(csv_in)
    with open(dataset + '_pruned.csv', 'w') as csv_out:
      fieldnames = [''] + sas_names
      writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
      writer.writeheader()
      for in_row in reader:
        out_row = {}
        out_row[''] = in_row['']
        for sas_name in sas_names:
          out_row[sas_name] = in_row[sas_name]
        writer.writerow(out_row)

# Deal with missing values.
def fill_missing_values(dataset):
  df = pandas.read_csv(dataset + '_pruned.csv', index_col=0)

  # Compute replacement values for each column:
  # half of the lowest non-zero (positive) value.
  replace_by_col = {}
  for (col_name, series) in df.iteritems():
    replace_by_col[col_name] = min(i for i in series if i > 0) / 2

  # Do the replacement and write the data back out to disk.
  df.fillna(value=replace_by_col, inplace=True)
  df.to_csv(dataset + '_cleaned.csv')

  # Normalize too while we're here.
  df = df.div(df.median(axis=1), axis=0)
  df.to_csv(dataset + '_normalized.csv')


# Main execution begins here.

# Extract the metadata that we're interested in.
broad_metadata = parse_metadata('broad_metadata.csv')
metabolon_metadata = parse_metadata('metabolon_metadata.csv')

# Get column names for shared HMDB_IDs.
shared_hmdb_ids = set(broad_metadata.keys()) & set(metabolon_metadata.keys())
broad_columns = []
metabolon_columns = []
for hmdb_id in shared_hmdb_ids:
  broad_columns.append(broad_metadata[hmdb_id])
  metabolon_columns.append(metabolon_metadata[hmdb_id])

# Prune data, removing irrelevant columns.
prune_data('broad', broad_columns)
prune_data('metabolon', metabolon_columns)

# Deal with N/As and normalize.
fill_missing_values('broad')
fill_missing_values('metabolon')
