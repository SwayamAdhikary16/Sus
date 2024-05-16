from confluent_kafka import Producer
import json
import random 
import time

def generate():
    return str(random.randint(0,1))

producer = Producer({'bootstrap.servers': 'localhost:9092'})

header = '1111111111111111'

for i in range(10):
    for j in header:
        producer.produce('sample', key=None, value=str(j))    
        print(f'Data sent {j}')
        time.sleep(1)
    data = generate()
    producer.produce('sample', key=None, value=data)
    print(f'Data sent {data}')
    producer.flush()
    time.sleep(1)
exit()
producer.close()  # Close the producer
