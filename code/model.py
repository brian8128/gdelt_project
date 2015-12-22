from sklearn.decomposition import SparsePCA
import numpy as np


# Encapsulate the model. Once constructed class should have all the information needed
# to quickly generate a report about an hours worth of trading data.

# TODO: provide a way to see how much of the variance is explained by the model

class Model(object):
    # Number of 'principle components' in the model
    n_components = -1
    # Pandas index containing the companies that the model uses
    company_df = None
    factorization = None
    vocab = None

    def fit(self, dif_df, company_df, vocab, n_components=7):
        # Subsets the ticker_df to limit to what's also in the company_df
        self.n_components = n_components
        self.vocab = vocab

        # We only want to use data that is present in both of our data frames
        idx = company_df.index.intersection(dif_df.columns)
        dif_df = dif_df.loc[:, idx]
        self.company_df = company_df = company_df.loc[idx, :]

        # Get the data.  The first row of X is all zeros so drop it.
        X = dif_df.values[1:]

        # TODO: This is sort of cowboy science.  We need to figure out a way
        # to statistically test which companies actually belong in which components
        # probably using a p test to prove that the correlation is not random.
        # We also want to test how many components are really there in the data
        # because we could generate as many components as we want but at some point
        # the components are just explaining random fluctuations in the data
        self.factorization = SparsePCA(n_components=n_components, alpha=0.03)
        self.factorization.fit(X)


    def transform(self, company_df):
        # Subsets company_df
        # prints a warning if there are companies missing, and fills them with zeros
        # Returns: a data frame with one column per component and one column for the error term
        pass

    def get_component(self, component_number):
        # Returns a numpy array that gives the weight of each company in the component
        return self.factorization.components_[component_number]

    def get_company_df(self):
        '''
        Returns a data frame with info about the companies being used in the model
        Note that this may not contain all the rows that were in the input comapny_df
        because we subset based on what data is also in the dif_df.
        '''
        return self.get_company_df()

    def get_vocab(self):
        return self.vocab

    def get_component_info(self, component_df, n_companies=20, n_words=20):
        '''
        component: 1d numpy array representing a linear combination of companies
        component_labels: the ticker symbols of the companies from component
        company_df: pandas dataframe with index ticker symbols, a column 'description' with a
                    text description of the company and a column 'tfidf' a tfidf vector
        vocab: the vocab for the tfidf vector above

        returns: A dictionary with the following information about the company:
                    'companies_pro': Numpy array of ticker symbols of the top n_companies
                                     companies associated with this component
                    'importances_pro': Numpy array of floats that tell the weight of the
                                       above companies in the principle component
                    'companies_con': Numpy array of ticker symbols of the top n_companies
                                     companies anti-correlated with this component
                    'importances_con': Numpy array of floats that tell the weight of the
                                       above companies in the principle component
                                       (these numbers are positive, measuring the anti-correlation)
                    'words_pro':
                    'word_importances_pro':
        '''
        d = {}
        idx_con = np.argsort(component)[:n_companies]
        d['companies_con'] = component_labels[idx_con]
        d['importances_con'] = component[idx_con] * -1.

        idx_pro = np.argsort(component)[::-1][:n_companies]
        d['companies_pro'] = component_labels[idx_pro]
        d['importances_pro'] = component[idx_pro]

        # TODO: Weight the word importances by the company importance
        word_importances_list_con = company_df.ix[d['companies_con'], :]['tfidf']
        weighted_word_impt_list_con = word_importances_list_con.multiply(d['importances_con'], fill_value=0)

        word_importances_con = weighted_word_impt_list_con.mean()
        #word_importances_con = company_df.ix[d['companies_con'], :]['tfidf'].mean()
        word_idx_con = word_importances_con.argsort()[::-1][:n_words]
        d['words_con'] = np.array(vocab)[word_idx_con]
        d['word_importances_con'] = word_importances_con[word_idx_con]

        word_importances_list_pro = company_df.ix[d['companies_pro'], :]['tfidf']
        weighted_word_impt_list_pro = word_importances_list_pro.multiply(d['importances_pro'], fill_value=0)

        word_importances_pro = weighted_word_impt_list_pro.mean()
        #word_importances_pro = company_df.ix[d['companies_pro'], :]['tfidf'].mean()
        word_idx_pro = word_importances_pro.argsort()[::-1][:n_words]
        d['words_pro'] = np.array(vocab)[word_idx_pro]
        d['word_importances_pro'] = word_importances_pro[word_idx_pro]

        return d