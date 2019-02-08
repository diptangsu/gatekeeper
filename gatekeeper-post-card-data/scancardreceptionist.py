import requests


url = 'http://127.0.0.1:8000/scan/submit-card'
data = {'uid': 123}

response = requests.post(url=url, data=data)


# class X:
# 	def __init__(self, x, y):
# 		self.x = x 
# 		self.y = y

# 	def __str__(self):
# 		return 'x = {}, y = {}'.format(self.x, self.y)


# a = X(2, 3)
# b = X(y=3, x=10)

# print (a)
# print (b)