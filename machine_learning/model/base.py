import pandas as pd
import copy
from abc import abstractmethod
from machine_learning.enum.missing_data_strategy import MissingDataStrategy
from util import pd_util


class MLBase:

    def __init__(self, data: pd.DataFrame, 
                 target_variable: str, 
                 numeric_strategy: MissingDataStrategy = MissingDataStrategy.FILL_MEAN,
                 character_strategy: MissingDataStrategy = MissingDataStrategy.DROP,
                 train_size: float = 0.8):
        self.data = copy.deepcopy(data)
        self.target_variable = target_variable
        self.numeric_strategy = numeric_strategy
        self.character_strategy = character_strategy
        self.train_size = train_size
        self.independent_columns = [column for column in self.data.columns if column != self.target_variable]
        self.prepare_for_train()
        
        
    def __handle_missing_data(self):
        numeric_columns, character_columns = [], []
        for column in self.data.columns:
            is_numeric = pd_util.is_numeric(self.data[column])
            if is_numeric:
                numeric_columns.append(column)
            else:
                character_columns.append(column)
        # handle character columns
        if self.character_strategy == MissingDataStrategy.DROP:
            self.data.dropna(subset=character_columns, inplace=True)
        # handle numeric columns
        if self.numeric_strategy == MissingDataStrategy.DROP:
            self.data.dropna(subset=numeric_columns, inplace=True)
        else:
            value = {}
            for column in numeric_columns:
                num = 0
                if self.numeric_strategy == MissingDataStrategy.FILL_MEAN:
                    num = self.data[column].mean()
                elif self.numeric_strategy == MissingDataStrategy.FILL_MEDIAN:
                    num = self.data[column].median()
                elif self.numeric_strategy == MissingDataStrategy.FILL_MODE:
                    num = self.data[column].mode()[0]
                value[column] = num
            self.data.fillna(value=value, inplace=True)


    def prepare_for_train(self):
        self.__handle_missing_data()
        train_length = int(len(self.data)*self.train_size)
        self.train_data = self.data[:train_length]
        self.test_data = self.data[train_length:]

    
    @abstractmethod
    def evaluate(self):
        pass
        
    
    @abstractmethod
    def train(self):
        pass


    @abstractmethod
    def predict(self):
        pass
    