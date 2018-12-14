#                              dP       M""MMMMM""MM M""""""""M M"""""`'"""`YM M""MMMMMMMM 
#                              88       M  MMMMM  MM Mmmm  mmmM M  mm.  mm.  M M  MMMMMMMM 
# 88d8b.d8b. .d8888b. .d8888b. 88  .dP  M         `M MMMM  MMMM M  MMM  MMM  M M  MMMMMMMM 
# 88'`88'`88 88'  `88 Y8ooooo. 88888"   M  MMMMM  MM MMMM  MMMM M  MMM  MMM  M M  MMMMMMMM 
# 88  88  88 88.  .88       88 88  `8b. M  MMMMM  MM MMMM  MMMM M  MMM  MMM  M M  MMMMMMMM 
# dP  dP  dP `88888P8 `88888P' dP   `YP M  MMMMM  MM MMMM  MMMM M  MMM  MMM  M M         M 
#                                       MMMMMMMMMMMM MMMMMMMMMM MMMMMMMMMMMMMM MMMMMMMMMMM 
#
# ----------------------------------------------------------------------------------------
# by @paulpierre (11/26/2018)
#
# Proof-of-concept polymorphic fracturing of content tags as well as padder of HTML files
# using HTML elements invisible to the end-user. Purpose of this is to "cloak" a landing
# page submitted to an advertiser to avoid heuristics and fingerprinting checks
#
# More at: https://github.com/paulpierre

from bs4 import BeautifulSoup
import htmlmin
import sys
import random
import string



#==============
# Configuration
#==============

#Bank of characters to utilize when generating random words
string.letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 '

class config:
	# How often we want to insert the padding tags to separate HTML tags
	PADDING_INJECTION_RATE = 1

	# How often we want to fracture words within a content tag measured by character length
	FRACTURE_INJECTION_RATE = .5

	# Minimum character length of the randomly generated word
	WORD_MIN_LENGTH = 6

	# Maximum character length of the randomly generated word
	WORD_MAX_LENGTH = 10

	# The tags that will be injected into content tags used for fracturing
	FRACTURE_TAGS = ["font","span"]

	# Tags to be used for padding. A newline character will also be used
	PAD_TAGS = ["input"]

	# Tags we should target for fracturing
	CONTENT_TAGS = ["p", "a", "meta","link","html","nav","button", "div", "li", "span", "i", "strong","h1","h2","h3","h4","h5","section","footer","header"]

	MINIFY_HTML = False

#Because colorful ascii is sublime
class colors:
    GREEN = '\033[32m'
    NORMAL = '\033[37m'
    TEAL = '\033[36m'


#==========
# Functions
#==========

#Everyone needs a good intro amirite?
def main_screen():
	print " ----------------------------------------------------------------------------------------"
	print colors.GREEN + "                              dP       M\"\"MMMMM\"\"MM M\"\"\"\"\"\"\"\"M M\"\"\"\"\"`'\"\"\"`YM M\"\"MMMMMMMM" 
	print "                              88       M  MMMMM  MM Mmmm  mmmM M  mm.  mm.  M M  MMMMMMMM"
	print " 88d8b.d8b. .d8888b. .d8888b. 88  .dP  M         `M MMMM  MMMM M  MMM  MMM  M M  MMMMMMMM"
	print " 88'`88'`88 88'  `88 Y8ooooo. 88888\"   M  MMMMM  MM MMMM  MMMM M  MMM  MMM  M M  MMMMMMMM"
	print " 88  88  88 88.  .88       88 88  `8b. M  MMMMM  MM MMMM  MMMM M  MMM  MMM  M M  MMMMMMMM"
	print " dP  dP  dP `88888P8 `88888P' dP   `YP M  MMMMM  MM MMMM  MMMM M  MMM  MMM  M M         M"
	print "                                       MMMMMMMMMMMM MMMMMMMMMM MMMMMMMMMMMMMM MMMMMMMMMMM" + colors.NORMAL
	print " ----------------------------------------------------------------------------------------"
	print " by @paulpierre \n\n"
	return

