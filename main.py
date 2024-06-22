import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from utils import aggiungi_transazione, valida_data, print_saluto, report_mensile, top_10_transazioni


def main():
    '''
    Funzione principale del programma per la gestione delle transazioni.
    Crea un menu di opzioni per aggiungere transazioni, generare report mensili e visualizzare le top 10 transazioni per importo.
    '''
    file_csv = 'transazioni.csv'
    
    while True:
        print("\nMenu delle operazioni:")
        print("[1] Aggiungi una transazione")
        print("[2] Visualizza i Report mensili")
        print("[3] Visualizza le Top 10 transazioni per importo")
        print("Digita 'quit' se vuoi uscire dal programma")
        
        scelta = input("Seleziona un'opzione: ")
        
        if scelta == '1':
            aggiungi_transazione(file_csv)
        elif scelta == '2':
            report_mensile(file_csv)
        elif scelta == '3':
            top_10_transazioni(file_csv)
        elif scelta == 'quit':
            print_saluto()
            break
        else:
            print("Opzione non valida. Seleziona 1, 2, 3 o quit")



if __name__ == "__main__":
    main()