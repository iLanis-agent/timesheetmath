#!/usr/bin/env python3
# Timesheet Math oracle - mirrors engine.js.
import json, math, re

def _num(x):
    return str(int(x)) if x == int(x) else repr(x)

def _clock(s):
    m = re.fullmatch(r"(\d{1,2}):(\d{2})", str(s).strip())
    if not m or int(m.group(1)) > 23 or int(m.group(2)) > 59:
        raise ValueError("time must look like 9:00 (24-hour clock)")
    return int(m.group(1)) * 60 + int(m.group(2))

def _length(s):
    m = re.fullmatch(r"(\d{1,3}):(\d{2})", str(s).strip())
    if not m or int(m.group(2)) > 59:
        raise ValueError("each day must look like 7:45 (hours:minutes)")
    return int(m.group(1)) * 60 + int(m.group(2))

def _hm(mins):
    return f"{mins // 60}:{mins % 60:02d}"

def _dur(mins):
    h, r = divmod(mins, 60)
    if h == 0:
        return f"{r} min"
    return f"{h} h" if r == 0 else f"{h} h {r} min"

def _dec(mins):
    hh = math.floor(mins * 100 / 60 + 0.5)
    return f"{hh // 100}.{hh % 100:02d}"

def shift_truth(start, end, break_min):
    s, e = _clock(start), _clock(end)
    if s == e:
        raise ValueError("start and end are the same time")
    if not math.isfinite(break_min) or break_min % 1 != 0 or break_min < 0:
        raise ValueError("break must be a whole number of minutes, 0 or more")
    wrap = e < s
    span = e + 1440 - s if wrap else e - s
    if break_min > span:
        raise ValueError("the break is longer than the shift")
    worked = span - int(break_min)
    return (f"{_hm(s)} to {_hm(e)}{' (next day)' if wrap else ''}, {_dur(span)} on the clock, "
            f"{int(break_min)} min unpaid break: {_dur(worked)} worked, {_dec(worked)} decimal hours.")

def week_truth(days):
    n = len(days)
    if n < 1:
        raise ValueError("enter at least one day")
    total = 0
    for d in days:
        total = total + _length(d)
    avg = math.floor(total / n + 0.5)
    return f"{n} {'day' if n == 1 else 'days'}: {_dur(total)}, {_dec(total)} decimal hours, {_dur(avg)} a day on average."

def decimal_truth(hours):
    if not math.isfinite(hours) or hours < 0 or hours > 1000:
        raise ValueError("hours must be between 0 and 1000")
    mins = math.floor(hours * 60 + 0.5)
    return f"{_num(hours)} {'hour' if hours == 1 else 'hours'} is {_dur(mins)}."

FNS = {"shiftTruth": shift_truth, "weekTruth": week_truth, "decimalTruth": decimal_truth}

CASES = [
    ("shiftTruth", ["9:00", "17:30", 30]), ("shiftTruth", ["09:00", "17:00", 0]),
    ("shiftTruth", ["22:00", "6:15", 45]), ("shiftTruth", ["8:00", "8:20", 20]),
    ("shiftTruth", ["9:00", "9:00", 0]), ("shiftTruth", ["9:00", "25:00", 0]),
    ("shiftTruth", ["9am", "17:00", 0]), ("shiftTruth", ["9:00", "10:00", 61]),
    ("shiftTruth", ["9:00", "17:00", 2.5]), ("shiftTruth", ["9:00", "17:00", -5]),
    ("weekTruth", [["7:45", "8:00", "7:30", "8:15", "7:45"]]),
    ("weekTruth", [["0:00", "0:00", "0:00", "0:00", "0:00"]]),
    ("weekTruth", [["8:00"]]), ("weekTruth", [["7:45", "8:61"]]), ("weekTruth", [["7:45", "eight"]]),
    ("weekTruth", [[]]),
    ("decimalTruth", [7.75]), ("decimalTruth", [1]), ("decimalTruth", [0.1]),
    ("decimalTruth", [38.33]), ("decimalTruth", [0]), ("decimalTruth", [-1]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
