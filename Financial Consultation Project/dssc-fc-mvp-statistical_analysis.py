# This python file calculates the statistical attributes of the stock symbols in question
import pandas as pd
import numpy as np
import os
import statistics


class StatisticalAnalysis:

    def __int__(self):
        self.temp_data = []
        self.temp_data_frame = []
        self.statistical_data = pd.DataFrame()
        self.statistical_data['Company'] = []
        self.statistical_data['Open_Max'] = []
        self.statistical_data['Open_Min'] = []
        self.statistical_data['Open_Range'] = []
        self.statistical_data['Open_Median'] = []
        self.statistical_data['Open_Mean'] = []
        self.statistical_data['Open_Variance'] = []
        self.statistical_data['Open_STD'] = []
        self.statistical_data['High_Max'] = []
        self.statistical_data['High_Min'] = []
        self.statistical_data['High_Range'] = []
        self.statistical_data['High_Median'] = []
        self.statistical_data['High_Mean'] = []
        self.statistical_data['High_Variance'] = []
        self.statistical_data['High_STD'] = []
        self.statistical_data['Low_Max'] = []
        self.statistical_data['Low_Min'] = []
        self.statistical_data['Low_Range'] = []
        self.statistical_data['Low_Median'] = []
        self.statistical_data['Low_Mean'] = []
        self.statistical_data['Low_Variance'] = []
        self.statistical_data['Low_STD'] = []
        self.statistical_data['Close_Max'] = []
        self.statistical_data['Close_Min'] = []
        self.statistical_data['Close_Range'] = []
        self.statistical_data['Close_Median'] = []
        self.statistical_data['Close_Mean'] = []
        self.statistical_data['Close_Variance'] = []
        self.statistical_data['Close_STD'] = []
        self.statistical_data['Adj_Close_Max'] = []
        self.statistical_data['Adj_Close_Min'] = []
        self.statistical_data['Adj_Close_Range'] = []
        self.statistical_data['Adj_Close_Median'] = []
        self.statistical_data['Adj_Close_Mean'] = []
        self.statistical_data['Adj_Close_Variance'] = []
        self.statistical_data['Adj_Close_STD'] = []
        self.statistical_data['Volume_Max'] = []
        self.statistical_data['Volume_Min'] = []
        self.statistical_data['Volume_Range'] = []
        self.statistical_data['Volume_Median'] = []
        self.statistical_data['Volume_Mean'] = []
        self.statistical_data['Volume_Variance'] = []
        self.statistical_data['Volume_STD'] = []

    # This method takes in data frame of every company and calculates the various statistical information on them
    # Finally this return a data frame that consists of the statical information of every company
    @staticmethod
    def initialize_data_frame(self, dataframe):
        self.temp_data = []
        self.temp_data_frame = pd.read_csv(f'{dataframe}')
        splits = dataframe.split('_')
        self.temp_data.append(splits[0])
        for column in self.temp_data_frame.columns:
            if column != 'DateTime':
                self.temp_data.append(self.calculate_min_value(self.temp_data_frame[column]))
                self.temp_data.append(self.calculate_max_value(self.temp_data_frame[column]))
                self.temp_data.append(self.calculate_range_value(self.temp_data_frame[column]))
                self.temp_data.append(self.calculate_median_value(self.temp_data_frame[column]))
                self.temp_data.append(self.calculate_mean_value(self.temp_data_frame[column]))
                self.temp_data.append(self.calculate_variance_value(self.temp_data_frame[column]))
                self.temp_data.append(self.calculate_standard_deviation_value(self.temp_data_frame[column]))

        self.statistical_data.loc[len(self.statistical_data)] = self.temp_data

    @staticmethod
    def calculate_min_value(data_series):
        return data_series.values.min()

    @staticmethod
    def calculate_max_value(data_series):
        return data_series.values.max()

    @staticmethod
    def calculate_range_value(data_series):
        return data_series.values.max() - data_series.values.min()

    @staticmethod
    def calculate_median_value(data_series):
        return statistics.median(data_series.values)

    @staticmethod
    def calculate_mean_value(data_series):
        return statistics.mean(data_series.values)

    @staticmethod
    def calculate_variance_value(data_series):
        return statistics.variance(data_series)

    @staticmethod
    def calculate_standard_deviation_value(data_series):
        return abs(np.std(data_series.values))


# The main start point of the project is this function
# This function goes through every csv file that has been stored in the temp file
def main():
    os.chdir("temp_files\\")
    statistical_report_1 = StatisticalAnalysis()
    statistical_report_1.__int__()

    # List of all the companies for which we have calculated the statistical information
    company_list = {'Alphabet': 'GOOG', 'Apple': 'AAPL', 'BMO': 'BMO.TO', 'Cisco': 'CSCO', 'IBM': 'IBM', 'Meta': 'META',
                    'Microsoft': 'MSFT', 'Nvidia': 'NVDA', 'Oracle': 'ORCL', 'RBC': 'RY.TO', 'Scotia': 'BNS.TO',
                    'TSM': 'TSM',
                    'TXN': 'TXN', 'VZ': 'VZ'}

    for files in os.listdir():
        statistical_report_1.initialize_data_frame(statistical_report_1, files)

    # Create and store the statistical files in the same local temp folder
    statistical_report_1.statistical_data.to_csv('statistic_information.csv', index=False)


# START POINT OF THE PROGRAM
if __name__ == "__main__":
    main()