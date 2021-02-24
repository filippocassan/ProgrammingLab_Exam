#Definisco la classe delle eccezioni
class ExamException(Exception):
    pass

#Definisco la classe CSVTimeSeriesFile
class CSVTimeSeriesFile():

    #Istanzio la classe sul nome del file tramite la variabile 'name'
    def __init__(self, name):
        self.name = name

    #Definisco il metodo 'get_data()', che deve tornare una lista di liste che abbia come primo elemento l'epoch e come secondo elemento la temperatura
    def get_data(self):

        #Definisco una lista che immagazzina i time_series di tutto il file
        Lista = []

        #Provo ad aprire il file
        try:
            time_series_file = open(self.name, 'r')
        #Se non esiste o non è leggibile, alzo un'eccezione
        except:
            raise ExamException('Il file specificato non esiste o non è leggibile')

        #Leggo il file linea per linea con l'utilizzo di un ciclo for
        for line in time_series_file:

            #Separo ("splitto") ogni linea del file sulla virgola, in modo da ottenere due elementi (quello prima della virgola e quello dopo la virgola) e li associo ad una nuova lista chiamata appunto 'elements'
            try:
                elements = line.split(',')
            except:
                continue
            
            #Controllo di non stare processando l'intestazione del file
            if elements[0] != 'epoch':

                #In tal caso associo a due diverse variabili l'elemento prima della virgola (gli epoch) e l'elemento dopo la virgola (le temperature). Provo inoltre a convertire gli epoch ad interi per arrotondamento e le temperature a floating point
                try:
                    epoch = round(float(elements[0]))
                except:
                    continue

                try:
                    temperature = float(elements[1])
                except:
                    continue
               
                #Aggiungo alla 'Lista' la lista annidata formata da 'epoch', 'temperature' e altre tre variabili che mi saranno utili successivamente. Lo '0' per salvare gli "epoch orari" (epoch/3600), le due stringhe vuote per poi salvare il trend(se positivo (+) o negativo(-)) e un simbolo che mi indichi la presenza di un'inversione di trend (l'asterisco '*')
                try:
                    Lista.append([epoch, temperature, 0, '', ''])
                except:
                    continue

        #Controllo che la lista 'Lista' sia ordinata utilizzando un ciclo for. Inoltre ne approfitto per 'riempire' le posizioni 2, 3 e 4 della 'Lista' con le corrispettive variabili 
        for i, line in enumerate(Lista):
            
            #Se sono al primo elemento della lista, vado direttamente al prossimo poichè in questo momento non sono in grado di sapere se la lista è o non è ordinata e se è o non è presente un duplicato
            if i == 0:

                #Prima però inserisco in posizione 2 della 'Lista' l' "epoch orario", che ricavo dividendo l'epoch per 3600 e convertendo il risultato ad intero
                Lista[i][2] = int(Lista[i][0] / 3600)

                #A questo punto devo inserire la stringa in posizione 3 della 'Lista', che in questo caso, se la temperatura precedente è minore di quella attuale,
                if Lista[i][1] < Lista[1][1]:
                    #sarà un '+', poichè significa che il trend è in crescita 
                    Lista[i][3] = '+'

                #se la temperatura precedente è maggiore di quella attuale
                elif Lista[i][1] > Lista[1][1]:
                    #inserisco in posizione 3 della 'Lista' un '-', poichè significa che il trend è in calo
                    Lista[i][3] = '-'
                
                continue

            #Non è necessario fare un controllo del tipo 'if i > 0', poichè dopo il 'continue' il programma eseguirebbe ugualmente la parte seguente

            #Anche nel caso degli elementi successivi al primo pongo in posizione numero 2 della 'Lista' l' "epoch orario"
            Lista[i][2] = int(Lista[i][0] / 3600)

            #Ed eseguo i soliti controlli per stabilire che segno deve avere il trend in posizione 3 della 'Lista'
            if Lista[i][1] < Lista[i - 1][1]:
                Lista[i][3] = '-' 
            
            elif Lista[i][1] > Lista[i - 1][1]:
                Lista[i][3] = '+'

            #Aggiungo anche un controllo per sapere cosa fare se la temperatura attuale è uguale a quella precedente
            elif Lista[i][1] == Lista[i - 1][1]:
                #In questo caso il trend non cambia e quindi pongo il trend della temperatura attuale uguale al trend della temperatura precedente
                Lista[i][3] = Lista[i - 1][3]

            #Se poi il trend della temperatura attuale è diverso dal trend della temperatura precedente
            if Lista[i][3] != Lista[i - 1][3]:
                #Significa che c'è stata un'inversione di trend e di conseguenza in posizione 4 della 'Lista' inserisco un asterisco '*', come ho deciso sopra
                Lista[i][4] = '*'

            #Ora passo a fare i controlli per vedere se la lista è ordinata o se nella lista vi è un duplicato

            #Se l'elemento attuale è minore dell'elemento precedente
            if Lista[i][0] < Lista[i - 1][0]:
                #Alzo un'eccezione, poichè significa che la serie temporale non è ordinata
                raise ExamException("La serie temporale contenuta nel file '{}'' non è ordinata".format(self.name))

            #E se invece l'elemento attuale è uguale all'elemento precedente
            elif Lista[i][0] == Lista[i - 1][0]:
                #Alzo un'eccezione, poichè significa che la serie temporale contiene un duplicato
                raise ExamException("Ho trovato un duplicato all'interno della serie temporale contenuta nel file '{}'".format(self.name))

        #Chiudo il file che avevo aperto inizialmente
        time_series_file.close()

        #Il metodo 'get_data()' deve tornare in output la lista di liste ('Lista')
        return Lista

