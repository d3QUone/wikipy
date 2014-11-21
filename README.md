wikipy
======

Collection of Python 2.7.8-made tools to get the biggest list of well known people from "Wikipedia"

<h4>Some ideas how to make this to work:</h4>
1) Using Semantic search in DBpedia: create different triple searches, check graphs and parse the result.<br>Use <code>rdflib, json</code>

2) Manually find all wikipedia lists with people, parse them for links and parse the target pages.<br>Use <code>bs4, json, requests, threading</code>, etc.

<h4>As a result the script was based on the 2nd idea. </h4>

===
<h4>Features list:</h4>

<ul>
<li><s>Parse wikipedia lists for endpoint links to personal pages</s></li>
<li><s>Parse personal page for Full name, Nickname, B-date, D-date, Role/Occupation</s></li>
<li><s>Save data into CSV file</s></li>
<li><s>Intergate indexing system</s></li>
<li>Improve parsing personal data</li>
<li>Intergate multi threading system</li>
<li>Optimize:)</li>
</ul>


===
<h4>Usage:</h4>

1) Save all needed links to lists of personal pages to the <code>lists.txt</code> file

2) Run <code>main.py</code> and get the result in <code>output.csv</code>
