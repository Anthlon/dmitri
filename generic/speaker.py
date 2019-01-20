
LANG = {
    'EN': {
        'single': ('year', 'month', 'day'),
        'middle': ('years', 'months', 'days'),
        'many': ('years', 'months', 'days'),
    },
    'RU': {
        'single': ('год', 'месяц', 'день'),
        'middle': ('года', 'месяца', 'дня'),
        'many': ('лет', 'месяцев', 'дней'),
    }
}


def smm(value, lang, index):
    if value > 4:
        word = 'many'
    elif 1 < value < 5:
        word = 'middle'
    else:
        word = 'single'
    return lang[word][index]


def cogwheel(boolean, divider, language, index, delta):
    if boolean:
        val = int(delta/divider)
        delta = delta - val*divider
        if val:
            return str(val) + ' ' + smm(val, language, index), delta
    return '', delta


def delta_date_printer(start, end, lang='EN', years=True, months=True, days=True, st_year=365, st_month=29):

    """


    :param start: date obj.
    :param end: date obj.
    :param lang: language that is used, only 'RU' or 'EN'.
    :param years: Using years in str return?
    :param months: Using months in str return?
    :param days: Using days in str return?
    :param st_year: standard year = 365 days.
    :param st_month: standard month = 29 days.
    :return str delta like '1 year, 7 months' or '2 years' or '1 month'.
    """

    language = LANG[lang]
    delta = (end - start).days
    booleans = [years, months, days]
    divider = [st_year, st_month, 1]
    index = [i for i in range(3)]
    container = []
    while index and delta:
        string, delta = cogwheel(booleans.pop(0), divider.pop(0), language, index.pop(0), delta)
        if len(string):
            if len(container):
                container.append(', ')
            container.append(string)

    return ''.join(container)



