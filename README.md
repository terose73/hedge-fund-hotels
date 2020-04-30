Output from screener run on letters in /{year}_Q{quarter_number} is in **results.txt**

The interpretation for the sentiment score can be found at https://cloud.google.com/natural-language/docs/basics#interpreting_sentiment_analysis_values

Note: Please hook up a new google account with sufficient GCP credits before running, you should receive a service account JSON secret and place it in the respository. 

The updated google api key can be recieved
by following this guide
https://cloud.google.com/natural-language/docs/setup

Set GOOGLE_APPLICATION_CREDENTIALS path to the file path of the json secret, as well
as the path to a folder of PDF files by modifying the "pdfs" variable in sentiment.py

I.E. pdfs = os.scandir(path="./2020_Q1")

Average cost per run is around $25 for full scan for 500 MB of pdfs.


