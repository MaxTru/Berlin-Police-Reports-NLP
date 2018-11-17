#!/usr/bin/env bash
sed -i -r -e 's/([0-9][0-9])\.([0-9][0-9])\.([0-9][0-9][0-9][0-9])/\3-\2-\1/g' reports_cleaned_metadata_2018-10-21.dat