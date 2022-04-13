import requests
import json
import sys
import argparse

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0)',
	'tellonym-client': 'web:0.63.5',
	'content-type': 'application/json;charset=utf-8'
}

def get_user_info(username):
	"""	Gets informations about a username (We need the User-ID)
	"""
	try:
		response = requests.get('https://api.tellonym.me/profiles/name/{0}'.format(username), headers=headers)
		data = json.loads(response.text)
	except Exception as e:
		print("[!] Failed to connect to the Tellonym API (https://api.tellonym.me)")
		return False, None
	else:
		if 'err' in data:
			print("[!] User '{0}' doenst seem to exist".format(username))
			return False, None
		else:
			del data['answers']
			return True, data

def get_tells_of_user(user_id):
	""" Iterates trough all tells/answers of the user and collects them in a list of dictionaries.
	"""
	tells = []
	position = 0
	while True:
		params = {'limit':'100','pos':str(position)}
		response = requests.get('https://api.tellonym.me/answers/{0}'.format(user_id), headers=headers, params=params)
		new_tells = json.loads(response.text)['answers']

		for tell in new_tells: tells.append(tell)
		if len(new_tells) > 0:
			print("  > Got another {0} from API - (Total collected: {1})".format(len(new_tells), len(tells)))
		
		if len(new_tells) == 100:
			position = position + 100
		else:
			print("  > Last page reached")
			break;
	return tells

def remove_unnecessary_data(data):
	# I know this is not particularly nice, but I needed a fast solution :P
	keys_to_keep = ['tell', 'answer', 'createdAt']
	data_new = {'user_info':data['user_info'], 'answers':[]}
	for answer in data['answers']:
		new_answer = {'tell':answer['tell'], 'answer':answer['answer'], 'createdAt':answer['createdAt']}
		data_new['answers'].append(new_answer)
	return data_new

def banner():
	print("  _______   _ _                                ")
	print(" |__   __| | | |                               ")
	print("    | | ___| | | ___  ___  ___ _ __ __ _ _ __  ")
	print("    | |/ _ \ | |/ _ \/ __|/ __| '__/ _` | '_ \ ")
	print("    | |  __/ | | (_) \__ \ (__| | | (_| | |_) |")
	print("    |_|\___|_|_|\___/|___/\___|_|  \__,_| .__/ ")
	print("                                        | |    ")
	print("    Version: 1.0 - Author: @curosim     |_|    \n")

def help(args):
	print("    Description:")
	print("    Telloscrap is a crawler for Tellonym.me Users.")
	print("    It downloads User Info, Questions and Answers and saves it to a file.\n")
	print("    Usage: {0} USERNAME [--full]".format(args[0]))
	print("    Use --full to save metadata too (Default: False).")


def abort():
	print("[*] Aborting...")
	exit()


def main(args):
	banner()

	# Check if the minimal amount of arguments got passed (pos 0 is always the script name)
	if len(args) < 2:
		help(args)
		exit()
	
	# Check if the user requested help
	if args[1] == '-h' or args[1] == '--help':
		help(args)
		exit()

	print("[*] Starting to crawl data for user '{0}'".format(args[1]))

	# Check if user exists
	success, info = get_user_info(args[1])
	if success == False:
		abort()
	else:
		print("[*] User '{0}' exists!".format(args[1]))

	print("[*] Collecting questions and answers")

	# Collect all questsions and answers
	data = {}
	data['user_info'] = info
	data['answers'] = get_tells_of_user(user_id=data['user_info']['id'])

	# Display crawling summary
	print("[*] FINISHED!")
	print("    Total tells: {0}".format(data['user_info']['tellCount']))
	print("    Crawled tells: {0}".format(len(data['answers'])))
	if data['user_info']['tellCount'] > len(data['answers']):
		if len(data['answers']) == 0:
			print("    Note: Although there were tells once, we cant see them anymore :(")
		else:
			print("    Note: It seems not all Tells can be seen anymore.")

	
	# Clean the JSON of data we dont need
	keep_metadata = False
	if len(args) == 3:
		if args[2] == '--full':
			keep_metadata = True
	if keep_metadata == False: data = remove_unnecessary_data(data)

	# Write results to file
	filename = '{0}.json'.format(data['user_info']['username'])
	with open(filename, 'w') as f:
		f.write(json.dumps(data, indent=4, sort_keys=True))

	print("[*] Results written to file '{0}'".format(filename))


if __name__ == '__main__':
	try:
		main(sys.argv)
	except KeyboardInterrupt:
		print("[*] Execution stopped by keyboard!")
		abort()