def generate_random_word():
	word_length = random.randint(config.WORD_MIN_LENGTH,config.WORD_MAX_LENGTH)
	word = ""
	for i in range(word_length):
		word += random.choice(string.letters)
	return word
	
def get_fracture_tag():
	index = random.randint(0,len(config.FRACTURE_TAGS)-1)
	tag = soup.new_tag(config.FRACTURE_TAGS[index],style="display:none;")

	return "<" + config.FRACTURE_TAGS[index] + " style=\"display:none;\">" + generate_random_word() +  "</" + config.FRACTURE_TAGS[index] + ">"

def fracture_string(input_string):

	output_string = ""
	char_hit_rate = 0

	random_1 = 0
	random_2 = 0

	char_count = len(input_string)
	for input_char in input_string:
		if input_char == "\n" or input_char == " ":
			output_string +=input_char
		 	continue


		random_1 = random.randint(1,(config.FRACTURE_INJECTION_RATE * 10))
		random_2 = random.randint(1,(config.FRACTURE_INJECTION_RATE * 10))
 		#print " random: " + str(random_1) + " random: " + str(random_2) + "\n\n"

		if(random_1 == random_2):
			char_hit_rate +=1
			output_string +=get_fracture_tag()

		output_string += input_char
	
	#print input_char
	print colors.NORMAL + "char count:" + str(len(input_string)) + " hit_rate: " + str(char_hit_rate) + " rate: " + str(float(char_hit_rate/char_count))

	return output_string


def load_html(file_name):
	with open(file_name) as fp:
		soup_obj = BeautifulSoup(fp,features="html.parser")
	return soup_obj


def minify(data):
	min = htmlmin.minify(data.decode("utf8"),remove_empty_space=True)
	return min


def export(data,file_name):
	f = open(file_name, "w")
	if config.MINIFY_HTML:
		f.write(minify(data).encode('utf-8'))
	else:
		f.write(data)
	
	return

def fracture_obj(element):
		print "TAG: " + element.name + "\n\n"
		# lets fracture the string
		fractured_string = fracture_string(element.string)

		print colors.GREEN + "[" + element.name + "]-----------------------------------------------" + colors.NORMAL
		print element.string
		print colors.GREEN + "--------------------------------------------------" + colors.NORMAL
		print colors.TEAL + fractured_string + "\n" + colors.NORMAL

		element.string = fractured_string


def pad_obj(element):

	# lets also pad
	random_1 = 0
	random_2 = 0

	if config.PAD_TAGS and len(config.PAD_TAGS) > 0:
		random_1 = random.randint(1,(config.PADDING_INJECTION_RATE * 10))
		random_2 = random.randint(1,(config.PADDING_INJECTION_RATE * 10))

		if random_1 == random_2:
			index = random.randint(0,len(config.PAD_TAGS)-1)
			tag = soup.new_tag(config.PAD_TAGS[index],style="display:none;")
			element.append(tag)


main_screen()
input_file = "demo/index.html"
output_file = "demo/index2.html"

soup = load_html(input_file)

content_tags = soup.find_all(config.CONTENT_TAGS)

print "\n=========================\n" + "Qualified tag count: " + str(len(content_tags)) + "\n=========================\n\n"

for element in content_tags:

	#If we get children nodes containing the text, not parent nodes containing children nodes with text
	#and it HAS a string and not just empty space or special characters, lets fracture it!

	print "children len: " + str(len(element.findChildren())) + "!!!"
	print "\n------------\n" + "Checking tag: " + element.name + "\n--------------\n\n"
	if element.string is not None: print "tag content: " + element.string + "\n"
	else: print "NoneType\n"




	if element.string is not None: #and len(element.findChildren()) == 0: 
		fracture_obj(element)
	#elif len(element.findChildren()) == 0:
	#	for el in element.descendants 


	pad_obj(element)






export(str(soup.prettify(formatter=None).encode('utf-8')),output_file)
#print soup

sys.exit()
