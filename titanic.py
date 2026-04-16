from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

class TitanicPreprocessor:
    
    def __init__(self, age_fitter: str = "mean", farebins: bool = True):
        self.imputations = {}
        self.encoders = {}
        self.fitted = False
        self.farebins = farebins
        self.age_fitter = age_fitter

    def fit(self, X: pd.DataFrame) -> None:
        # 1: Decode Categorical Features
        cat_features = ["Pclass", "Sex", "Cabin", "Embarked"]
        
        # "Sex"
        le_sex = LabelEncoder()
        le_sex.fit(X["Sex"])
        self.encoders["Sex"] = le_sex

        # "Embarked"
        le_embarked = LabelEncoder()
        le_embarked.fit(X["Embarked"])
        self.encoders["Embarked"] = le_embarked

        # "Cabin"
        cabin_column = df_X["Cabin"].fillna("Unknown").apply(lambda row: row[0])
        cabin_column = cabin_column.replace({"T": "R", "G": "R"})
        le_cabin = LabelEncoder()
        le_cabin.fit(cabin_column)
        self.encoders["Cabin"] = le_cabin

        # 2: "Name"
        status_column = X["Name"].str.extract(r"([A-Za-z]+)\.")
        status_replace_dict = {i: "Rare" for i in ['Lady', 'Countess','Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona']}
        status_replace_dict['Mlle'] = 'Miss'
        status_replace_dict['Ms'] = 'Miss'
        status_replace_dict['Mme'] = 'Mrs'
        self.imputations["Name"] = status_replace_dict
        status_column = status_column.replace(status_replace_dict)
        le_status = LabelEncoder()
        le_status.fit(status_column)
        self.encoders["Status"] = le_status

        # 4: "Fare"
        if self.farebins:
            _, self.imputations["Fare"] = pd.qcut(X["Fare"], 5, retbins=True)
            self.imputations["Fare"][-1] = np.inf
            farebins_column = pd.cut(X["Fare"], self.imputations["Fare"])
            le_farebins = LabelEncoder()
            le_farebins.fit(farebins_column)
            self.encoders["FareBins"] = le_farebins

        # 5: "Age"
        self.imputations["Age"]=[0, 5, 12, 18, 35, 60, 100]
        X_age = X.copy()[["Age", "Pclass"]]
        X_age["Status"] = le_status.transform(status_column)
        X_age["FamilySize"] = X["SibSp"] + X["Parch"]
        X_age = X_age.dropna(subset=["Age"])
        agebins_column = pd.cut(X_age["Age"], self.imputations["Age"])
        le_agebins = LabelEncoder()
        le_agebins.fit(agebins_column)
        X_age["AgeBins"] = le_agebins.transform(agebins_column)
        self.encoders["AgeBins"] = le_agebins
        # mean imputation
        if self.age_fitter == "mean":
            self.imputations["AgeBins"] = X_age["AgeBins"].mean().round()
        elif self.age_fitter == "mean+":
            age_class_imputations = X_age.groupby(["Pclass", "Status"])["AgeBins"].mean().round()
            self.imputations["AgeBins"] = age_class_imputations
        # median imputation   
        elif self.age_fitter == "median":
            self.imputations["AgeBins"] = X_age["AgeBins"].median()
        elif self.age_fitter == "median+":
            age_class_imputations = X_age.groupby(["Pclass", "Status"])["AgeBins"].median()
            self.imputations["AgeBins"] = age_class_imputations
        # regression imputation
        elif self.age_fitter == "simpleregressor":
            rfr_imputation_age = RandomForestRegressor(n_estimators=100, max_depth=3, random_state=42)
            rfr_imputation_age.fit(X_age[["Pclass", "Status", "FamilySize"]], X_age["AgeBins"].values)
            self.imputations["AgeBins"] = rfr_imputation_age 

        self.fitted = True
        return None

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if not self.fitted:
            raise BaseException("No fitted data")
            return None
        X_transform = X.copy()
        
        # 1: Decode Categorical Features
        cat_features = ["Pclass", "Sex", "Cabin", "Embarked"]
        
        # "Sex"
        X_transform["Sex"] = self.encoders["Sex"].transform(X_transform["Sex"])

        # "Embarked"
        X_transform["Embarked"] = self.encoders["Embarked"].transform(X_transform["Embarked"])

        # "Cabin"
        X_transform["Cabin"] = X["Cabin"].fillna("Unknown").apply(lambda row: row[0])
        X_transform["Cabin"] = X_transform["Cabin"].replace({"T": "R", "G": "R"})
        X_transform["Cabin"] = self.encoders["Cabin"].transform(X_transform["Cabin"])

        # 2: "Name"
        X_transform["Status"] = X_transform["Name"].str.extract(r"([A-Za-z]+)\.")
        X_transform["Status"] = X_transform["Status"].replace(self.imputations["Name"])
        X_transform["Status"] = self.encoders["Status"].transform(X_transform["Status"])

        # 3: "FamilySize"
        X_transform["FamilySize"] = X_transform["SibSp"] + X_transform["Parch"]
        
        # 4: "Fare"
        if self.farebins:
            X_transform["Fare"] = X_transform["Fare"].fillna(X_transform["Fare"].mean())
            X_transform["FareBins"] = pd.cut(X_transform["Fare"], self.imputations["Fare"])
            X_transform["FareBins"] = self.encoders["FareBins"].transform(X_transform["FareBins"])
            X_transform = X_transform.drop(columns = ["Fare"])

        # 5: "Age"
        X_transform["AgeBins"] = pd.Series()
        X_transform.loc[X_transform["Age"].notna(), "AgeBins"] = pd.cut(X_transform.loc[X_transform["Age"].notna(), "Age"], self.imputations["Age"])
        X_transform.loc[X_transform["Age"].notna(), "AgeBins"] = self.encoders["AgeBins"].transform(X_transform.loc[X_transform["Age"].notna(), "AgeBins"])
        # mean imputation
        if self.age_fitter == "mean":
            X_transform["AgeBins"] = X_transform["AgeBins"].fillna(self.imputations["AgeBins"])
        elif self.age_fitter == "mean+":
            X_transform.loc[X_transform["Age"].isna(), "AgeBins"] = X_transform.loc[X_transform["Age"].isna(),["Pclass", "Status"]].merge(self.imputations["AgeBins"], on=["Pclass", "Status"], how="left")["AgeBins"].fillna(3).values
        # median imputation   
        elif self.age_fitter == "median":
            X_transform["AgeBins"] = X_transform["AgeBins"].fillna(self.imputations["AgeBins"])
        elif self.age_fitter == "median+":
            X_transform.loc[X_transform["Age"].isna(), "AgeBins"] = X_transform.loc[X_transform["Age"].isna(),["Pclass", "Status"]].merge(self.imputations["AgeBins"], on=["Pclass", "Status"], how="left")["AgeBins"].fillna(3).values
        # regression imputation
        elif self.age_fitter == "simpleregressor":
            X_transform.loc[X_transform["Age"].isna(), "AgeBins"] = self.imputations["AgeBins"].predict(X_transform.loc[X_transform["Age"].isna(), ["Pclass", "Status", "FamilySize"]]).round()

        X_transform = X_transform.drop(columns = ["Ticket", "Name", "Age"])
        return X_transform
