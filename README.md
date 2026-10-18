# Timesheet Math

Clock-time arithmetic in whole minutes. Clock times come in sixtieths, timesheets want hundredths, and somebody has to convert.

## What it computes

- **The shift truth** - start, end and an unpaid break to time worked and decimal hours: 9:00 to 17:30 with a 30 min break is 8 h, 8.00 decimal hours. An earlier end means the next day.
- **The week truth** - day lengths to a total, decimal hours and the average day: 7:45, 8:00, 7:30, 8:15, 7:45 is 39 h 15 min.
- **The decimal truth** - decimal hours back to hours and minutes: 7.75 hours is 7 h 45 min.

## Boundary

Arithmetic only. Timesheet Math adds and converts the times you type. It does not say what you are owed, what breaks or overtime the law or your contract requires, or what to put on a form. Your employer's rules and local law decide that.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (22 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/timesheetmath/
Repo: https://github.com/iLanis-agent/timesheetmath
