import random
import math

# Funzione che si occupa della creazione del magazzino, 
# inizializzando ciascuna componente con un valore variabile in base alla 
# capienza massima in magazzino per tale componente.
def creaMagazzino():
    return {
        "Mandorla": random.randint(0, 500),
        "Zucchero": random.randint(0, 2000),
        "Sciroppo di glucosio": random.randint(0, 100),
        "Miele": random.randint(0, 50)
    }

# Funzione che si occupa della creazione del lotto commissionato 
# all'azienda, assegnando a ciascun prodotto un numero di unità variabile in 
# base alla quantità che l'azienda si prende in carico per ciascuno di essi.
def creaLotto():
    return {
        "Mandorla pelata": random.randint(0, 500),
        "Latte di mandorla": random.randint(0, 250),
        "Torrone": random.randint(0, 70)
    }

# Funzione che restituisce il tempo necessario al riapprovvigionamento
# nel caso in cui una componente in magazzino venga esaurita.
def riapprovvigionamento(magazzino):
    tempoDiRiapprovvigionamento = 0 # Variabile utilizzata per tener conto del tempo di riapprovvigionamento

   # Dizionario contenete i tempi di approvvigionamento relativi a ciascuna componente
    approvvigionamenti = {
        "Mandorla": 2,   
        "Zucchero": 1,   
        "Sciroppo di glucosio": 1, 
        "Miele": 1
    }

    # Dizionario contente la capacità massima in magazzino relativa a ciascuna componente
    capacitaMax = {
        "Mandorla": 500,
        "Zucchero": 2000,
        "Sciroppo di glucosio": 100,
        "Miele": 50
    }
    
    for componente in magazzino.keys(): # Itera le componenti presenti in magazzino
        if magazzino[componente] < 0:   # Verifica la presenza in magazzino per componente
            tempoDiRiapprovvigionamento = approvvigionamenti[componente] # Se la componente è esaurita viene restituito il tempo necessario al 
            magazzino[componente] = capacitaMax[componente]              # riapprovvigionamento e le scorte in magazzino vengono ripristinate.
                                                                         
    
    return tempoDiRiapprovvigionamento

# Funzione che nel caso in cui si verifichi un guasto restituisce il tempo necessario alla sua risoluzione
def gestioneGuasti(prodotto):

    # Dizionario contenente le probabiltà di guasto relative al ciclo produttivo di ciascun prodotto  
    probabilitaGuasto = {
        "Mandorla pelata": 0.05, 
        "Latte di mandorla": 0.10,  
        "Torrone": 0.15   
    }

    if random.random() < probabilitaGuasto[prodotto]:        # Nel caso in cui si verifica un guasto viene calcolato il tempo
        tempoDiRisoluzione = random.randint(1, 3) * 8 * 60   # necessario alla sua risoluzione, il quale varia tra 1 e 3 giorni lavorativi.
        return tempoDiRisoluzione
    
    return 0

# Funzione che restituisce il tempo necessario alla produzione del lotto 
def produzioneLotto(magazzino, lotto):
    
    # Dizionario contenente la quantità di componente necessaria alla realizzazione
    # di ciascun prodotto
    usoComponente = {
        "Mandorla pelata": {"Mandorla": 0.5},
        "Latte di mandorla": {"Mandorla": 0.4, "Zucchero": 0.35, "Sciroppo di glucosio": 0.25},
        "Torrone": {"Mandorla": 2.0, "Zucchero": 0.75, "Miele": 0.25}
    }
    
    # Dizionario contenente i tempi di produzione relativi alla realizzazione di un unità di prodotto
    tempoDiProduzionePerUnita = {"Mandorla pelata": 5, "Latte di mandorla": 20, "Torrone": 25}

    tempoDiProduzioneTotale = 0 # Variabile utilizzata per tener traccia del tempo di produzione totale
    
    for prodotto, quantita in lotto.items(): # Itera il lotto da produrre 
        for componente, qntComponentePerUnita in usoComponente[prodotto].items(): # Itera le componenti per prodotto
            qntComponenteRichiestaLotto = qntComponentePerUnita * quantita # Calcola la quantità di componente necessaria alla realizzazione del prodotto in esame
            magazzino[componente] -= qntComponenteRichiestaLotto  # Sottrae tale quantità alle scorte in magazzino
            if magazzino[componente] < 0:                                               # Nel caso in cui le scorte si esauriscono viene invocata la funzione riapprovvigionamento(magazzino) e
                tempoDiProduzioneTotale += riapprovvigionamento(magazzino) * 8 * 60     # il tempo restituito viene convertito in minuti e sommato alla variabile tempoDiProduzioneTotale
            
        tempoDiProduzioneTotale += quantita * tempoDiProduzionePerUnita[prodotto]  # Alla variabile tempoDiProduzioneTotale viene sommato il tempo necessario alla produzione del prodotto in esame
        tempoDiProduzioneTotale += gestioneGuasti(prodotto)                        # e l'eventuale tempo necessario alla risoluzione del guasto
                        
                            

    giorniLavorativi = math.ceil(tempoDiProduzioneTotale / (8 * 60)) # Il tempo calcolato viene trasformato in giorni e arrotondato per eccesso
    return giorniLavorativi



def main():
    
    # Viene creato il magazzino
    magazzino = creaMagazzino() 

    # Viene creato e stampato il lotto di ordinazione
    lotto = creaLotto() 
    print("\n=== LOTTO DA PRODURRE ===")
    for product, quantita in lotto.items():
        print(f"{product}: {quantita} unità")
    
    # Vengono calcolati i giorni lavorativi necessari alla realizzazione del lotto e stampati
    giorniLavorativi = produzioneLotto(magazzino, lotto)
    print("\n=== RISULTATI DELLA SIMULAZIONE ===")
    print(f"Tempo totale di produzione: {giorniLavorativi} giorni lavorativi")
    
if __name__ == "__main__":
    main()
