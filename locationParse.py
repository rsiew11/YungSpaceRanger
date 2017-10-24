import math

#open the text file for the location
fo = open("gpsLocation.txt", "r+")

#longitude = fo.read()
#latitude = fo.read()

#print('longitude is ' + longitude)
#print('latidue is ' + latitude)

s = fo.read(500)
print s

x = s.find("Latitude")
y = s.find("Longitude")
z = s.find("Altitude")

print "latitude",x
print "longitude", y
print "Altitude" , z

latitude = s[x+9:x+16]
longitude = s[y+10:y+16]
altitude = s[z+9:z+16]

print "lat", latitude
print "long", longitude
print "alt", altitude


fo.close()


#generate packet here
