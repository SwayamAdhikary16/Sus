from confluent_kafka import Consumer, KafkaError
import json
import time

# Create a Kafka consumer
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'
})

# Subscribe to the 'sample' and 'pytest' topics
consumer.subscribe(['sample', 'pytest'])

received_data = ''
timeout = 5  # Timeout in seconds
last_received_time = time.time()

while True:
    msg = consumer.poll(timeout=1.0)
    if msg is None:
        # Check for timeout even if no message is received
        current_time = time.time()
        if current_time - last_received_time >= timeout:
            print("Data not received for 5 seconds. Storing in list:", received_data)
            break
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            # End of partition, reset consumer's offsets to start from the beginning
            consumer.seek_to_beginning(msg.partition())
            print("Reached end of partition. Resetting offsets.")
            continue
        else:
            # Other error, stop consuming.
            print(msg.error())
            break

    # Decode the message value and add it to the received data
    value = msg.value().decode('utf-8')
    print('Value Received',value)
    received_data += value

    # Update the last received time
    last_received_time = time.time()

# Close the consumer
consumer.close()
