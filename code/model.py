# Encapsulate the model. Once constructed class should have all the information needed
# to quickly generate a report about an hours worth of trading data.

class Model(object):
    n_components = -1

    def fit(self, company_df, ticker_df, n_components=7):
        # Subsets the ticker_df to limit to what's also in the company_df
        self.n_components = n_components

    def transform(self, company_df):
        # Subsets company_df
        # prints a warning if there are companies missing, and fills them with zeros
        # Returns: a data frame with one column per component and one column for the error term

    def get_component(self, component_number):
        # Returns a numpy array that gives the weight of each company in the component

    def get_ticker_df(self):
        # Returns a data frame with info about the companies being used in the model

    def get_vocab(self):
        # 