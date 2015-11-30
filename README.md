# FileParser
Python Module to parse log file and fetch desired lines

#Methods
<b>searchLine(pattern, count=1, start_from=0, match=0)</b><br>
Search string or pattern in log file. <br><br>
It returns a list of tuple having first value as line in which matched pattern or string is found, second value is line number, and third value is pointer to previous line<br><br>
e.g. To search first 2 occurances string 'MyStrig', <br>
     searchLine('MyStrig', count=2)

<b>reverseSearchFromLine(line_no, pattern)</b><br>
Search pattern in reverse direction from specified line number.<br><br>
Return type is same that of searchLine()

<b>fetchDataBetweenLines(start_pattern, end_pattern)</b><br>
Returns all the lines between the lines where start line is the line in which start_pattern is found and end line is the line in which end_pattern is found.

<b>fetchDataAroundLine(pattern, scope=0, up=None, down=None)</b><br>
Search for line having specified pattern. If found return x number of lines(scope) above and bellow the matched line including matched line. If up or down scope is specified, given number of lines will be fetched above and below respectively from matched line.

<b>goToStart</b><br>
Move pointer to the start of file.

<b>goToLine(lineno)</b><br>
Move file pointer to specified line number.

<b>readline</b><br>
Read current line.

<b>Property - currentLineNo</b><br>
Returns current line number.


