import pandas as pd

train = pd.read_csv("train.csv")
train.head()

test = pd.read_csv("test.csv")
test.head()

print("Train shape: " , train.shape)
print("Test shape: ",test.shape)

print(train.dtypes)

X = train[['fire_location_latitude', 'fire_location_longitude', 'fire_origin', 'true_cause', 'fire_type', 'weather_conditions_over_fire', 'fuel_type']]
X.head()

y = train['size_class']
y.unique()

null_value_stats = X.isnull().sum(axis=0)
null_value_stats[null_value_stats != 0]

X = X.fillna('Unknown') 

from sklearn.model_selection import train_test_split
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.75, random_state=42)

import category_encoders as ce

ohe = ce.OneHotEncoder(handle_unknown='value', use_cat_names=True)
X_train_ohe = ohe.fit_transform(X_train)
X_train_ohe.sample(5)

X_valid_ohe = ohe.transform(X_valid)
X_valid_ohe.sample(5)

from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train_ohe, y_train)

importance = pd.DataFrame()
importance['Feature'] = X_train_ohe.columns
importance['Importance'] = model.feature_importances_
importance.set_index('Feature', inplace=True)

importance.sort_values(by='Importance', ascending=False)

import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

plt.figure(figsize=(20,15))
plot_tree(model, max_depth=3, feature_names=X_train_ohe.columns, filled=True, fontsize=10)
plt.show()

y_valid_pred = model.predict(X_valid_ohe)

from sklearn.metrics import accuracy_score

print('Validation accuracy score:', accuracy_score(y_valid, y_valid_pred))

pd.DataFrame(y_valid, columns=['size_class'])['size_class'].value_counts()

from sklearn.metrics import f1_score

print('Macro F1-score:', f1_score(y_valid, y_valid_pred, average='macro'))

from sklearn.metrics import plot_confusion_matrix

class_names = y_valid.unique()

# Plot non-normalized and normalized confusion matrices
titles_options = [("Confusion matrix, without normalization", None),
                  ("Normalized confusion matrix", 'true')]

for title, normalize in titles_options:
    disp = plot_confusion_matrix(model, X_valid_ohe, y_valid,
                                 labels=class_names,
                                 cmap=plt.cm.Blues,
                                 normalize=normalize)
    disp.ax_.set_title(title)

plt.show()



