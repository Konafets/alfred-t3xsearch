# encoding: utf-8

import sys
import json
from workflow import Workflow, ICON_WARNING, web

def get_extensions():
	url = 'http://composer.typo3.org/packages-TYPO3Extensions-archive.json'
	
	r = web.get(url)

	r.raise_for_status()

	result = r.json()
	extensions = result['packages']

	return extensions

def main(wf):
	url_ter = 'http://typo3.org/extensions/repository/view/'

	if len(wf.args):
		query = wf.args[0]
	else: 
		query = None

	extensions = wf.cached_data('extensions', get_extensions, max_age=600)	

	if query:
		filteredExtensions = wf.filter(query, extensions)

	if not filteredExtensions:
		wf.add_item('No matching extensions found.', icon=ICON_WARNING)
		wf.send_feedback()
		return 0

	extensionResult = {}
	for extension in filteredExtensions:
		extensionResult[extension] = extensions[extension]


	for extensionName, version in extensionResult.items():
		extensionkey = extensionName[10:]

		TYPO3Compatibility =  extensionResult[extensionName][max(version)]['require']['typo3/cms']
		wf.add_item(
			title=extensionkey,
			subtitle='Latest version: ' + max(version) + ', Compatible with TYPO3: ' + TYPO3Compatibility,
			arg=url_ter + extensionkey,
			valid=True,
			icon='TYPO3Logo.png'
		)

	wf.send_feedback()

if __name__ == u"__main__":
	wf = Workflow()
	sys.exit(wf.run(main))
