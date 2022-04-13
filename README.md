# cse573-stock-prediction

If editing .tex files with a lateX editor like texmaker

The following may be necessary if running linux:
sudo apt-get install texlive-science

### Necessary Dependencies ###
Flask
Selenium
BeautifulSoup4

### Running Server ###
1. Change endpoints in main.js to reflect your ip address:5000
2. Change self.host in server/server.py to reflect your ip address
3. Change CHROMEDRIVER_PATH to your chromedriver path in server/server.py (must install selenium and chromedriver)

### Steps to run the application ###
1. Run/start server.py
2. Head over to the interface directory and run index.html in any desired web-browser (Tested on Safari 15.3)
3. In the textbox, paste a valid Twitter tweet link (Sample tweet: https://twitter.com/elonmusk/status/1026872652290379776)
4. After pasting a valid tweet, click the "Predict Stock Direction" button
5. Five items will appear: (1) The embed tweet of the link (2) The overall stock direction (3) The stock direction for model 1 (4) The stock direction for model 2 (5) The stock direction for model 3. 
6. The stock direction will showcase up or down.


