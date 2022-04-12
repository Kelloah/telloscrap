import requests
import json

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36',
	'tellonym-client': 'web:0.51.1',
	'content-type': 'application/json;charset=utf-8'
}

def get_user_info(username):
	"""	Gets informations about a username (We need the User-ID)
	"""
	response = requests.get('https://api.tellonym.me/profiles/name/{0}'.format(username), headers=headers)
	data = json.loads(response.text)
	if 'err' in data:
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
		print("  > Got another {0} from API - (Total: {1})".format(len(new_tells), len(tells)))
		
		if len(new_tells) == 100:
			position = position + 100
		else:
			print("  > Last page reached")
			break;
	return tells

def banner():
	print("  _______   _ _                                ")
	print(" |__   __| | | |                               ")
	print("    | | ___| | | ___  ___  ___ _ __ __ _ _ __  ")
	print("    | |/ _ \ | |/ _ \/ __|/ __| '__/ _` | '_ \ ")
	print("    | |  __/ | | (_) \__ \ (__| | | (_| | |_) |")
	print("    |_|\___|_|_|\___/|___/\___|_|  \__,_| .__/ ")
	print("                                        | |    ")
	print("                                        |_|    \n")

def close():
	print("[*] Aborting...")
	exit()

def main():
	banner()

	username = input('[*] Please enter Tellonym username: ')

	data = {}
	success, info = get_user_info(username)
	if success == False:
		print("[!] User '{0}' doenst seem to exist".format(username))
		close()

	print("[*] Starting to collect tells of user '{0}'".format(username))

	data['user_info'] = info
	data['answers'] = get_tells_of_user(user_id=data['user_info']['id'])

	print("[*] FINISHED!")
	print("    Total tells: {0}".format(data['user_info']['tellCount']))
	print("    Crawled tells: {0}".format(len(data['answers'])))
	
	filename = '{0}.json'.format(data['user_info']['username'])
	with open(filename, 'w') as f:
		f.write(json.dumps(data, indent=4, sort_keys=True))

	print("[*] All written to file '{0}'".format(filename))


if __name__ == '__main__':
	main()