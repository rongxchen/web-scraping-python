import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from typing import List
from machine_learning.enum.missing_data_strategy import MissingDataStrategy
from machine_learning.model.base import MLBase
from sklearn.linear_model import LinearRegression as SkLinearRegression


class LinearRegression(MLBase):
    
    def __init__(self, data: pd.DataFrame, 
                 target_variable: str, 
                 numeric_strategy: MissingDataStrategy = MissingDataStrategy.FILL_MEAN,
                 character_strategy: MissingDataStrategy = MissingDataStrategy.DROP,
                 train_size = 0.8):
        super().__init__(data, target_variable, numeric_strategy, character_strategy, train_size)


    def train(self, columns: List[str] = None):
        self.model = SkLinearRegression()
        if columns is not None:
            self.independent_columns = columns
        self.model.fit(X=self.train_data[self.independent_columns], y=self.train_data[self.target_variable])


    def predict(self, data: List[dict] = None):
        if data is None:
            data = self.test_data
        data = pd.DataFrame(data)
        self.last_predict_res = self.model.predict(data[self.independent_columns])
        return self.last_predict_res


    def plot(self):
        if self.last_predict_res is None:
            raise Exception("Please train the model and make a prediction before plotting")
        df = self.data
        row_count, total_columns, curr_column_count = 1, 2, 1
        for i, var in enumerate(self.independent_columns):
            x = df[var].values
            y = df[self.target_variable].values
            slope = self.model.coef_[i]
            intercept = self.model.intercept_
            line = slope * x + intercept
            plt.subplot(row_count, total_columns, curr_column_count)
            plt.scatter(x, y)
            plt.plot(x, line, color="red")
            plt.title(f"{var} vs {self.target_variable}")
            if curr_column_count == total_columns:
                curr_column_count = 1
                row_count += 1
            else:
                curr_column_count += 1
        plt.tight_layout()
        plt.show()
