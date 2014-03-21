# Relative Dates Alfred Workflow #

Generate relative dates based on a simple input format and your own date formatting parameters (there are some default placeholders you can delete).

Supports multiple locales/languages.

![](https://github.com/deanishe/alfred-relative-dates/raw/master/demo.gif "")

## Downloading ##

Get the workflow from [GitHub](https://github.com/deanishe/alfred-relative-dates/raw/master/Relative%20Dates.alfredworkflow) or [Packal](http://www.packal.org/workflow/relative-dates).

## Keywords ##

- `date` — Generate a formatted date using the [input format][]
	+ `↩` — Copy date to clipboard
	+ `⌘+↩` — Copy date to clipboard and paste into frontmost app
- `datehelp` — Open (this) help file
- `dateformats` — View saved date formats
	+ `⌘+↩` — Delete date format
- `dateadd` — Add a new date format
	+ `↩` — Save the date format
- `datereset` — Reset the saved date formats to the defaults


## Input format ##

`(+/-)<NUM>(w|d|y)` where `w` = week(s), `d` = day(s) and `y` = year(s)

You needn't specify a sign: `+` is understood as the default, so `+1d` and `1d` mean the same thing.

Months are not supported, as it leads to ambiguity: what if today is the 31st, but the target month only has 30 days? Similarly, a year is naively defined as 365 days.

### Examples ###

- `0` = `now` = `today` — today's date
- `1d` — 1 day from now
- `7d` = `1w` — 1 week from now
- `-21d` = `-3w` — 3 weeks ago


## Supported formats ##

The Workflow includes a few defaults for the locales `en_US`, `en_GB` and `de_DE`.

You can specify your own custom date formats using the following symbols, and you can also specify a language (locale) with the format `lang=de` or `lang=de_DE` if you want to use dates formatted for a language different to your system's.

| Symbol |                                                                                   Description                                                                                    |                                     Examples                                     |
|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| %a     | Weekday as locale’s abbreviated name.                                                                                                                                            | Sun, Mon, ..., Sat (en_US); So, Mo, ..., Sa (de_DE)                              |
| %A     | Weekday as locale’s full name.                                                                                                                                                   | Sunday, Monday, ..., Saturday (en_US); Sonntag, Montag, ..., Samstag (de_DE)     |
| %w     | Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.                                                                                                                | 0, 1, ..., 6                                                                     |
| %d     | Day of the month as a zero-padded decimal number.                                                                                                                                | 01, 02, ..., 31                                                                  |
| %b     | Month as locale’s abbreviated name.                                                                                                                                              | Jan, Feb, ..., Dec (en_US); Jan, Feb, ..., Dez (de_DE)                           |
| %B     | Month as locale’s full name.                                                                                                                                                     | January, February, ..., December (en_US); Januar, Februar, ..., Dezember (de_DE) |
| %m     | Month as a zero-padded decimal number.                                                                                                                                           | 01, 02, ..., 12                                                                  |
| %y     | Year without century as a zero-padded decimal number.                                                                                                                            | 00, 01, ..., 99                                                                  |
| %Y     | Year with century as a decimal number.                                                                                                                                           | 1970, 1988, 2001, 2013                                                           |
| %p     | Locale’s equivalent of either AM or PM.                                                                                                                                          | AM, PM (en_US); am, pm (de_DE)                                                   |
| %j     | Day of the year as a zero-padded decimal number.                                                                                                                                 | 001, 002, ..., 366                                                               |
| %U     | Week number of the year (Sunday as the first day of the week) as a zero padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0. | 00, 01, ..., 53                                                                  |
| %W     | Week number of the year (Monday as the first day of the week) as a decimal number. All days in a new year preceding the first Monday are considered to be in week 0.             | 00, 01, ..., 53                                                                  |
| %x     | Locale’s appropriate date representation.                                                                                                                                        | 08/16/88 (None); 08/16/1988 (en_US); 16.08.1988 (de_DE)                          |
| %%     | A literal '%' character.                                                                                                                                                         | %                                                                                |


### Examples ###

- `%d/%m/%Y` — e.g. 21/01/2014
- `%A %B %d %Y` — e.g. Wednesday March 12 2014
- `%A %d. %B %Y lang=de` — e.g. Mittwoch 12. März 2014


## Bug reports, feedback ##

Report any issues or feature requests either on [GitHub](https://github.com/deanishe/alfred-relative-dates/issues) or the [Alfred Forum](http://www.alfredforum.com/topic/4056-relative-dates/).

## Licensing, thanks etc. ##

This Workflow is released under the [MIT Licence](http://opensource.org/licenses/MIT).

It uses the [docopt](https://github.com/docopt/docopt) library.
