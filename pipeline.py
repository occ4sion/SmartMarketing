import pickle
from pandas import read_csv, DataFrame
from numpy import vstack
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error as MSE
from sklearn.preprocessing import PolynomialFeatures
import clickhouse_connect

MODEL, X, Y, POLY = None, None, None, None


def init(path):

    global MODEL, X, Y, POLY

    company = read_csv(path+'company.csv', index_col='id')
    product = read_csv(path+'product.csv', index_col='id')
    user = read_csv(path+'user.csv', index_col='id')
    asset = read_csv(path+'asset.csv', index_col='id')
    AU = read_csv(path+'AssetUser.csv', index_col='id')
    AUG = read_csv(path+'AssetUserGroup.csv')
    campaign = read_csv(path+'campaign.csv', index_col='id')

    product_cols = ['price', 'novelty', 'uniqueness', 'conversion', 'popularity', 'volume', 'type']
    campaign[product_cols] = product.loc[campaign['product'], product_cols]
    AUG_ = AUG.loc[campaign.AUG, :].drop('price', axis=1)
    campaign['AU_activity'] = (AUG_ * AU.loc[:, 'activity'].values.T).sum(1).values
    campaign['AU_conversion'] = (AUG_ * AU.loc[:, 'conversion'].values.T).sum(1).values
    campaign['company_popularity'] = company.loc[product.loc[campaign['product'], 'company'], 'popularity'].values
    campaign['U_conversion'] = (AUG_ * user.loc[AU.loc[:, 'user'], 'conversion'].values.T).sum(1).values
    campaign['U_activity'] = (AUG_ * user.loc[AU.loc[:, 'user'], 'activity'].values.T).sum(1).values
    
    features = [
        'rounds', 'novelty', 'uniqueness', 'conversion', 'popularity', 'volume', 'AU_activity',
        'AU_conversion', 'price', 'company_popularity', 'U_conversion', 'U_activity'
    ]
    POLY = PolynomialFeatures(degree=4)
    X, Y = campaign[features], campaign['revenue']
    with open('model.pickle', 'rb') as file:
        MODEL = pickle.load(file)
    
    del company, product, user, asset, AU, AUG, campaign

def fit(path):
    global MODEL, X, Y, POLY
    init(path)

    scores = {'old': {'RMSE': None, 'R2': None}, 'new': {'RMSE': None, 'R2': None}}

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
    X_train = POLY.fit_transform(X_train)
    X_test = POLY.transform(X_test)

    scores['old']['RMSE'] = MSE(MODEL.predict(X_test), y_test, squared=False)
    scores['old']['R2'] = MODEL.score(X_test, y_test)

    MODEL.fit(X_train, y_train)

    scores['new']['RMSE'] = MSE(MODEL.predict(X_test), y_test, squared=False)
    scores['new']['R2'] = MODEL.score(X_test, y_test)

    with open('model.pickle', 'wb') as file:
        pickle.dump(MODEL, file)

    return scores

def predict(path):
    global MODEL, X, Y, POLY
    init(path)

    x = POLY.fit_transform(X)
    predictions = MODEL.predict(x)

    df = DataFrame(vstack([X.index.astype(int), predictions.T]).T, columns=['campaign', 'revenue'])
    df.to_csv(path+'predictions.csv', index=False)

    return True

def clickhouse(cmd, params):
    params = params.split(',')
    params = [param.split('=') for param in params]
    params = [[param.strip() for param in pair] for pair in params]
    params = dict(params)
    client = clickhouse_connect.get_client(params)
    return client.command(cmd)

def main():
    return 0

if __name__ == '__main__':
    main()