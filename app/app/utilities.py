from datetime import datetime
import random

def generate_id():
	return f'{str(datetime.now())}-{random.randrange(100)}'
