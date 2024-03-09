from Functions.air_distance import haversine
import pandas as pd
import matplotlib.pyplot as plt
from numpy import ndarray
import numpy as np

# Latitude and Longtitude from center point (Yerevan Center)
YEREVAN_CENTER_LAT, YEREVAN_CENTER_LONG = 40.18111, 44.51361


class DataAnalyse:

    def __init__(self, center_lat: float, center_long: float):
        self.df = pd.read_csv(r'C:\Users\Mikayel\PycharmProjects\AnalysProject\Data\CombinedData.csv', encoding='utf-8', low_memory=False)
        self.__making_distance_column(center_lat, center_long)
        self.df.rename(columns={'childer': 'children'}, inplace=True)
        self.df.dropna(subset=['floorcount','roomcount','bathroomcount'], inplace=True)
        self.df['floorcount'] = self.df['floorcount'].astype(int)
        self.df['roomcount'] = self.df['roomcount'].astype(int)
        self.df['bathroomcount'] = self.df['bathroomcount'].astype(int)

    def __making_distance_column(self, center_lat: float, center_long: float) -> None:
        '''
        Making distance_from_center column in df
        :param center_lat: center latitude
        :param center_long: center longtitdue
        :return: None
        '''
        self.df['distance_from_center'] = self.df.apply(
            lambda row: haversine(center_lat, center_long, row['latitude'], row['longtitude']), axis=1)

    def distance_price_dependence_plot(self, filt: ndarray, min_km: float = 0, max_km: float = 250, min_price: int = 0,
                                       max_price: int = 1000000):
        '''
        Price dependence from distance
        :param filt: = (analyze.df['category_from_list'] == 'commercial-estate-offices-rent')
        :param min_km: minimum distance from center
        :param max_km: maximum distance from center
        :param min_price: minimum price
        :param max_price: maximum price
        :return: returns plot
        '''
        x = self.df.loc[filt, 'distance_from_center']
        y = self.df.loc[filt, 'price']
        plt.plot(x, y, 'o')
        plt.title('Price change depending on distance')
        plt.xlabel('Distance')
        plt.ylabel('Price')
        plt.xlim(min_km, max_km)
        plt.ylim(min_price, max_price)
        plt.show()

    def data_mean_by_distance(self, filt: ndarray, distance_from_center: float, plus_minus_km: float):
        new_filt = (filt) & (self.df['distance_from_center'] >= distance_from_center - plus_minus_km) & (
                self.df['distance_from_center'] <= distance_from_center + plus_minus_km)
        return self.df[new_filt]['price'].mean()

    def data_median_by_distance(self, filt: ndarray, distance_from_center: float, plus_minus_km: float):
        new_filt = (filt) & (self.df['distance_from_center'] >= distance_from_center - plus_minus_km) & (
                self.df['distance_from_center'] <= distance_from_center + plus_minus_km)
        return self.df[new_filt]['price'].median()

    def find_outliers(self, filt: ndarray, plot=True):
        '''
        Find outlaiers depending on price

        :param filt: filter of data
        :param plot: plotin if plot=True
        :return: series that is outlaiers
        '''
        filtered_df = self.df[filt]

        q1 = filtered_df['price'].quantile(0.25)
        q3 = filtered_df['price'].quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = filtered_df[(filtered_df['price'] < lower_bound) | (filtered_df['price'] > upper_bound)]
        if plot:
            colors = {'medians': 'Black', 'caps': 'Red'}
            filtered_df['price'].plot.box(color=colors)
            plt.title('Box Plot of Price')
            plt.ylabel('Price')
            plt.ylim(filtered_df['price'].min() * 0.9, filtered_df['price'].mean() * 4)
            plt.show()

        return outliers

    def remove_outliers(self, filt: ndarray):
        '''
        Remove outliers depending on price

        :param filt: filter of data
        :return: DataFrame without outliers
        '''
        filtered_df = self.df[filt]

        q1 = filtered_df['price'].quantile(0.25)
        q3 = filtered_df['price'].quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        filtered_df = filtered_df[(filtered_df['price'] >= lower_bound) & (filtered_df['price'] <= upper_bound)]

        return filtered_df

    def price_per_square_meter(self, filt: ndarray) -> float:
        '''
        Price of square meter of item
        :param filt: filter for data
        :return: float, price for each meter
        '''
        filtered_df = self.df[filt]

        if filtered_df['landarea'].notna().any() and filtered_df['area'].notna().any():
            price_per_sqm = filtered_df['price'] / (filtered_df['area'] + filtered_df['landarea'])
        elif filtered_df['landarea'].isna().all() and filtered_df['area'].notna().any():
            price_per_sqm = filtered_df['price'] / (filtered_df['area'])
        else:
            price_per_sqm = filtered_df['price'] / (filtered_df['landarea'])

        return np.median(price_per_sqm)


if __name__ == "__main__":
    analyze = DataAnalyse(YEREVAN_CENTER_LAT, YEREVAN_CENTER_LONG)

    filt = (analyze.df['category_from_list'] == 'apartments-sale')
    # print(analyze.df[filt]['floorcount'].isna().sum())
    # print(analyze.df[filt]['roomcount'].isna().sum())
    # print(analyze.df[filt]['bathroomcount'].isna().sum())
    analyze.find_outliers(filt)
