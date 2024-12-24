CSV=../csv
FULL_CSV=$(realpath $CSV)
FILE=uscis_questions
rm $CSV/$FILE.csv
osascript ./uscis_questions.applescript $FULL_CSV/$FILE.numbers $FULL_CSV/$FILE.csv
echo "Generated:"
ls -l $CSV/$FILE.csv
