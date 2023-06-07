import j2l.pytactx.agent as pytactx
import copy
# <<< DECLARATION DES VARIABLES >>>

agent = pytactx.AgentFr(nom="Alexandre",
                        arene="numsup2223",
                        username="demo",
                        password=input("🔑 password: "),
                        url="mqtt.jusdeliens.com",
                        verbosite=3)

agentVoisinsVieux = {
}  # Dico des joueurs dans l'état avant la dernière actualisation.

agentState = "onLookout"  # Etat de base de la machine à état globale.

shootoutState = 0 # Etat de base de la machine à état du shootout. 0 = en train de se déplacer dans l'axe de l'ennemi; 1 = en train de tirer sur cet ennemi

rondeEtat = 0 # L'état de la ronde pour le mode Recherche: 0, 1, 2 ou 3 selon l'étape de la ronde.

voisinIdeal = "" # La cible à abattre actuelle.

# <<< DEFINITION DES FONCTIONS >>>


def eval(agent, voisin):
  """
  Evalue le coût d'un ennemi. Un coût élevé correspond à un ennemi difficile à abattre.
  :param agent: Notre agent.
  :type agent: dict
  :param voisin: L'agent voisin à calculer.
  :type voisin: dict
  :return: Le coût de l'agent voisin.
  :rtype: float
  """

  # On calcule le poids lié à la distance en comparant notre agent et le voisin.
  poidsDistx = abs(agent["x"] - voisin["x"]) / 10
  poidsDisty = abs(agent["y"] - voisin["y"]) / 10 # Pourquoi 10? Car le champ de vision est de 10. La normalisation est ainsi garantie.
  poidsDist = (poidsDistx + poidsDisty) / 2

  # On calcule le poids lié à la vie d'un ennemi.
  # Si la vie d'un ennemi est supérieure à 100, on lui donne le coût maximum.
  vie = voisin["life"]
  if vie <= 100:
    poidsVie = vie / 100
  else:
    poidsVie = 1

  # On calcule le poids lié à la réserve de munition d'un ennemi.
  # Si la réserve de munition d'un ennemi est supérieure à 100, on lui donne le coût maximum.
  munitions = voisin["ammo"]
  if munitions <= 100:
    poidsMunition = munitions / 100
  else:
    poidsMunition = 1

  # Comme il y a 3 paramètres, on fait la moyenne de ces paramètres en en faisant la somme divisée par 3.
  poidsTotal = (poidsDist + poidsVie + poidsMunition) / 3

  return poidsTotal

def testEval():
  """
  fonction test de eval
  """
  ficAgent1 = {"x": 10, "y": 10, "ammo": 50, "life": 50}
  ficAgent2 = {"x": 12, "y": 12, "ammo": 70, "life": 70}
  testing = eval(ficAgent1, ficAgent2)

  # Mauvaises utilisations
  assert isinstance(testing, float), "Function should return a float"
  assert testing <= 1, "Function should return a float LOWER THAN 1"

  # Bonne utilisation
  assert testing == 1.6 / 3, "Function returns" + testing + " instead of the correct result"

def rechercheMin(dico):
  """
  Recherche la clé d'un dictionnaire dont la valeur est la plus petite.
  :param dico: Dictionnaire dont les valeurs sont soit des float, soit des int.
  :type dico: dict
  :return: Tuple contenant en 0 la clé ayant la valeur minimale, et en 1 le montant de cette valeur.
  """
  minAgent = ("noAgent", 1)
  for agent, cout in dico.items():
    if minAgent[1] > cout:
      minAgent = (agent, cout)

  return minAgent

def testRechercheMin():
  assert rechercheMin({
    "agent1": 0.9,
    "agent2": 0.2
  }) == ("agent2", 0.2), "Error: incorrect result. Expected" + (
    "agent2", 0.2) + "lowest cost agent with his cost."

