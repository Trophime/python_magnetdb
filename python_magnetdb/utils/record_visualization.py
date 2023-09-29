columns = {
    'Date': "date d'acquisition",
    'Time': "heure d'acquisition",
    'Field': 'T',
    'Tin1': "°C",
    'Tin2': "°C",
    'Tout': '°C',
    'TAlimout': '°C',
    'HP1': "bar",
    'HP2': "bar",
    'BP': 'bar',
    'Flow1': 'l/s',
    'Flow2': 'l/s',
    'Rpm1': 'rpm',
    'Rpm2': 'rpm',
    'Idcct1': 'A',
    'Idcct2': 'A',
    'Idcct3': 'A',
    'Idcct4': 'A',
    'Pmagnet': "MW",
    'Ptot': 'MW',
    'teb': "°C",
    'tsb': "°C",
    'debitbrut': 'm^3/h',
    'Q': 'MVars',
    't': 's',
    'timestamp': 'date complète'
}

for i in range(16):
    columns[f'Icoil{i + 1}'] = 'A'
    columns[f'Ucoil{i + 1}'] = 'V'
    columns[f'DRcoil{i + 1}'] = '%'
    columns[f'Tcal{i + 1}'] = '°C'
