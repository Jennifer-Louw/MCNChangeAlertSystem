import serial
import boto3

# Initialise variables
consecutive_values1 = 0
consecutive_values2 = 0
consecutive_values3 = 0
consecutive_values4 = 0
prev_value = 0
message_sent = 0

# Initialise SNS client
client = boto3.client(
    "sns",
    aws_access_key_id = 'aws access key',
    aws_secret_access_key = 'aws secret access key',
    region_name = 'ap-southeast-2'
)

# Connect to serial port
serialPort = serial.Serial(port='COM5', baudrate=9600, timeout=0, stopbits=1)

# Read sensor data and trigger SNS message
buffer = ""
while True:
    data = serialPort.read().decode().strip()

    if data.endswith("$"):
        # Extract the values from the buffer
        sensor_data = int(buffer)
        buffer = "" # Reset the buffer
        # Ignore values less than 10
        if sensor_data < 10:
            if message_sent != 5:
                message = 'No action needed'
                print(message)
            message_sent = 5  # Reset the flag
        # Check value range and trigger SNS message if necessary
        # Check if 3 consecutive values less than 40 occurred
        elif sensor_data >= 10 and sensor_data <= 40:
            consecutive_values1 += 1
            if consecutive_values1 == 3 and message_sent != 1:
                message = 'A urination event has occurred, however no change is needed'
                print(message)
                client.publish(
                    TopicArn='arn:aws:sns:ap-southeast-2:043212318633:NappyChange_Alert',
                    Message=message
                )
                message_sent = 1  # Set the flag
        elif sensor_data >= 41 and sensor_data <= 55:
            consecutive_values2 += 1
            if consecutive_values2 == 3 and message_sent != 2:
                message = 'The nappy is lightly wet'
                print(message)
                client.publish(
                    TopicArn='arn:aws:sns:ap-southeast-2:043212318633:NappyChange_Alert',
                    Message=message
                )
                message_sent = 2  # Set the flag
        elif sensor_data >= 56 and sensor_data <= 65:
            consecutive_values3 += 1
            if consecutive_values3 == 3 and message_sent != 3:
                message = 'A nappy change is required at your earliest convenience'
                client.publish(
                    TopicArn='arn:aws:sns:ap-southeast-2:043212318633:NappyChange_Alert',
                    Message=message
                )
                print(message)
                message_sent = 3 # Set the flag
        elif sensor_data >= 66:
            consecutive_values4 += 1
            if consecutive_values4 == 3 and message_sent != 4:
                message = 'The nappy is very wet and an immediate change is required'
                client.publish(
                    TopicArn='arn:aws:sns:ap-southeast-2:043212318633:NappyChange_Alert',
                    Message=message
                )
                print(message)
                message_sent = 4  # Set the flag
        else:
            # Store current value as previous value
            prev_value = sensor_data
            message_sent = 0  # Reset the flag

    else:
        buffer += data
