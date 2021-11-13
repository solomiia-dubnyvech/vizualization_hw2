from source import *
from params import *
import altair as alt


def task1():
    agg_data = get_melted_sum_grouped_by_year()
    line = alt.Chart(agg_data).mark_bar().encode(
        x=alt.X('origin:O'),
        y=alt.Y('energy:Q'),
        color='origin:N',
        column='year:N',
    )

    return add_title(
        chart=line,
        title='Зміна структури генерації електроенергії за роками',
    )


def task2_1():
    agg_data = get_sum_grouped_by_day_of_year()
    dates = agg_data['month_day'].tolist()
    line = alt.Chart(agg_data, height=500, width=1100).mark_line().encode(
        x=alt.X('month_day:O', sort=dates, axis=alt.Axis(values=[f'{x}.1' for x in range(1, 13)], labelAngle=0)),
        y=alt.Y('CONSUMPTION:Q', scale=get_scale(320000, 520000)),
    )

    desc = alt.Chart(agg_data).mark_text(
        text='Вісь Х подана у форматі Місяць.День',
        dy=240,
        dx=450,
        color='gray',
    )

    return add_title(
        chart=line + desc,
        title='Залежність споживання електроенергії від дня року',
    )


def task2_2():
    data = load_data()
    agg_data = get_mean_grouped_by_hour()
    line = alt.Chart(agg_data, width=1100, height=500).mark_line(color='green').encode(
        x=alt.X('hour:O', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('CONSUMPTION:Q', scale=get_scale(14000, 20000)),
    )

    band = alt.Chart(data, width=900, height=500).mark_errorband(extent='ci', color='green').encode(
        x='hour:O',
        y=alt.Y('CONSUMPTION:Q', scale=get_scale(14000, 20000)),
    )

    return add_title(
        chart=line + band,
        title='Залежність споживання електроенергії від години доби',
    )


def task3():
    agg_data = get_melted_mean_grouped_by_hour()
    line = alt.Chart(agg_data, height=500, width=1100).mark_line().encode(
        x=alt.X('hour:O', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('energy:Q'),
        color='origin:N',
    )

    return add_title(
        chart=line,
        title='Зміна генерації електроенергії з різних джерел впродовж доби',
    )


def task4_1():
    agg_data = get_mean_grouped_by_month_and_hour()
    selection = alt.selection_multi(fields=['month'], bind='legend')
    line = alt.Chart(agg_data, height=500, width=1100).mark_line().encode(
        x=alt.X('hour:O', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('CONSUMPTION:Q', scale=get_scale(12000, 24000)),
        color='month:N',
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).add_selection(selection)

    return add_title(
        chart=line,
        title='Зміна споживання електроенергії впродовж доби у розрізі місяців року',
    )


def task4_2():
    agg_data = get_mean_grouped_by_season_and_hour()
    selection = alt.selection_multi(fields=['season'], bind='legend')
    line = alt.Chart(agg_data, height=500, width=1100).mark_line().encode(
        x=alt.X('hour:O', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('CONSUMPTION:Q', scale=get_scale(12000, 24000)),
        color='season:N',
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).add_selection(selection)

    return add_title(
        chart=line,
        title='Зміна споживання електроенергії впродовж доби у розрізі пір року',
    )


def task5():
    agg_data = get_mean_grouped_by_weekday()
    line = alt.Chart(agg_data, height=500, width=750).mark_bar(color='lightcoral').encode(
        x=alt.X('weekday:O', axis=alt.Axis(labelAngle=0), sort=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
        y=alt.Y('CONSUMPTION:Q', scale=get_scale(370000, 420000)),
    )

    return add_title(
        chart=line,
        title='Зміна споживання електроенергії впродовж тижня',
    )


if __name__ == '__main__':
    alt.data_transformers.disable_max_rows()
    task5().show()
