# EN
First, download the Chrome driver as a ZIP file from this website: https://googlechromelabs.github.io/chrome-for-testing/.
To find out your browser version, open Google Chrome, click on the three dots in the top-right corner, then go to Help > About Google Chrome. Here, you will see your browser version.
From the provided link, download the ZIP file with the closest version to your browser by clicking on Stable, Beta, etc. If the version does not match, clicking on About Google Chrome should trigger an automatic browser update. After the update, close and reopen the browser.
Make sure to save the ZIP file in the same folder as your Python script.
Next, install Selenium via the command line using this command:
**pip install selenium==4.2.0**
Then, open the Python script and make the following modifications:
**Line 25: Set the path to your chromedriver.exe file.**
**Line 427: Enter your Instagram username.**
**Line 428: Enter your Instagram password.**
**Line 429: Set the account you want to report.**
**Line 430: Set the number of repetitions.**
Save the changes and run the script by navigating to the script's folder in the command line and executing:
**python x.py**
# SK
Najprv si  stiahnite chrome driver ako zip z tejto stránky https://googlechromelabs.github.io/chrome-for-testing/. Verziu zistíte tak ,že klikneme v google chrome na tri bodky v pravom rohu . Potom klikneme na pomocník a potom informácie o prehliadaci a  tam uvidíme  verziu nášho prehliadača . Potom z toho linku si stiahneme zip kde na nabližia verziu k našmu prehliadaču ,klinutím na stable,beta ... .AK vám verzia nevyhovuje po klinutí na informácie o priehladači sa by vám  mala sama začať stahovať priehladač a potom treba zatvoriť a na novo otvoriť . Zip súbor musíte mať uložený v tom istom priečinku ako python súbor.
Potom si v príkazovom riadku stiahnite selenium cez tento príkaz pip **install selenium==4.2.0** . Otvorte potom python subor . Na riadku **25 si nastavte cestu k suboru chromedriver.exe**, na riadku **427 si napiste prihlasovacie meno** ,**428 dajte svoje heslo na instagram**,**429 nastavte účet ,ktorý chccete reportovať**,**430 nastavte pocet opakovani**. Uložte zmeny a program spustíite tak ,že v príkazovom riadku 
sa presunieme do priecinku kde je python subor a napsime **python x.py** 
