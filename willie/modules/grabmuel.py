import willie
import urllib2
import xml.etree.ElementTree as ET
import re

@willie.module.commands('ena')
def ena_lookup(bot, trigger):
	url = 'http://www.ebi.ac.uk/ena/data/view/%s&display=xml' % trigger.group(2)
	page = urllib2.urlopen(url).read()
	tree = ET.fromstring(page)
	desc = tree.iter('description').next().text
	bot.say(desc)

@willie.module.commands('ebistaff')
def ebi_people(bot, trigger):
	url = 'http://www.ebi.ac.uk/ebisearch/search.ebi?query=%s&db=ebiweb' % trigger.group(2)
	page = urllib2.urlopen(url).read()
	if 'View in the website' in page:
		name = re.search('title="View in the website" rel="nofollow">(.+?)</a>', page, re.DOTALL).group(1)
		name = ' '.join(name.split())	
		name = unicode(name, 'utf-8').encode('ascii', 'replace')
		room = re.search('Room: </span>(.+?)<br />', page).group(1)
		telephone = re.search('Tel: </span>(.+?)<br />', page).group(1)
		position = re.search('Position\(s\):.+?<span >(.+?)</span>', page, re.DOTALL).group(1)
		position = ' '.join(position.split())
		bot.say('%s | room %s | %s |  %s' % (name, room, telephone, position))
	else:
		bot.say("couldn't find '%s'" % trigger.group(2))