#Definisco la funzione 'hourly_trend_changes' 
def hourly_trend_changes(time_series):

    #Se la funzione non sta operando su una lista
    if not isinstance(time_series, list):
        #Alzo un'eccezione
        raise ExamException('Non è stata inserita una lista')

    #Definisco una lista dove salverò le singole ore (in "epoch orari") e il corrispettivo numero di inversioni di trend di temperatura avvenute in quella precisa ora
    lista_ore_inversioni = []

    #Analizzo tutta la lista 'time_series' utilizzando un ciclo for
    for i, line in enumerate(time_series):

        #Se mi trovo al primo elemento della lista
        if i == 0:

            #Aggiungo subito alla 'lista_ore_inversioni' l' "epoch orario", insieme alla variabile 0, che mi servirà per immagazzinare successivamente il numero di inversioni di trend per quella ora
            lista_ore_inversioni.append([time_series[i][2], 0])

            #Vado agli elementi successivi
            continue

        #Se l' "epoch orario" attuale è diverso dall'ultimo elemento ([-1]) della 'lista_ore_inversioni'
        if time_series[i][2] != lista_ore_inversioni[-1][0]:

            #Scorro tutte le righe e man mano che passano le ore, aggiungo gli "epoch orari" alla 'lista_ore_inversioni'
            lista_ore_inversioni.append([time_series[i][2], 0])

            #Testo con un print() che la 'lista_ore_inversioni' si sia formata correttamente
            #print(lista_ore_inversioni[-1])

    #Analizzo nuovamente tutta la 'time_series'
    for i, line in enumerate(time_series):
        
        #E se trovo un'inversione di trend (ovvero scopro che in posizione 4 della lista c'è un asterisco '*')
        if time_series[i][4] == '*':

            #Analizzo tutta la 'lista_ore_inversioni'
            for j, line in enumerate(lista_ore_inversioni):

                #Se l' "epoch orario" della 'lista_ore_inversioni' è uguale all' "epoch orario" della lista 'time_series' in cui ho trovato l'asterisco
                if lista_ore_inversioni[j][0] == time_series[i][2]:

                    #Aumento il contatore delle inversioni di trend, posto in posizione 1 nella 'lista_ore_inversioni', di 1
                    lista_ore_inversioni[j][1] += 1

                    continue

    #Definisco la lista 'lista_inversioni', in cui salverò le inversioni di trend di temperatura per ogni ora presente nel dataset
    lista_inversioni = []

    #Analizzo tutta la 'lista_ore_inversioni'
    for i, line in enumerate(lista_ore_inversioni):
        #per prenderne ogni elemento in posizione 1 (ovvero il numero di inversioni di trend) e aggiungerlo alla 'lista_inversioni'
        lista_inversioni.append(lista_ore_inversioni[i][1])

    #La funzione 'hourly_tren_changes(time_series)' deve poi ritornare in output la lista contenente le inversioni di trend di temperatura(in questo caso 'lista_inversioni')
    return lista_inversioni



#CORPO DEL PROGRAMMA

time_series_file = CSVTimeSeriesFile(name = 'data.csv')
time_series = time_series_file.get_data()

#Test
#print('\nFile: {}\n'.format(time_series_file.name))
#print('Dati del file sottoforma di lista di liste di 5 elementi(epoch, temperatura, "epoch orario", trend, inversione):\n {}\n'.format(time_series))

lista_inversioni = hourly_trend_changes(time_series)

print('Lista di inversioni di trend di temperatura per ogni ora presente nel dataset:\n {}\n'.format(lista_inversioni))

print('In totale ci sono state {} inversioni'.format(sum(lista_inversioni)))