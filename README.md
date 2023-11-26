# WebUntis-Viewer
Eine verbesserte Version vom Vertretungsplan auf der Website kephiso.Webuntis

Anfängerprojekt! Teile des Codes sind KI generiert.

Free to Download und Free to use


if you want to use this one on another school than bbs friesoythe, you need to do some things first. 

1. Open the Python script "Viewer.py"
2. Get your Data from webuntis
3. to do so, open the website where your timetable is. you should find the link on your schools website. The app is not supported.
4. Press f12 to open the developer tools.
5. Go to "Network"
6. Press ctrl + r to reload
7. there are a lot of things now. find something called data?school=..... there should be only one
8. Right click > copy > copy as cUrl (bash)
9. open "https://curlconverter.com/python/"
10. copy your cUrl command there and select "Python" > "requests" if it wasnt selected by default. i think it wouldnt work with "http client" 
11. copy the script and delete "import requests. and the multi-line comment at the end.
12. Place your Data in the "get_data_from_Webuntis" function (its somewhere at the beginning)
13. i added comments there, so just delete everything between them and replace it with the code you got.

14. now hope that it works. i tried it with another school than my and got the data. but the format was another wich caused some errors in displaying the data. maybe you need to fix some things there.

15. too run the script, you need to have installed python and the needed python packages on your computer. you can download python on "https://python.org" and the packages over the cmd or powershell via "pip install requirements.txt"
16. make sure to open the cmd in the same folder where the .txt file is located.

17. maybe you want to build a .exe now?
18. use "pip install py2exe" and "pip install auto-py-to-exe" for that. now hope that everything works. 

