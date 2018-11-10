 #!/bin/bash
 # This script will:
 # 1. Normalize the text of a file where each line represents a document to a Starspace-appropriate format
 # 2. Train Starspace based on the training dataset
 # 3. Test the trained Starspace model on a test dataset and store the resulst
 # 4. Apply the model to a full dataset and store the predicitons
 #
 # Requirements: this must run in the Starspace directory

 # Settings Inputs
TRAINDOCS="police_reports_data/reports_cleaned_payload_2018-10-21_sample_n=750.train"
TESTDOCS="police_reports_data/reports_cleaned_payload_2018-10-21_sample_n=750.test"
ALLDOCS="police_reports_data/reports_cleaned_payload_2018-10-21.dat"

# Settings Outputs
TRAINDOCS_NORM="police_reports_data/reports_cleaned_payload_2018-10-21_sample_n=750_normalized.train"
TESTDOCS_NORM="police_reports_data/reports_cleaned_payload_2018-10-21_sample_n=750_normalized.test"
ALLDOCS_NORM="police_reports_data/reports_cleaned_payload_2018-10-21_normalized.dat"
MODEL="police_reports_data/police-reports-model-simp"
TEST_RESULTS="police_reports_data/eval_results.txt"
PREDICTIONS="police_reports_data/predictions.txt"

# Clean-Up
rm -f $TRAINDOCS_NORM
rm -f $TESTDOCS_NORM
rm -f $ALLDOCS_NORM
rm -f $TEST_RESULTS
rm -f $PREDICTIONS

# Build
echo "Building Starspace..."
make
echo "Building Starspace... Done"
echo "Building query_predict..."
make query_predict
echo "Building query_predict... Done"

# Normalize input files
echo "Normalizing input files..."
normalize_text() {
  tr '[:upper:]' '[:lower:]' | \
    sed -e "s/'/ ' /g" -e 's/"//g' -e 's/\./ \. /g' -e 's/<br \/>/ /g' \
        -e 's/,/ , /g' -e 's/(/ ( /g' -e 's/)/ ) /g' -e 's/\!/ \! /g' \
        -e 's/\?/ \? /g' -e 's/\;/ /g' -e 's/\:/ /g' | tr -s " "
}

cat $TRAINDOCS | normalize_text > $TRAINDOCS_NORM
cat $TESTDOCS | normalize_text > $TESTDOCS_NORM
cat $ALLDOCS | normalize_text > $ALLDOCS_NORM

echo "Normalizing input files... Done"

# Train Starspace Model
echo "Training Starspace Model..."
./starspace train \
  -trainFile $TRAINDOCS_NORM \
  -model $MODEL \
  -initRandSd 0.01 \
  -adagrad false \
  -ngrams 1 \
  -lr 0.01 \
  -epoch 5 \
  -thread 20 \
  -dim 10 \
  -negSearchLimit 5 \
  -maxNegSamples 3 \
  -trainMode 0 \
  -label "__label__" \
  -similarity "dot" \
  -verbose true
echo "Training Starspace Model... Done"

# Test the trained model
echo "Testing the trained Model..."

./starspace test \
  -model $MODEL \
  -testFile $TESTDOCS_NORM\
  -ngrams 1 \
  -dim 10 \
  -label "__label__" \
  -thread 10 \
  -similarity "dot" \
  -trainMode 0 \
  -verbose true > $TEST_RESULTS

echo "Testing the trained Model... Done"

# Predicitons for full dataset
echo "Making predictions for full dataset..."
# First SED removes blank linse, 2nd removes all lines without starting enter some text, 3rd line kills beginning words prior to the predicted label
./query_predict $MODEL 1 < $ALLDOCS_NORM | sed '/^$/d' | sed '/^Enter some text/!d' | sed 's/Enter some text: 0\[[0-9].[0-9]*\]: //' > $PREDICTIONS
echo "Making predictions for full dataset... Done"