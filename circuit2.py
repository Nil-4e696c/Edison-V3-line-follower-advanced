#-------------Setup----------------
import Ed
Ed.EdisonVersion = Ed.V3
Ed.DistanceUnits = Ed.CM
Ed.Tempo = Ed.TEMPO_FAST

#--------Your code below-----------

# Variables de calibration
white_threshold = 0
black_threshold = 0
calibrated = False

def calibrateLineTracker():
    """
    Calibre le capteur de ligne en démarrant sur du blanc.
    Tout ce qui est plus sombre sera considéré comme noir.
    """
    global white_threshold, black_threshold, calibrated
    
    # Active le capteur
    Ed.LineTrackerLed(Ed.ON)
    
    # Signal de début de calibration
    Ed.LeftLed(Ed.ON)
    Ed.RightLed(Ed.ON)
    Ed.PlayBeep()
    Ed.TimeWait(500, Ed.TIME_MILLISECONDS)
    Ed.LeftLed(Ed.OFF)
    Ed.RightLed(Ed.OFF)
    
    # Prend plusieurs mesures sur le blanc pour avoir une valeur stable
    total_readings = 0
    num_readings = 10
    
    for i in range(num_readings):
        total_readings = total_readings + Ed.ReadLineTracker()
        Ed.TimeWait(100, Ed.TIME_MILLISECONDS)
        # Clignote pour indiquer la calibration en cours
        if i % 2 == 0:
            Ed.LeftLed(Ed.ON)
        else:
            Ed.LeftLed(Ed.OFF)
    
    # Calcule la moyenne des lectures sur le blanc
    white_threshold = total_readings // num_readings
    
    # Définit le seuil noir comme 70% de la valeur blanche
    # (ajustable selon les conditions d'éclairage)
    black_threshold = (white_threshold * 7) // 10
    
    # Signal de fin de calibration
    Ed.LeftLed(Ed.OFF)
    Ed.RightLed(Ed.OFF)
    for i in range(3):
        Ed.PlayBeep()
        Ed.LeftLed(Ed.ON)
        Ed.RightLed(Ed.ON)
        Ed.TimeWait(200, Ed.TIME_MILLISECONDS)
        Ed.LeftLed(Ed.OFF)
        Ed.RightLed(Ed.OFF)
        Ed.TimeWait(200, Ed.TIME_MILLISECONDS)
    
    calibrated = True

def isOnBlackLine():
    """
    Retourne True si le robot est sur une ligne noire
    """
    if not calibrated:
        return False
    
    current_reading = Ed.ReadLineTracker()
    return current_reading < black_threshold

# Configuration des LEDs et capteurs
Ed.ObstacleDetectionBeam(Ed.ON)

# Variables pour la gestion des obstacles
obstacle_pause_duration = 3000  # 3 sec de pause quand obstacle détecté
cooldown_duration = 5000  # 5 sec avant de pouvoir re-détecter un obstacle
cooldown_timer_ms = 5000  # Timer pour le cooldown (démarre à 5000 pour permettre détection immédiate)
wait_step = 4  # pause entre chaque tour de boucle

def waitClap():
    # Loop around, waiting for a clap to be detected
    while Ed.ReadClapSensor() != Ed.CLAP_DETECTED:
        pass

def followLine():
    """
    Suit la ligne en utilisant la calibration personnalisée
    INVERSÉ : gauche et droite échangés
    """
    if isOnBlackLine():
        Ed.Drive(Ed.FORWARD_RIGHT, Ed.SPEED_7, 1)  # INVERSÉ : était FORWARD_LEFT
    else:
        Ed.Drive(Ed.FORWARD_LEFT, Ed.SPEED_7, 1)   # INVERSÉ : était FORWARD_RIGHT

def handleObstacle():
    """
    Gère la détection d'obstacle : s'arrête, pause 3 sec + bip, puis repart
    """
    global cooldown_timer_ms
    
    Ed.Drive(Ed.STOP, 0, 0)  # Arrêt immédiat
    Ed.LeftLed(Ed.ON)
    Ed.RightLed(Ed.ON)
    Ed.PlayBeep()  # Bip d'alerte immédiat
    Ed.TimeWait(obstacle_pause_duration, Ed.TIME_MILLISECONDS)  # Pause 3 secondes
    Ed.PlayBeep()  # Bip de redémarrage
    Ed.LeftLed(Ed.OFF)
    Ed.RightLed(Ed.OFF)
    
    # Démarre le cooldown de 5 secondes
    cooldown_timer_ms = 0
    # Le robot va automatiquement reprendre le suivi de ligne

# === SÉQUENCE DE DÉMARRAGE ===

# 1. Calibration automatique du capteur de ligne
# Placez le robot sur une surface BLANCHE et attendez...
Ed.TimeWait(3, Ed.TIME_SECONDS)  # Laisse le temps de positionner le robot
calibrateLineTracker()

# 2. Signal de fin de calibration avec bip différent
Ed.PlayBeep()
Ed.TimeWait(300, Ed.TIME_MILLISECONDS)
Ed.PlayBeep()

# 3. Attente du départ par clap
# Calibration terminée ! Tapez dans vos mains pour démarrer...
waitClap()

# Signal de démarrage
Ed.LeftLed(Ed.ON)
Ed.RightLed(Ed.ON)
Ed.PlayBeep()
Ed.TimeWait(500, Ed.TIME_MILLISECONDS)
Ed.LeftLed(Ed.OFF)
Ed.RightLed(Ed.OFF)

# === BOUCLE PRINCIPALE ===
# Démarrage du suivi de ligne avec évitement d'obstacles !

while True:
    # Vérifie s'il y a un obstacle ET si le cooldown est écoulé
    if cooldown_timer_ms >= cooldown_duration:
        if Ed.ReadObstacleDetection() != Ed.OBSTACLE_NONE:
            handleObstacle()
            # Après la pause, le cooldown de 5 sec commence
        else:
            # Pas d'obstacle, suit la ligne normalement
            followLine()
    else:
        # En période de cooldown, suit la ligne sans détecter d'obstacles
        followLine()
        cooldown_timer_ms += wait_step  # Incrémente le timer de cooldown
    
    Ed.TimeWait(wait_step, Ed.TIME_MILLISECONDS)