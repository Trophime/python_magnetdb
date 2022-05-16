columns = {
    'Date': "date d'acquisition",
    'Time': "heure d'acquisition",
    'Field': 'Champ magnétique en Tesla',
    'Tin1': "Température d'entrée tranche 1 en °C",
    'Tin2': "Température d'entrée tranche 2 en °C",
    'Tout': 'Température de sortie en °C',
    'TAlimout': 'Température de sortie des convertisseurs de puissance A1, A2, A3, A4 en °C',
    'HP1': "Pression d'entrée tranche 1 en bar",
    'HP2': "Pression d'entrée tranche 2 en bar",
    'BP': 'Pression de sortie en bar',
    'Flow1': 'débit tranche 1 en l/s',
    'Flow2': 'débit tranche 2 en l/s',
    'Rpm1': 'vitesse pompe tranche 1 en tr/min',
    'Rpm2': 'vitesse pompe tranche 2 en tr/min',
    'Idcct1': 'Courant A1 en Ampères',
    'Idcct2': 'Courant A2 en Ampères',
    'Idcct3': 'Courant A3 en Ampères',
    'Idcct4': 'Courant A4 en Ampères',
    'Pmagnet': "Puissance sur l'aimant UxI en MW",
    'Ptot': 'Puissance totale sur installation en MW',
    'teb': "température d'entrée sur l'échangeur, eau Drac en °C",
    'tsb': "température de sortie sur l'échangeur, eau Drac en °C",
    'debitbrut': 'débit eau Drac en m3/h',
    'Q': 'Puissance réactive en MVars',
    't': 'temps depuis le début',
    'timestamp': 'date complète'
}

for i in range(16):
    columns[f'Icoil{i + 1}'] = f'Courant hélice {i + 1} en A'
    columns[f'Ucoil{i + 1}'] = f'Tension hélice {i + 1} en V'
    columns[f'DRcoil{i + 1}'] = 'Ecart entre modèle et mesure en %'
    columns[f'Tcal{i + 1}'] = 'Température calculée/modèle en °C'
