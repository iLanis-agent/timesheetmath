// Timesheet Math engine - clock-time arithmetic in whole minutes.
// Mirrored by oracle.py; keep the op order identical.

function _p2(n) {
  return (n < 10 ? "0" : "") + n;
}

function _num(x) {
  return String(x);
}

function _clock(str) {
  var m = /^(\d{1,2}):(\d{2})$/.exec(String(str).trim());
  if (!m || Number(m[1]) > 23 || Number(m[2]) > 59) throw new Error("time must look like 9:00 (24-hour clock)");
  return Number(m[1]) * 60 + Number(m[2]);
}

function _length(str) {
  var m = /^(\d{1,3}):(\d{2})$/.exec(String(str).trim());
  if (!m || Number(m[2]) > 59) throw new Error("each day must look like 7:45 (hours:minutes)");
  return Number(m[1]) * 60 + Number(m[2]);
}

function _hm(mins) {
  return Math.floor(mins / 60) + ":" + _p2(mins % 60);
}

function _dur(mins) {
  var h = Math.floor(mins / 60), r = mins % 60;
  if (h === 0) return r + " min";
  return r === 0 ? h + " h" : h + " h " + r + " min";
}

function _dec(mins) {
  var hh = Math.floor(mins * 100 / 60 + 0.5);
  return Math.floor(hh / 100) + "." + _p2(hh % 100);
}

// The shift truth: start, end and an unpaid break to time worked.
function shiftTruth(start, end, breakMin) {
  var s = _clock(start), e = _clock(end);
  if (s === e) throw new Error("start and end are the same time");
  if (!isFinite(breakMin) || breakMin % 1 !== 0 || breakMin < 0) throw new Error("break must be a whole number of minutes, 0 or more");
  var wrap = e < s;
  var span = wrap ? e + 1440 - s : e - s;
  if (breakMin > span) throw new Error("the break is longer than the shift");
  var worked = span - breakMin;
  return _hm(s) + " to " + _hm(e) + (wrap ? " (next day)" : "") + ", " + _dur(span) + " on the clock, " +
    breakMin + " min unpaid break: " + _dur(worked) + " worked, " + _dec(worked) + " decimal hours.";
}

// The week truth: day lengths to a total and an average.
function weekTruth(days) {
  var n = days.length;
  if (n < 1) throw new Error("enter at least one day");
  var total = 0;
  for (var i = 0; i < n; i++) total = total + _length(days[i]);
  var avg = Math.floor(total / n + 0.5);
  return n + " " + (n === 1 ? "day" : "days") + ": " + _dur(total) + ", " + _dec(total) + " decimal hours, " +
    _dur(avg) + " a day on average.";
}

// The decimal truth: decimal hours back to hours and minutes.
function decimalTruth(hours) {
  if (!isFinite(hours) || hours < 0 || hours > 1000) throw new Error("hours must be between 0 and 1000");
  var mins = Math.floor(hours * 60 + 0.5);
  return _num(hours) + " " + (hours === 1 ? "hour" : "hours") + " is " + _dur(mins) + ".";
}
