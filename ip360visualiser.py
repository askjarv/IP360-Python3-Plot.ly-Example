# IP360 API Tutorial Example Script
msg = "IP360 API Example"
print(msg)
# Set up our IP360 connection variables (username, password, and the VnE's web interface IP)
USERNAME = "ip360@tripwire.com"
PASSWORD = "YourVnEPasswordHere"
VNEADDRESS = "192.168.0.58"
# Add the modules we need to interact with the API 
import xmlrpclib
import ssl
# Handle invalid SSL certificates by first checking if the SSL certificate is invalid:
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Since legacy Python  doesn't verify HTTPS certificates by default we can simply pass
    pass
else:
    # we can handle target environment that doesn't support HTTPS verification by creating an unverified context to work in,
    ssl._create_default_https_context = _create_unverified_https_context
# Setup server for our connection:
server = xmlrpclib.ServerProxy("https://"+VNEADDRESS+"/api2xmlrpc")
# Setup a session (with corresponding sessionID) for our connection
sessionID = server.login(2,0,USERNAME,PASSWORD)
# Confirm the session by returning some information:
result = server.call(sessionID, "SESSION", "getUserObject",{})
# Print the results
print "My user object is %s" % (result)
# Let's try retrieving some other data, from a different class (VnE this time)
version = server.call(sessionID, "class.VNE", "getVersionInfo",{})
print "VnE version information is %s" % (version)
# OK, let's try get the most recent audit. We'll use the class.Audit with the action fetch. We'll also set some parameters on our request to limit it to the most recent audit only.
audit = server.call(sessionID, "class.Audit", "fetch", {'limit' : 1, 'sortBy' : 'id', 'sortOrder' : 'descending'})
print audit
audit = "audit.2"
# Let's try getting some hosts from the audit:
hosts = server.call(sessionID, "class.Host", "fetch",{'query' : 'audit = \'%s\'' % audit})
print hosts
# Great, we've got the ID's, but not a lot else, so let's use that data to get more info. First we need to know what attributes we're trying to get data for:
attributes = server.call(sessionID, "class.Host", "getAttributes", {})
print "Attributes for a host includes:"
print attributes
# OK, now we know what all our attributes are, we can ask for each of these 
# Let's pick a single host to test with for now: 
host = "Host.30"
# Let's ask for each of the host's attributes now
print "Host details"
for a in attributes:
    hostdetail = server.call(sessionID, host, "getAttribute", {'attribute': a, })
    print a + ":"
    print hostdetail
# OK, how about getting the IP and scores for all the hosts?
for h in hosts:
    #Get the host IP
    hostIPaddress = server.call(sessionID, h, "getAttribute", {'attribute':'ipAddress'})
    # And it's score
    hostScore = server.call(sessionID, h, "getAttribute", {'attribute':'hostScore'})
    # Print them
    print "Host: " + hostIPaddress + " scored: " 
    print hostScore


# And now we have some hosts, let's get some vuln results
vulns = server.call(sessionID, "class.VulnResult","search",{'query' : 'host = \'%s\'' % host})
print vulns
# Not very interesting - we want the vulnerability details:
attributes = server.call(sessionID, "class.vulnResult", "getAttributes", {})
print "Attributes for a vulnresult includes:"
print attributes
for v in vulns:
    for a in attributes:
        vulnDetails = server.call(sessionID, v, "getAttribute", {'attribute': a})
        print a+":"
        print vulnDetails


import plotly 
plotly.tools.set_credentials_file(username='yourusernamehere', api_key='yourkeyhere')
import plotly.plotly as py
import plotly.graph_objs as go
# Get data from IP360
print "************************************************"
xval = []
yval = []
for h in hosts:
    #Get the host IP
    hostIPaddress = server.call(sessionID, h, "getAttribute", {'attribute':'ipAddress'})
    # And it's score
    hostScore = server.call(sessionID, h, "getAttribute", {'attribute':'hostScore'})
    xval.append(hostIPaddress)
    yval.append(hostScore)
print "************************************************"
print xval
print yval
print "************************************************"
# Create a bar graph
data  = [go.Bar(
    x = xval,
    y = yval
)]
print data
py.iplot(data, filename='basic-bar')
