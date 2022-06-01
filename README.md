# Quick and dirty instant runoff voting tabulator.

To use this make a Google form with a number of questions following the pattern
'CATEGORY NAME - first choice', 'CATEGORY NAME - second choice', etc.

Then export the spreadsheet containing the results as a .csv. Run `irv.py` with
the filename of the CSV as the first argument.
