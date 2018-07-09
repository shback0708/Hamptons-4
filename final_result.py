import csv

def returnFinal(self):
    final = [["Game_ID", "Player_ID", "Player_Plus/Minus"]]
    for game in self.games:
        for players in self.games[game].playersAppeared:
            final += [[str(game),str(players),str(players.rpm)]]
    return final; 


with open("Hamptons_4_Q1_BBALL.csv", "w", newLine = "") as fp:
    a = csv.writer(fp, delimiter = ',')
    data = returnFinal(Data)
    a.writerows(data)



