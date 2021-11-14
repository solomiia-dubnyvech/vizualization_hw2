import numpy as np
import pandas as pd


def load_data():
    fields = ['date_time', 'AES', 'TEC', 'VDE', 'TES', 'GES', 'GAES_GEN', 'CONSUMPTION']
    data = pd.read_csv('./data_lab2.csv').loc[:, fields]
    return _divide_date_time(data)


def _divide_date_time(df: pd.DataFrame):
    def _get_time(x):
        return int(x.split('-')[0])

    def _get_date(x):
        return x.split('-')[1]

    def _get_day(x):
        return int(_get_date(x).split('.')[0])

    def _get_month(x):
        return int(_get_date(x).split('.')[1])

    def _get_year(x):
        return int(_get_date(x).split('.')[2])

    df['hour'] = df.date_time.apply(_get_time)
    df['date'] = df.date_time.apply(_get_date)
    df['day'] = df.date_time.apply(_get_day)
    df['month'] = df.date_time.apply(_get_month)
    df['year'] = df.date_time.apply(_get_year)

    return df


def get_sum_grouped_by_day_of_year():
    df = load_data().groupby(['year', 'month', 'day']).sum().reset_index()  # total consumption for each day
    df = df.groupby(['month', 'day']).mean().reset_index()                  # mean consumption for day of month
    df['month_day'] = df['month'].astype(str) + '.' + df['day'].astype(str)
    return df.sort_values(['month', 'day'])


def get_melted_sum_grouped_by_year():
    df = load_data()
    df = df.drop(['hour', 'date', 'day', 'month', 'date_time', 'CONSUMPTION'], axis=1)
    return df.melt('year', var_name='origin', value_name='energy').groupby(['year', 'origin']).sum().reset_index()


def get_melted_mean_grouped_by_hour():
    df = load_data()
    df = df.drop(['year', 'date', 'day', 'month', 'date_time', 'CONSUMPTION'], axis=1)
    return df.melt('hour', var_name='origin', value_name='energy').groupby(['hour', 'origin']).mean().reset_index()


def get_mean_grouped_by_month_and_hour():
    return load_data().groupby(['month', 'hour']).mean().reset_index()


def get_mean_grouped_by_season_and_hour():
    def _get_season(month):
        season_num = month // 3
        seasons = ['Winter', 'Spring', 'Summer', 'Autumn', 'Winter']
        return seasons[season_num]

    df = get_mean_grouped_by_month_and_hour()
    df['season'] = df.month.apply(_get_season)
    return df.groupby(['season', 'hour']).mean().reset_index()


def get_mean_grouped_by_hour():
    return load_data().groupby('hour').mean().reset_index()


def get_mean_grouped_by_weekday():
    def _get_week_day(day_num):
        # 01.01.2014 is Wednesday
        week_days = ['Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue']
        return week_days[day_num % 7]

    df = load_data().groupby(['year', 'month', 'day']).sum().reset_index()
    df['row_num'] = np.arange(len(df))
    df['weekday'] = df.row_num.apply(_get_week_day)
    return df.groupby('weekday').mean().reset_index()


if __name__ == '__main__':
    print(get_mean_grouped_by_weekday())
