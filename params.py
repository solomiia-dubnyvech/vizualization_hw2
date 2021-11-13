import altair as alt


def get_scale(domain_min, domain_max):
    return alt.Scale(domain=(domain_min, domain_max), zero=False, nice=False)


def add_title(chart, title):
    return chart.properties(
        title=title,
    ).configure_title(
        fontSize=24,
        font='Courier',
        anchor='start',
        dy=-30
    )
