# Meraki Dashboard API

Access  to your Cisco Meraki cloud-managed in a pythonic way.  Also available via PIP

## Prerequisites
You need to enable APIs in your Meraki dashboard and obtain an APIKey:  [Instructions](https://documentation.meraki.com/zGeneral_Administration/Other_Topics/The_Cisco_Meraki_Dashboard_API) 

## Example

```python
from meraki_dashboard_api import Dashboard

apikey = "jkhsfsdhk32424******example*****jlasdfsdfl3245345"

dash = Dashboard(apikey)

# list all organizations
myOrgs = dash.organizations.list()
print(myOrgs)

# list all organization's networks
myNets = dash.organizations.networks(<orgId>)
print(myNets)

```


Since the other options available are complex or old school, my need was a more pythonic and object oriented way.

The 90% of que API belong to the **/networks** endpoint and from there appears some groups, in the Meraki documentation these groups are represented as isolated, but  most of them belong to the same parent endpoint.

The [oficial](https://github.com/meraki/dashboard-api-python) implementation is a simple functional programming (old school) and the [guzmonne](https://github.com/guzmonne/meraki_api) implementation is, I think, a really complex approach returning instances inside another instances.

Ex:
```python
response = meraki.organizations().index()
json = response.json()
```

Instead I use some magic methods to instantiate the classes following a strict URL pattern.

Ex:
```python
client = dash.networks.clients.get(<networkId>, <clientId>)
print(client)
```

I use args to build the URL path and kwargs to pass query parameters each endpoint .

Ex:
```python
dev = dash.networks.devices.loss_and_latency(<networkId>, <serial>, uplink=‘wan1’, ip=‘1.2.3.4’, timespan=7200)
print(dev)
```

For POST and PUT methods you can use a kwargs data or update.

Ex.
```python
payload = {
	'name': 'My AP',
	'tags': 'recently-added ',
	'lat': 37.4180951010362,
	'lng': -122.098531723022,
	'address': 'some place',
	'notes': 'no notes',
	'moveMapMarker': True
}
dev = dash.networks.devices.update(<networkId>, <serial>, update=payload)
print(dev)
```