def evalPossibilites(lagent, voisins):
  """
  Consulte le dictionnaire de l'intégralité des voisins et détermine, pour chaque voisin, son coût pour aller l'abattre.
  :param lagent: Votre agent.
  :type lagent: dict
  :param voisins: Dictionnaire des agents voisins de votre agent.
  :type voisins: dict
  :return: Le dictionnaire des voisins avec leurs coûts. Si pas de voisins, renvoie False.
  :rtype: dict
  """

  # On initialise les variables: possibilites sera le cout minimum, et voisinIdeal sera le nom du voisin avec le cout minimum.
  possibilites = {
  }  # Normalement, le coût ne peut pas dépasser 1, mais on met 10 juste au cas où.

  for voisin, attributs in voisins.items():  # Pour chaque voisin...
    actualCout = eval(lagent, attributs)  # On calcule le cout du voisin.
    # print("Coût pour ", voisin, ": ", actualCout)  # Outil de calcul du cout en temps réel
    possibilites[
      voisin] = actualCout  # Crée, dans le dictionnaire de retour, une entrée avec comme clé le nom du voisin et comme valeur son coût

  # Si il n'y a pas de voisins, retourne false, sinon retourne le dictionnaire des voisins avec leurs coûts.
  return possibilites

def testPossibilites():
  """
  fonction test de eval
  """
  ficAgent = {"x": 10, "y": 10, "ammo": 50, "life": 50}
  ficAgent1 = {"x": 12, "y": 12, "ammo": 70, "life": 70}
  ficAgent2 = {"x": 14, "y": 14, "ammo": 75, "life": 75}
  dicoFicAgents = {"Bob": ficAgent1, "John": ficAgent2}
  coutFicAgents = {"Bob": 0.5333333333333333, "John": 0.6333333333333333}

  #Mauvaises utilisations
  assert isinstance(evalPossibilites(ficAgent, dicoFicAgents),
                    dict), "Function should return a dict"

  #Bonne utilisation
  # assert evalPossibilites(
  #   ficAgent, {}) == False, "Function does not return False when no neighbours"
  assert evalPossibilites(
    ficAgent, dicoFicAgents
  ) == coutFicAgents, "Function does not return a dict with the cost of each agent"

def agentDetecter():
  """
  Dès qu'un nouvel agent apparaît dans le champ de vision, cette fonction affiche le nom du nouveau venu ainsi que ses points de vie.
  """
  global agentVoisinsVieux

  nomsAgentsDetecte = []
  hpAgentDetecte = 0

  for cle, valeur in agent.voisins.items():
    if cle not in agentVoisinsVieux:  # Si le joueur n'est pas dans l'ancien dico...
      nomsAgentsDetecte.append(cle)  # C'est qu'il vient d'apparaître.
      for valeur in nomsAgentsDetecte:
        for cles, valeurs in agent.voisins.items():
          if (valeur in cles):
            if ("life" in valeurs):
              hpAgentDetecte = agent.voisins[valeur]["life"]
        print("Agent detected:", nomsAgentsDetecte, "with ", hpAgentDetecte,
              " HP.")

def agentDissiper():
  """
  Dès qu'un agent disparaît du champ de vision, cette fonction affiche le nom du joueur parti ainsi que ses points de vie.
  """
  global agentVoisinsVieux

  nomsAgentsDetecte = []
  hpAgentDetecte = 0

  for cle, valeur in agentVoisinsVieux.items():
    if cle not in agent.voisins:
      nomsAgentsDetecte.append(cle)
      for valeur in nomsAgentsDetecte:
        for cles, valeurs in agentVoisinsVieux.items():
          if (valeur in cles):
            if ("life" in valeurs):
              hpAgentDetecte = agentVoisinsVieux[valeur]["life"]
        print("Agent vanished:", nomsAgentsDetecte, "with ", hpAgentDetecte,
              " HP.")

def agentDecisionAttaque():
  """
  Si il n'y a pas de voisins ou que les voisins sont trop dangereux, ne fait rien. Sinon, si il est assez faible, passe à l'état 'OnPursuit'. Et si il est moyennement dangereux, passe à l'état OnShootout.
  """
  global agentState
  global voisinIdeal

  agentInfo = {"x": agent.x, "y": agent.y}  # On formate les donnees de position de notre agent.
  voisinIdeal = rechercheMin(evalPossibilites(
  agentInfo,
  agent.voisins))[0]  # Détermine (avec rechercheMin()) le voisin avec le moindre coût (calculé grâce à possibilites()).
  voisinIdealCout = rechercheMin(evalPossibilites(
  agentInfo,
  agent.voisins))[1]  # Détermine (avec rechercheMin()) le coût de ce voisin (calculé grâce à possibilites()).
  if voisinIdeal == "noAgent":
    pass
  elif voisinIdealCout <= 0.45:
    agentState = "onPursuit" # L'agent est suffisament faible et proche pour mourir dans un combat au corps-à-corps.
  elif voisinIdealCout <= 0.85:
    print(voisinIdeal + "SniperTime")
    agentState = "onShootout" # L'agent est tuable en prenant les précautions nécessaires: rester loin et lui tirer dessus.
  else:
    print(voisinIdeal + " is too strong!")

