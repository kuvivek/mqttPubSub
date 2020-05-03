import paho.mqtt.client as mqtt
import time

#Taking the variables for the method.
client = mqtt.Client() # here we are getting the instance of the Client class
topicName = "vivek/azeti/test"
QOS_val = 2
 
client.username_pw_set(username="vivek", password="Saanvi@13")

#====================Defining call backs ===================
def on_connect(pvtClient, userdata, flags, rc): 
  if (rc == 0): # on successful connection
    print("Connected to the client! Return code:" + str(rc)) # Printing the data on the screen
    # Once connection is established, then only subscribe to the topic, also the Qos value is important for the subscriber without fail.
    # QOS value is of least important for Publisher. It should be least in Publisher, meaning fire and forget for value 0
    # 1 meaning atleast once it should be done, Similarly for highly secure it should be 2, as it involves 3 way handshake.
    result = client.subscribe(topicName, QOS_val) # Getting the tuple from the callback.
    
  elif(rc == 5): # In case of authentication error
    print("Authentication Error! Return Code: " + str(rc)) # printing the data on the screen.
    client.disconnect()

#================Callback for the callback message==========
# This call back will run whenever there is a message(payload) published on the given topic.
def on_message(pvtClient, userdata, msg):
  # Extracting the details from the message parameter.
  print("\n============================")
  print("Payload             :" + str(msg.payload.decode()))
  print("Qos of the message  :" + str(msg.qos))
  print("Message Topic       :" + str(msg.topic))
  print("Message Retain      :" + str(msg.retain))
  if (msg.payload.decode() == "exit(0)"):
    client.disconnect()
'''
# Currently not using this callback
def will_set(pvtClient, payload="disconnected!!!", qos=2, retain=False):
  print("status: " + payload)
  
'''

# this call back is used for the log generation
def on_log(topic, userdata, level, buf): 
  print("Logs: " + str(buf))             
  

#======== Associating the methods with the given callbacks of the MQTT ========
client.on_connect    = on_connect
client.on_message    = on_message
client.on_log        = on_log
#client.will_set     = will_set

host      = "localhost"
port      = 1883
keepAlive = 60

client.connect(host, port, keepAlive) # Establishing the connection

time.sleep(2)   # giving a sleep time for the connection to setup

client.loop_forever()
