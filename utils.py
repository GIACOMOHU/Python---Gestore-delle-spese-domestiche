# Importiamo le librerie, i moduli e le classi necessarie

import os
from datetime import datetime
from collections import defaultdict
import csv





# Definiamo le funzioni necessarie

def aggiungi_transazione(file_csv):
    '''
    Aggiunge una transazione a un file CSV.
    
    L'utente deve inserire una data, una descrizione e un importo separati da spazi.
    Ad esempio: "18/05/2024 Cena al ristorante 45"
    '''
    while True:
        # Richiede l'input della transazione
        input_transazione = input("Inserisci la data della transazione, la descrizione e l'importo (es. 18/05/2024 Cena al ristorante 45) oppure digita 'quit' per tornare al menù principale: ")
        if input_transazione.lower() == 'quit':
            return 'quit'
        
        try:
            # Trova l'ultimo spazio nell'input per separare descrizione e importo
            last_space_index = input_transazione.rfind(' ')
            if last_space_index == -1:
                raise ValueError("Errore: formato input non valido. Assicurati di inserire data, descrizione e importo separati da spazi (es. 18/05/2024 Cena al ristorante 45).")
            
            importo = input_transazione[last_space_index+1:].strip()
            data_descrizione = input_transazione[:last_space_index].strip()

            # Trova il primo spazio nella prima parte per separare la data e la descrizione
            first_space_index = data_descrizione.find(' ')
            if first_space_index == -1:
                raise ValueError("Errore: formato input non valido. Assicurati di inserire data, descrizione e importo separati da spazi (es. 18/05/2024 Cena al ristorante 45).")

            data = data_descrizione[:first_space_index].strip()
            descrizione = data_descrizione[first_space_index+1:].strip()
                
        except ValueError as e:
            print(str(e))
            continue

        # Verifica e converte la data
        if not valida_data(data):
            continue

        # Verifica e converte l'importo
        try:
            importo = float(importo)
        except ValueError:
            print("Errore: importo non valido. Inserisci un numero valido.")
            continue

        # Scrive la transazione nel file CSV
        with open(file_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([data, descrizione, importo])
        print("Transazione aggiunta con successo!")

        # Chiede all'utente se vuole aggiungere un'altra transazione
        risposta = input("Vuoi aggiungere un'altra transazione? (1: Sì ; 4: No, torna al menù principale): ")
        if risposta == '1':
            continue
        elif risposta == '4':
            return 'quit'
        else:
            print("Opzione non valida.")
            return 'quit'



def valida_data(data_str):
    '''
    Verifica se una data è valida e ben formattata nel formato GG/MM/AAAA.
    Controlla anche che la data non sia futura.
    '''
    try:
        # Dividi la stringa della data in giorno, mese e anno
        parts = data_str.split('/')
        if len(parts) != 3:
            raise ValueError("Errore: data incompleta o non ben formattata. Assicurati di inserire data, mese e anno nel formato GG/MM/AAAA.")
        
        giorno, mese, anno = parts
        if len(anno) != 4:
            raise ValueError("Errore: anno incompleto. Assicurati di inserire l'anno nel formato AAAA.")
        
        giorno, mese, anno = int(giorno), int(mese), int(anno)

        # Controlla se il mese è valido (tra 1 e 12)
        if mese < 1 or mese > 12:
            raise ValueError("Errore: mese non valido. Inserisci un mese compreso tra 1 e 12.")

        # Controlla se il giorno è valido per il mese e l'anno specificato
        giorni_del_mese = {
            1: 31, 2: 29 if anno % 4 == 0 and (anno % 100 != 0 or anno % 400 == 0) else 28,
            3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31,
            9: 30, 10: 31, 11: 30, 12: 31
        }

        if giorno < 1 or giorno > giorni_del_mese[mese]:
            raise ValueError(f"Errore: il mese {mese} ha massimo {giorni_del_mese[mese]} giorni.")

        # Verifica la validità della data completa
        data = datetime.strptime(data_str, "%d/%m/%Y")

        # Controlla se la data è futura
        if data > datetime.now():
            raise ValueError("Errore: la data inserita è nel futuro. Inserisci una data valida.")

        return True
    except ValueError as e:
        print(e)
        return False



def print_saluto():
    '''
    Stampa un saluto in base all'ora corrente:
    - Buona giornata! se è prima di mezzogiorno
    - Buon proseguimento di giornata! se è tra mezzogiorno e le 15:00
    - Buona serata! se è dopo le 15:00
    '''
    # Ottieni l'ora corrente
    ora_corrente = datetime.now().hour
    
    # Determina il saluto appropriato in base all'ora corrente
    if ora_corrente < 12:
        print("Buona giornata!")
    elif 12 <= ora_corrente < 15:
        print("Buon proseguimento di giornata!")
    else:
        print("Buona serata!")



def report_mensile(file_csv):
    '''
    Genera un report mensile delle transazioni da un file CSV.
    Accumula e stampa gli importi per anno e mese.
    '''
    transazioni = defaultdict(float)
    
    # Verifica l'esistenza del file CSV e lo legge
    if os.path.exists(file_csv):
        with open(file_csv, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Estrae data, descrizione e importo dalla riga del CSV
                data, descrizione, importo = row
                # Converte la data nel formato "YYYY-MM"
                anno_mese = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m")
                # Accumula l'importo per il corrispondente anno e mese
                transazioni[anno_mese] += float(importo)
    
    # Stampa il report mensile ordinato per anno e mese
    for anno_mese, importo_totale in sorted(transazioni.items()):
        print(f"{anno_mese} {importo_totale:.2f}")
    
    # Messaggio se non ci sono transazioni
    if not transazioni:
        print("Non ci sono transazioni registrate.")



def top_10_transazioni(file_csv):
    '''
    Genera un report delle top 10 transazioni per importo da un file CSV.
    Le transazioni sono ordinate in ordine decrescente per importo.
    '''
    transazioni = []
    
    # Verifica l'esistenza del file CSV e lo legge
    if os.path.exists(file_csv):
        with open(file_csv, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Estrae data, descrizione e importo dalla riga del CSV
                data, descrizione, importo = row
                # Aggiunge la transazione alla lista
                transazioni.append((data, descrizione, float(importo)))
    
    # Ordina le transazioni per importo in ordine decrescente e seleziona le prime 10
    transazioni.sort(key=lambda x: x[2], reverse=True)
    top_10 = transazioni[:10]
    
    # Stampa le top 10 transazioni
    for data, descrizione, importo in top_10:
        print(f"{data} {descrizione} {importo:.2f}")
    
    # Messaggio se non ci sono transazioni
    if not transazioni:
        print("Non ci sono transazioni registrate.")