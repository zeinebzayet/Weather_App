from kafka import KafkaConsumer
import json

def consume_weather_data():
    # Create a Kafka consumer
    consumer = KafkaConsumer('weather_topic',
                             bootstrap_servers=['kafka:9092'],
                             auto_offset_reset='earliest',
                             group_id='my-group',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                             api_version=(0, 10, 0))

    while True:
        # Response format is {TopicPartiton('topic1', 1): [msg1, msg2]}
        msg_pack = consumer.poll(timeout_ms=500)

        for tp, messages in msg_pack.items():
                for message in messages:
                # message value and key are raw bytes -- decode if necessary!
                # e.g., for unicode: `message.value.decode('utf-8')`
                    print ("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition,
                                                        message.offset, message.key,
                                                        message.value))


if __name__ == '__main__':
    consume_weather_data()