#import time

# Seconds between sensor readings
#PASSENGER_INTERVAL = 1
#QUEUE_INTERVAL = 1
#GATE_INTERVAL = 1
#TEMPERATURE_INTERVAL = 1
#EMERGENCY_INTERVAL = 2

# Number of messages each sensor generates
#TOTAL_READINGS = 10


#new ......new.....
# BROKER = "localhost"
# PORT = 1883

# PASSENGER_TOPIC = "airport/passenger"
# QUEUE_TOPIC = "airport/queue"
# GATE_TOPIC = "airport/gate"
# TEMPERATURE_TOPIC = "airport/temperature"
# EMERGENCY_TOPIC = "airport/emergency"

# PASSENGER_INTERVAL = 2
# QUEUE_INTERVAL = 3
# GATE_INTERVAL = 4
# TEMPERATURE_INTERVAL = 5
# EMERGENCY_INTERVAL = 8

#new ......new.....
BROKER = "localhost"
PORT = 1883

RAW_PASSENGER_TOPIC = "airport/raw/passenger"
RAW_QUEUE_TOPIC = "airport/raw/queue"
RAW_GATE_TOPIC = "airport/raw/gate"
RAW_TEMPERATURE_TOPIC = "airport/raw/temperature"
RAW_EMERGENCY_TOPIC = "airport/raw/emergency"

EDGE_PASSENGER_TOPIC = "airport/edge/passenger"
EDGE_QUEUE_TOPIC = "airport/edge/queue"
EDGE_GATE_TOPIC = "airport/edge/gate"
EDGE_TEMPERATURE_TOPIC = "airport/edge/temperature"
EDGE_EMERGENCY_TOPIC = "airport/edge/emergency"

FOG_PASSENGER_TOPIC = "airport/fog/passenger"
FOG_QUEUE_TOPIC = "airport/fog/queue"
FOG_GATE_TOPIC = "airport/fog/gate"
FOG_TEMPERATURE_TOPIC = "airport/fog/temperature"
FOG_EMERGENCY_TOPIC = "airport/fog/emergency"

PASSENGER_INTERVAL = 2
QUEUE_INTERVAL = 2
GATE_INTERVAL = 2
TEMPERATURE_INTERVAL = 2
EMERGENCY_INTERVAL = 5