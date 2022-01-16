import os
import zipfile
from datetime import datetime
import string

def Proxy(proxy, i):
	try:
		line = proxy.split(':')
		PROXY_HOST = line[0]
		PROXY_PORT = line[1]
		PROXY_USER = line[2]
		PROXY_PASS = line[3]

		manifest_json = """
		{
			"version": "1.0.0",
			"manifest_version": 2,
			"name": "Chrome Proxy",
			"permissions": [
				"proxy",
				"tabs",
				"unlimitedStorage",
				"storage",
				"<all_urls>",
				"webRequest",
				"webRequestBlocking"
			],
			"background": {
				"scripts": ["background.js"]
			},
			"minimum_chrome_version":"22.0.0"
		}
		"""

		background_js = string.Template(
		"""
		var config = {
				mode: "fixed_servers",
				rules: {
				singleProxy: {
					scheme: "http",
					host: "${PROXY_HOST}",
					port: parseInt(${PROXY_PORT})
				},
				bypassList: ["foobar.com"]
				}
			};
		chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
		function callbackFn(details) {
			return {
				authCredentials: {
					username: "${PROXY_USER}",
					password: "${PROXY_PASS}"
				}
			};
		}
		chrome.webRequest.onAuthRequired.addListener(
					callbackFn,
					{urls: ["<all_urls>"]},
					['blocking']
		);
		"""
		).substitute(
			PROXY_HOST=PROXY_HOST,
			PROXY_PORT=PROXY_PORT,
			PROXY_USER=PROXY_USER,
			PROXY_PASS=PROXY_PASS)

		with zipfile.ZipFile(f'data/extension/proxy_auth_plugin_{i}.zip', 'w') as zp:
			zp.writestr('manifest.json', manifest_json)
			zp.writestr('background.js', background_js)
		#return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.abspath(__file__))))), 'proxy_auth_plugin.zip')
	except Exception as e:
		#print(e)
		now = datetime.now().strftime('%H:%M:%S')
		print(f'[{now}] - {e}')