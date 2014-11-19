wikipy
======

Collection of Python 2.7.8 made tools to get the biggest list of well known people from "Wikipedia"

<h4>Some ideas how to make this:</h4>
1) Using Semantic web machnism and DBpedia, create different searches, check and parse the result.<br>Use <code>rdflib, json</code>

2) Manually find all wikipedia lists with people, parse them for links and parse the target pages.<br>Use <code>bs4, json, requests, threading</code>, etc

As a result the script was based on the 2nd idea. 

===
<h4>Features list:</h4>

<ul>
<li><s>Parse wikipedia lists for endpoint links to personal pages</s></li>
<li><s>Parse personal page for Full name, Nickname, B-date, D-date, Role/Occupation</s></li>
<li><s>Save data into CSV file</s></li>
<li>Intergate indexing system</li>
<li>Intergate multi threading system</li>
<li>Optimize:)</li>
</ul>
