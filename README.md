<b>wikipy</b> - collection of Python 2.7.8-made tools to get the biggest list of well known people from "Wikipedia"
<hr>

<b>Some ideas how to make this to work:</b>

1) Using Semantic search in DBpedia: create different triple searches, check graphs and parse the result.<br>Use <code>rdflib, json</code>

2) Manually find all wikipedia lists with people, parse them for links and parse the target pages.<br>Use <code>bs4, requests</code> modules

<b>As a result the script was based on the 2nd idea</b>
<hr>
<h4>Features list:</h4>

<ul>
<li><s>Parse wikipedia lists for endpoint links to personal pages</s></li>
<li><s>Parse personal page for Full name, Nickname, B-date, D-date, Role/Occupation</s></li>
<li><s>Save data into CSV file</s></li>
<li><s>Intergate indexing system</s></li>
<li><s>Improve parsing personal data</s></li>
<li>Intergate multi threading system</li>
<li>Optimize:)</li>
</ul>

Parses not only wikipedia (a huge set of script)