def agentRonde():
  """
  Fonction de la machine à état Ronde, permettant à l'agent de faire sa ronde avec des points fixes.
  """
  global rondeEtat
  
  match rondeEtat:
    # La ronde peut avoir 4 états, correspondants aux 4 coins du rectangle de la ronde.
    
      case 0:
          rondeNordOuest()
  
      case 1:
          rondeSudOuest()
  
      case 2:
          rondeSudEst()
  
      case 3:
          rondeNordEst()
  
def rondeNordOuest():
  """
  Fonction de la ronde lorsque l'agent se dirige vers le nord-oues. Passe à l'étape suivante lorsque le point est atteint.
  """
  global rondeEtat
  if agent.x == 5 and agent.y == 5: # Si la destination est atteinte...
    rondeEtat = 1 # ...alors on passe à la prochaine destination
  else:
    agent.deplacerVers(5, 5) # On se dirige vers la destination de l'état actuel

def rondeSudOuest():
  """
  Fonction de la ronde lorsque l'agent se dirige vers le nsud-ouest. Passe à l'étape suivante lorsque le point est atteint.
  """
  global rondeEtat
  if agent.x == 5 and agent.y == 20: # Si la destination est atteinte... 
    rondeEtat = 2 # ...alors on passe à la prochaine destination 
  else:
    agent.deplacerVers(5, 20) # On se dirige vers la destination de l'état actuel

def rondeSudEst():
  """
  Fonction de la ronde lorsque l'agent se dirige vers le sud-est. Passe à l'étape suivante lorsque le point est atteint.
  """
  global rondeEtat
  if agent.x == 20 and agent.y == 20: # Si la destination est atteinte...
    rondeEtat = 3 # ...alors on passe à la prochaine destination
  else:
    agent.deplacerVers(20, 20) # On se dirige vers la destination de l'état actuel

def rondeNordEst():
  """
  Fonction de la ronde lorsque l'agent se dirige vers le nord-est. Passe à l'étape suivante lorsque le point est atteint.
  """
  global rondeEtat
  if agent.x == 20 and agent.y == 5: # Si la destination est atteinte...
    rondeEtat = 0 # ...alors on passe à la prochaine destination
  else:
    agent.deplacerVers(20, 5) # On se dirige vers la destination de l'état actuel

def shootoutPositionner():
  """
  Se déplace sur le même axe que l'agent à abattre (X ou Y selon lequel est plus proche). 
  Lorsqu'il est sur le même axe que l'ennemi, il passe à l'état 1 de Shootout.
  """
  global shootoutState

  agent.tirer(False) # Il ne tire pas dans cet état.
  x = agent.voisins[voisinIdeal]["x"]
  y = agent.voisins[voisinIdeal]["y"] # On récupère la position de l'ennemi.
  if agent.x == x or agent.y == y:
    shootoutState = 1 # Si on est dans l'axe x ou y de l'ennemi, on passe à un autre état.
  elif abs(agent.x - x) < abs(agent.y - y):
    agent.deplacerVers(x, agent.y)
  elif abs(agent.x - x) >= abs(agent.y - y):
    agent.deplacerVers(agent.x, y) # Se déplace vers l'axe x ou y de l'ennemi selon lequel est plus proche.

def shootoutTirerSorienter():
  """
  Fonction qui permet, lors de l'état 1 de Shootout, de s'orienter vers l'ennemi à tuer.
  En même temps, s'éloigne de cet ennemi.
  """

  x = agent.voisins[voisinIdeal]["x"]
  y = agent.voisins[voisinIdeal]["y"] # On récupère la position de l'ennemi.
  agentDead()

  if x == agent.x:
    if y < agent.y:
      agent.orienter(1)
      agent.deplacer(0, 1)
    else:
      agent.orienter(3)
      agent.deplacer(0, -1)
  elif y == agent.y:
    if x < agent.x:
      agent.orienter(2)
      agent.deplacer(1, 0)
    else:
      agent.orienter(0)
      agent.deplacer(-1, 0)
  else:
    pass
  
