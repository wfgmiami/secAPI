# ChatGPT Similar Agency CMO bonds unsupervised ML
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Example CMO dataset
import numpy as np

features = np.random.rand(100, 5)  # Dummy features (e.g., WAC, OAS, duration)
min_features = min(features.ravel())
max_features = max(features.ravel())
print(f"Min feature = {min_features} Max feature = {max_features}")
# features:
# -Agency: Conv, GN
# -Model: EA, OAS
# -Cpn type: Fix, Flt
# -Cpn: 5.5
# -Collat Cpn: 6
# -WAL: 4.5
# -WALA: 18
# -Prin Wind: 1-20, 120-240
# 9 -OAS Model Proj LT CPR: 12.4

# Standardize features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
min_features_scaled = min(features_scaled.ravel())
max_features_scaled = max(features_scaled.ravel())
print(
    f"Min feature scaled = {min_features_scaled} Max feature scaled = {max_features_scaled}"
)

# Dimensionality reduction with PCA
pca = PCA(n_components=2)
features_pca = pca.fit_transform(features_scaled)
min_features_pca = min(features_pca.ravel())
max_features_pca = max(features_pca.ravel())
print(f"Min feature pca = {min_features_pca} Max feature pca= {max_features_pca}")

# Clustering with K-Means
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(features_pca)
print(len(clusters))

# Visualize clusters
plt.scatter(features_pca[:, 0], features_pca[:, 1], c=clusters, cmap="viridis", s=50)
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("Clustering of CMOs using K-Means")
plt.show()

# 1. At least 10 features that group similar bonds provided
# 2. Text features (eg GNMA agency) converted to numbers
# 3. Selected features standardized
# 4. Using PCA features reduced to smaller number - eg 4 Cpn/Collat Cpn/WAL/WALA (most significant ones)
# 5. Choose number of clusters to be used in the KMeans
# 6. Eeach bond of a list of bonds will have the 4 features, those 4 features will be assigned to cluster
# 7. Average distance from each point to the cluster will be calculated
# 8. Step 6 and 7 will be repeated until the average distance is not changing
# 9. The predication for a new bond will be based on which cluste its 4 features fall into
# 10. All the bonds which points are in that cluster will be considered comparable bonds

# Unsupervised Learning with k-NN
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# Load and preprocess data
data = pd.read_csv("agency_cmo_bonds.csv")  # Example dataset
features = ["coupon_rate", "oas", "duration", "wac", "wala", "prepayment_speed"]
X = data[features]

# Normalize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fit k-Nearest Neighbors
knn = NearestNeighbors(n_neighbors=5, metric="euclidean")
knn.fit(X_scaled)

# Find similar bonds for a new bond
new_bond = pd.DataFrame(
    [[2.5, 80, 5.2, 3.5, 12, 10]], columns=features
)  # Example new bond
new_bond_scaled = scaler.transform(new_bond)

distances, indices = knn.kneighbors(new_bond_scaled)
similar_bonds = data.iloc[indices[0]]
print(similar_bonds)


# Supervised Learning with XGBoost
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Example labeled dataset (1 = comparable, 0 = not comparable)
X = data[features]
y = data["is_comparable"]  # Historical labels
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train XGBoost
model = XGBClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Predict on new bond
new_bond_pred = model.predict(new_bond)
print("Prediction:", new_bond_pred)


# Generate Synthetic Data
import pandas as pd
import numpy as np

np.random.seed(42)
n_bonds = 500

data = {
    "bond_id": [f"BOND_{i+1}" for i in range(n_bonds)],
    "coupon": np.random.randint(8, 14, n_bonds) / 4,
    "collat_coupon": np.random.randint(8, 14, n_bonds) / 4,
    "wal": np.random.uniform(1.0, 15.0, n_bonds),
    "wala": np.random.randint(0, 121, n_bonds),
    "prepayment_speed": np.random.uniform(5.0, 25.0, n_bonds),
    "oas": np.random.uniform(50, 200, n_bonds),
    "convexity": np.random.uniform(-1.0, 3.0, n_bonds),
    "spread_to_treasury": np.random.uniform(0.5, 2.5, n_bonds),
}

synthetic_bonds = pd.DataFrame(data)
synthetic_bonds.to_csv("agencycmo.csv", index=False)

# Unsupervised Learning with k-NN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

data = pd.read_csv("agencycmo.csv")
features = ["coupon", "collat_coupon", "wal", "wala", "oas", "prepayment_speed"]
X = data[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

knn = NearestNeighbors(n_neighbors=5, metric="euclidean")
knn.fit(X_scaled)

new_bond = pd.DataFrame([[2.5, 3, 3.8, 8, 100, 6]], columns=features)
new_bond_scaled = scaler.fit_transform(new_bond)

distances, indices = knn.kneighbors(new_bond_scaled)
similar_bonds = data.iloc[indices[0]]
print(similar_bonds)
