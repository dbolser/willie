from willie.module import commands, example
from willie import web
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

@commands('ena')
def ena_lookup(bot, trigger):	
	url = 'http://www.ebi.ac.uk/ena/data/view/%s&display=xml' % trigger.group(2)
	page = web.get(url)
	tree = ET.fromstring(page)
	if tree.text.strip().endswith('not found.'):
		bot.say("ENA doesn't have an entry for '%s'" % trigger.group(2))
	else:
		try:
			desc = tree.iter('DESCRIPTION').next().text
			bot.say(desc)
		except StopIteration:
			bot.say("entry for '%s' doesn't have a DESCRIPTION tag" % trigger.group(2))

@commands('ebistaff')
def ebi_staff_search(bot, trigger):
	url = 'http://www.ebi.ac.uk/ebisearch/search.ebi?query=%s&db=ebiweb' % trigger.group(2)
	page = web.get(url)	
	soup = BeautifulSoup(page)	
	name_link = soup.find('a', title='View in the website')
	if name_link:		
		name = name_link.text
		name = ' '.join(name.split())
		room = soup.find('span', text='Room: ').next_sibling
		telephone = soup.find('span', text='Tel: ').next_sibling
		position = soup.find('span', text="Position(s): ").next_sibling.next.text
		position = ' '.join(position.split())		
		bot.say('%s | room %s | %s |  %s' % (name, room, telephone, position))
	else:
		bot.say("couldn't find '%s'" % trigger.group(2))