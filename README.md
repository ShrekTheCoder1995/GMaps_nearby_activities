<h1>Finding all nearby locations of a certain type, based on a given address</h1>

<h2>Goal</h2>
This Python-application aims to help people to decide where they should go on vacation, by finding interesting possible activities nearby. The user provides a (collection of) address(es) and the application makes a ready-to-analyze Excel File that inventorizes activities to do near each of them, using the Google-Maps-API. Examples of identified vacation-like activities are: swimming pools, VR-/lasertag games and amusement parks.

<h2>Structure</h2>
The base folder contains 2 important folders:<br><br>
<ul>
<li>
src: here are all the scripts necessary to run the application. 

</li>
<br>
<li>
data: which contains 2 folders:
<ul>
    <li>raw: here, the file that contains initially provided possible vacation addresses is stored.</li>
    <li>processed: here, the file that contains all interesting nearby activity locations per address is stored.</li>
</ul>
</li>

</ul>

<h2>Installation (one time only)</h2>
<ol>
    <li>Install all dependencies via poetry by typing <code>poetry install</code> in the terminal</li>
    <li>Generate an API-key, following the steps of <a href="https://developers.google.com/maps/documentation/embed/get-api-key">this link</a>. It's completely free, but you need a Google-account.</li>
    <li>In the base folder, make a .txt-file and name it <code>gmaps_api_key</code>. Place your generated API-key in this file (don't surround it with single or double quotes). Make sure you close it when you continue to the next step.</li>
</ol>

<h2>Usage</h2>
<ol>
    <li>Open the search_terms.txt-file in the base folder. Here, you specify all nearby activity types that you want Google Maps to search for. Put each type on a separate line. The first time you use this application, you see my example of filling this file. Feel free to change it to your own search terms! </li>
    <li>Run main.py (in the src-folder), make sure you have an active internet connection. After running, open the Excel-file "Huisjes" (data-folder -> processed-folder). You can now start analyzing and choosing your favorite vacational activities, enjoy! :-)</li>
</ol>
