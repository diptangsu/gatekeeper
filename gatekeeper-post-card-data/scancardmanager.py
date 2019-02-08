import requests


# receptionist
url_scan_card = 'http://127.0.0.1:8000/scan/submit-card'

# company door
url_visitor_reached = 'http://127.0.0.1:8000/scan/visitor-reached'


receptionist_data = {
	'uid': 1322,  # from scan
}
files = {
	'image': open('slytherin.png', 'rb')
}

company_data = {
	'uid': 1321,  # from scan
	'company_id': 3,  # hard coded based on company id/ company door pi
}

response = requests.post(url=url_scan_card, data=receptionist_data, files=files)
# response = requests.post(url=url_visitor_reached, data=company_data)
