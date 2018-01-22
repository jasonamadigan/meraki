import sys
import csv
from meraki import meraki

##To do
#1. Sanitize whitespace while reading data in


##DEMO
apikey = ''
orgid = ''
Combined_Store_Template = 'L_646829496481096214'   ##run meraki.gettemplates(apikey,orgid)  to get templateid
Combined_Store_Template_No_Guest ='L_646829496481096214'

##REAL
##Combined_Store_Template = 'L_650207196201621825'   ##run meraki.gettemplates(apikey,orgid)  to get templateid
##Combined_Store_Template_No_Guest ='L_650207196201621826'

document = sys.argv[1]

devices = []
with open(document, 'r') as csv_file:
      csv_reader = csv.DictReader(csv_file)

      for line in csv_reader:
          devices.append(line)
      
##valdiate the CVS contains proper information by displying the list of serials
print("Running...")
print(len(devices), "devices found!!\n----------------------")

for device in devices:
    print(device['serial']," ", device['type'])


##Create a new network

net_name = input('Enter Network Name: ')

print('Adding network', net_name)
new_net = meraki.addnetwork(apikey,orgid,net_name,'appliance wireless switch',None,'America/Phoenix')

#network id of newly added network is returned in addnetwork function in a dictionary under the key 'id'


##Add all the devices to network
for dev in devices:
    meraki.adddevtonet(apikey,new_net['id'], dev['serial'])


##Update attributes
#For each device apply address, move map marker (api has a way to do this)
#APs do not  get named, however address and map marker are updated

for dev in devices:
    #if device is AP, don't update name
    if dev['type'] == '':
        meraki.updatedevice(apikey, networkid = new_net['id'], serial = dev['serial'], address = dev['address'], move='true')
    #Else it's either SW or FW, so go update the name
    else:
        meraki.updatedevice(apikey, networkid = new_net['id'], serial = dev['serial'], address =  dev['address'], move='true', name = dev['type']+'-'+net_name)


##Bind network to template

if devices[0]['template'].strip() == 'Combined-Store-Template':
    template = Combined_Store_Template
    print("Using Combined store")

else:
    template = Combined_Store_Template_No_Guest
    print("Using No Guest")


meraki.bindtotemplate(apikey, networkid=new_net['id'], templateid=template, autobind=True)








