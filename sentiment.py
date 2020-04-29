# Theodore Rose ter9hb@virginia.edu 2/18/20
from google.cloud.language import types
from google.cloud.language import enums
from google.cloud import language
from pdfminer.high_level import extract_text
import os
from names_dataset import NameDataset
from collections import defaultdict
import string
from letter_info import Firm

c_file = open('companies.txt')
t_file = open('tickers.txt')

companies = c_file.read()
tickers = t_file.read()

companies_list = companies.split('\n')
tickers_list = tickers.split('\n')

tick_to_comp = {tickers_list[i]: companies_list[i]
                for i in range(len(tickers_list))}

important = {}

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/teros/Downloads/fund_letters/Fund Letters-71193e5ca35b.json"
m = NameDataset()

# Instantiates a client
client = language.LanguageServiceClient()

banned_items = {'CAGR', 'FCF', 'YTD', 'NYSE',
                'U.S.', 'EPS', 'ROE', 'ROIC',
                'P/E', 'LONG', 'EV', 'PE', 'FUND',
                'CFA', 'GDP', 'NAV', 'WTI', 'CFO', 'GM', 'NI',
                'CAC', 'COO', 'CTO', 'CIO' 'CDC', 'AI', 'CIO', 'LAWS', 'MTD', 'III',
                'MLP', 'BOE', 'LPG', 'NPV', 'HR', 'VC', 'DCF', 'MLP',
                'IT', 'MSCI', 'RHS', 'FAX', 'UBS', 'CEM', 'CO', 'ALL', 'HY', 'NET', 'NOV', 'CCC',
                'CASH', 'MD', 'CBOE', 'IP', 'YLD', 'MD', 'SP', 'TR', 'IG', 'CMBS', 'RMBS'}

pdfs = os.scandir(path="./2019 4Q")

encoding_type = enums.EncodingType.UTF8

for fund_letter in pdfs:
    try:
        print(F'processing letter {fund_letter.name}')

        text = extract_text(fund_letter)

        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        response = client.analyze_entity_sentiment(
            document=document, encoding_type=encoding_type)

        for entity in response.entities:
            name = enums.Entity.Type(entity.type).name
            if tick_to_comp.get(entity.name) and len(entity.name) > 1 and (entity.name.upper() not in banned_items):
                company = important.get(entity.name)
                if not company:
                    firm = Firm(
                        ticker=entity.name, company_name=tick_to_comp[entity.name])
                    important[entity.name] = firm

                firm = important[entity.name]

                if str(fund_letter.name) not in firm.mentions_list:
                    firm.mentions += 1

                    if entity.sentiment.score > 0.1:
                        firm.sentiment_list.append(entity.sentiment.score)

                    firm.mentions_list.append(str(fund_letter.name))

        # elif len(entity.name) < 20:
            # if name == "ORGANIZATION" or name == "PERSON":
                # if entity.name[0].upper() == entity.name[0] and entity.sentiment.magnitude > 0.05:
                # if entity.name.upper() not in banned_items:
                # important.add(
                # (entity.name, round(entity.sentiment.score, 4)))
    except:
        continue

final = list(important.items())
final.sort(key=lambda x: x[1].mentions, reverse=True)

returning = []
for item in final:
    item[1].make_avg()
    item[1].make_std_dev()
    returning.append(item[1])

text_file = open("results.txt", "w")

for obj in returning:
    text_file.write(str(obj))

text_file.close()
