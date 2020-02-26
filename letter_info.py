import statistics


class Firm:

    def __init__(self, ticker, company_name):
        self.mentions = 0
        self.mentions_list = []
        self.sentiment_list = []
        self.ticker = ticker
        self.company_name = company_name
        self.stdev = 0
        self.avg = 0

    def make_avg(self):
        try:
            self.avg = round(statistics.mean(self.sentiment_list), 4)
        except:
            pass

    def make_std_dev(self):
        try:
            self.stdev = round(statistics.stdev(self.sentiment_list), 4)
        except:
            pass

    def __str__(self):
        print(F"Company Name: {self.company_name}")
        print(F"Ticker: {self.ticker}")
        print(F"Total Mentions: {self.mentions}")
        print(F"Letters Mentioned In: {self.mentions_list}")
        if self.avg != 0:
            print(F"Mean Sentiment: {self.avg}")
        if self.stdev != 0:
            print(F"Std. Dev Sentiment: {self.stdev}")

        return(F"Company Name: {self.company_name} \n Ticker: {self.ticker} \n Total Mentions: {self.mentions} \n Letters Mentioned In: {self.mentions_list} \n Mean Sentiment: {self.avg} \n Std. Dev Sentiment: {self.stdev} \n")
