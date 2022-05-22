import xml.etree.ElementTree as ET

#такой словарь нужен для создания гибкой настройки в дальнейшем
files = {'supermarket': open('Supermarkets.csv', 'w'), 'industrial': open('Work.csv', 'w'), 
	'office': open('Work.csv', 'w'), 'hospital': open('Medecine.csv', 'w'), 'clinic': open('Medecine.csv', 'w'),
	'school': open('Education.csv', 'w'), 'university': open('Education.csv', 'w'), 'kindergarten' : open('Education.csv', 'w')}

def parseBuilding(node, file):
	global files
	row = {'name' : '[empty]', 'lat' : node.attrib['lat'], 'lon' : node.attrib['lon']}
	for tag in node.iter('tag'):
		if tag.attrib['k'] == 'name':
			row['name'] = tag.attrib['v']
			break
	files[file].write(row['name']+';'+row['lat']+';'+row['lon']+'\n')



data = ET.parse('map.xml').getroot()
for node in data.iter('node'):
	for tag in node.iter('tag'):
		try:
			parseBuilding(node, tag.attrib['k'])
			break
		except:
			pass
		try:
			parseBuilding(node, tag.attrib['v'])
			break
		except:
			pass


for key in files:
	files[key].close()