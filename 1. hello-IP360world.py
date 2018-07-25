# IP360 API Tutorial Example Script
msg = "IP360 API Example"
print(msg)

USERNAME = "ip360@tripwire.com"
PASSWORD = "YourTripwireVnEPasswordHere"
VNEADDRESS = "192.168.0.58"

import xmlrpclib
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

server = xmlrpclib.ServerProxy("https://"+VNEADDRESS+"/api2xmlrpc")
sessionID = server.login(2,0,USERNAME,PASSWORD)
result = server.call(sessionID, "SESSION", "getUserObject",{})
print "My user object is %s" % (result)

