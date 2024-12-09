# todo: take cli args for phonenumber
# todo: take dotfile or other config for tty configuration
# todo: externalize send_AT_command function

# derived from WaveShare example code and GPT which is unknown license
import serial
import time
import argparse
serial_connection = serial.Serial("/dev/ttyS0",115200)
receive_buffer = ''
def send_AT_command(command, expected_response, timeout):
  receive_buffer = ''
  serial_connection.write((command+'\r\n').encode())
  time.sleep(timeout)
  if serial_connection.inWaiting():
    time.sleep(0.01)
    receive_buffer = serial_connection.read(serial_connection.inWaiting())
  if expected_response not in receive_buffer.decode():
    print(command + ' ERROR')
    print(command + ' response:\t' + receive_buffer.decode())
    return 0
  else:
    print(receive_buffer.decode())
    return 1

def wait_for_hangup(ser):
  print("Waiting for call to be hung up...")
  while True:
    if ser.inWaiting():
      response = ser.read(ser.inWaiting()).decode()
      if "NO CARRIER" in response:
        print("Call ended by the other party.")
        break
    time.sleep(1)

def main(phone_number):
  try:
    # todo: annotate AT commands
    # todo: better yet, make an API
    send_AT_command('AT+CSQ','OK',1)
    send_AT_command('AT+CREG?','OK',1)
    send_AT_command('AT+CPSI?','OK',1)
    send_AT_command('ATD'+phone_number+';','OK',1)
    wait_for_hangup(serial_connection)
  except Exception as e:
    print(f"An error occured: {e}")
  finally:
    serial_connection.close()

if __name__ == "__main__":
  # todo: input validation
  parser = argparse.ArgumentParser(description="Make a phone call using a serial modem.")
  parser.add_argument("phone_number", help="The phone number to call")
  args = parser.parse_args()
  
  main(args.phone_number)