def shootoutTirer():
  """
  Fonction qui permet de tirer sur la cible à abattre jusqu'à qu'elle ne soit plus dans la ligne de mire.
  """
  
  global shootoutState

  x = agent.voisins[voisinIdeal]["x"]
  y = agent.voisins[voisinIdeal]["y"]
  agentDead()
  
  if not(agent.x == x or agent.y == y):
    shootoutState = 0
  else:
    shootoutTirerSorienter()
    agent.tirer(True)
  
def agentOnShootout():
  """
  L'état correspondant à tirer sur la cible, qui ne s'arrète que lorsque l'on meurt ou si l'ennemi quitte le champ de vision.
  """

  global voisinIdeal
  global agentState
  global shootoutState
  
  print(voisinIdeal + "TireDessus")
  agent.changerCouleur(255, 255, 0)

  agentDead()
  if voisinIdeal not in agent.voisins:
    agentState = "onLookout"
  elif shootoutState == 0:
    shootoutPositionner()
  elif shootoutState == 1:
    shootoutTirer()

def agentOnPursuit():
  """
  La fonction correspondant à l'état poursuite. Dans cet état, l'agent se déplace vers le voisin idéal sélectionné en amont jusqu'à ce qu'il disparaisse du dictionnaire agent voisins. Ensuite, il repasse en mode recherche.
  """

  global voisinIdeal
  global agentState

  agent.changerCouleur(255, 0, 0) # Dans cet état, l'agent est rouge.
  
  if voisinIdeal not in agent.voisins:
    agentState = "onLookout" # On repasse en mode recherche 
  else:
    print(voisinIdeal + "CasseLaGueule")
    x = agent.voisins[voisinIdeal]["x"]
    y = agent.voisins[voisinIdeal]["y"]
    agent.deplacerVers(x, y)  # Se déplace vers la position du voisin idéal.
    agentDead()

def agentDead():
  """
  Permet de faire en sorte que lorsque l'agent meurt, tous les scripts s'arrêtent et lorsqu'il respawn, il repasse en mode onLookout.
  """
  global agentState

  # Si l'agent n'a plus de point de vie, il passe à l'état "mort", arrête de tirer et en informe la console.
  if agentState != "dead":
    if agent.vie == 0:
      agentState = "dead"
      agent.tirer(False)
      print("YOU ARE DEAD, DEAD, DEAD.")

  # Si l'agent est dans l'état "mort" mais qu'il est vivant (AKA quand il respawne), il en informe la console et repasse en état recherche. 
  elif agent.vie != 0:
    agentState = "onLookout"
    print("YOU ARE ALIVE.")

def agentOnLookout():
  """
  Effectue les actions liées à l'état "recherche" de l'agent (détecte les agents qui viennent et qui partent, tourne sur lui-même, fait une ronde, et décide si il veut ou non attaquer.)
  """
  agent.tirer(False) # Lorsqu'il recherche, il ne tire pas.
  
  agent.changerCouleur(0, 0, 255) # Lorsqu'il recherche, il est bleu foncé.
  
  agent.orienter((agent.orientation + 1) % 4) # Il tourne sur lui-même.
  
  agentRonde() # Il fait sa ronde.
  
  agentDetecter() # Lorsqu'il recherche, les agents détectés sont annoncés à la console.
  agentDissiper() # Lorsqu'il recherche, les agents disparus sont annoncés à la console.
  
  agentDecisionAttaque() # Fonction permettant à l'agent de changer d'état si un ennemi tuable est repéré.
  agentDead() # Si il meurt, il change d'état.


# <<< EXEC >>>

# Tests
testEval()
testPossibilites()
testRechercheMin()

# The main boucle.
while True:
  agent.actualiser()

  if agentState == "onLookout":
    agentOnLookout()

  elif agentState == "onPursuit":
    agentOnPursuit()

  elif agentState == "onShootout":
    agentOnShootout()

  elif agentState == "dead":
    agentDead()

  # print(agent.voisins)
  agentVoisinsVieux = copy.deepcopy(agent.voisins)
