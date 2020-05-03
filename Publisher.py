import paho.mqtt.client as mqtt
import time

client = mqtt.Client() # here we are getting the instance of the Client class

exitFlag = True # This is taken for the authentication purpose

client.username_pw_set(username="vivek", password="Saanvi@13")

#====================Call Backs ===================
def on_publish(client, userdata, mid): # call back for the published data
  print("Payload Published: " + str(mid)) # printing the message id of the published message

def on_connect(pvtClient, userdata, flags, rc): # call back for the connection acknowlegement
  global exitFlag # Setting an exitFlag based on connection status, used later 
  if (rc == 0):
    print("publisher Connected") # printing the data
    print("Connected to the client! Return code " + str(rc))
    exitFlag = False

  elif(rc == 5):
    print("Authentication Error! Return Code: " + str(rc))
    client.disconnect()
    exitFlag = True

# Using this call back for the log generation
def on_log(client, userdata, level, buf): # call backs for the logs,
  print("Logs: " + str(buf))              # printing the logs on the screen, this will show the logs
  
def on_disconnect(pvtClient, userdata, rc):
  print("disconnecting reason " + str(rc))
  client.disconnect()


#======== Associating the functions with the call ==========

client.on_publish    = on_publish
client.on_connect    = on_connect
client.on_log        = on_log
client.on_disconnect = on_disconnect

print("Starting the loop")

#==== Establishing Connection ===========
host      = "localhost"
port      = 1883
keepAlive = 60

client.connect(host, port, keepAlive)
# starting the loop
# Using this loop and sleep in between client.connect(...) and client.publish(...),
# so that we can observer the call backs
client.loop_start()  # starting a loop in order to observe the call backs
time.sleep(2)        # giving a sleep time for the connecttion to setup

#=========================================================
# once connected, publish the message
#=============Publishing the message =====================

topic_name = "vivek/azeti/test"

QOS  = 0
retain  = True


# print("Flag status: " + str(exitFlag))
while(exitFlag == False):
  time.sleep(.5)
  payload = raw_input("\nMessage: ")
  # publishing the message payload.
  client.publish(topic_name, payload, QOS, retain)
  # in case user has enetered  "exit(0)" then exit and disconnect
  if(payload == "exit(0)"):
    client.disconnect()

'''
Using the QOS we can set the Quality of Service of the given client connection
and the message published for the same.
# ======= Establishing Connection ========
Based on this QOS, the times our client is receiving the message may differ,
Furthermore, we may confirm the acknowledgements involved between

Publisher --- broker --- subscriber, are more

For a given MQTT setup we can set this value of either 0,1,2, wherein
different QOS has different properties.

Also, in our case, we can use the functionality of retaining the last known
message in case of the given client (subscriber) is not present, or unable
to receive the message (payload). Hence, setting the value of retain parameter
as True or 1 will make sure that in case of undeleivered message, the given 
message is retained.
'''

#=======================
# If you use the loop_start and loop_forever functions then the loop runs in
# a separate thread, and it is the loop that processes the incoming and
# outgoing messages.

client.loop_stop() # Stopping the time loop
# make sure to use client.loop_stop() function too, id we have used client.loop_start() function

