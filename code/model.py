from sklearn.decomposition import SparsePCA
from sklearn.preprocessing import normalize

import numpy as np


class Model(object):

    def __init__(self, company_df, vocab, n_components=10):
        self.n_components = n_components
        self.company_df = company_df
        self.vocab = vocab
        self.factorization = None
        self.labels = None

    def fit(self, dif_df):
        factorization = SparsePCA(n_components=self.n_components, alpha=0.03)
        X = dif_df.values[1:]
        self.labels = dif_df.columns.values
        factorization.fit(X)
        self.factorization = factorization

    def transform(self, dif_df):
        # TODO: Make sure dif_df has the right columns.  Maybe we can be flexible,
        # but be sure to match up columns correctly and perhaps give a warning and fill
        # in zeros if we have missing columns.  If there are extra columns we might be
        # able to ignore that.
        '''
        From the fit function we have 'principle components' (vectors) c = [c_0, ..., c_{k-1}]
        which are stored in self.factorization.components_
        Given v, a vector representing one row of the ticker_df, we want to find (scalars) a = [a_0, ..., a_{k-1}]
        such that
                e = sum(a_i * c_i) - v
        is minimized.

        To do this we set a_i = dot(v, c_i) / ||c_i||_2

        :param dif_df:
        :return:
        '''

        # Matrix whose columns are normalized 'principle components'
        c = np.matrix(normalize(self.factorization.components_).T)

        # Matrix whose rows are percent changes of all the stocks
        v = np.matrix(dif_df.values)

        # Matrix of the projections of the v's onto the c's telling for example, how well biotech did
        # in a particular hour
        a = v * c

        return a

    def analyze_principle_component(self, component_num, n_companies=15, n_words=20):
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

        component = self.factorization.components_[component_num]
        component_labels = self.labels
        company_df = self.company_df
        vocab = self.vocab

        d = {}
        idx_con = np.argsort(component)[:n_companies]
        d['companies_con'] = component_labels[idx_con]
        d['importances_con'] = component[idx_con] * -1.

        idx_pro = np.argsort(component)[::-1][:n_companies]
        d['companies_pro'] = component_labels[idx_pro]
        d['importances_pro'] = component[idx_pro]

        word_importances_con = company_df.ix[d['companies_con'], :]['tfidf'].mean()
        word_idx_con = word_importances_con.argsort()[::-1][:n_words]
        d['words_con'] = np.array(vocab)[word_idx_con]
        d['word_importances_con'] = word_importances_con[word_idx_con]

        word_importances_pro = company_df.ix[d['companies_pro'], :]['tfidf'].mean()
        word_idx_pro = word_importances_pro.argsort()[::-1][:n_words]
        d['words_pro'] = np.array(vocab)[word_idx_pro]
        d['word_importances_pro'] = word_importances_pro[word_idx_pro]

        return d