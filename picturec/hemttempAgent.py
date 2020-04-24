import serial
import time, logging
import walrus

START_MARKER = '<'
END_MARKER = '>'
REDIS_DB = 0

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Hemtduino(serial.Serial):
    def __init__(self, port, baudrate, timeout=None, queryTime=1):
        super(Hemtduino, self).__init__(port=port, baudrate=baudrate, timeout=timeout)
        self.queryTime = queryTime
        self.redis = walrus.Walrus(host='localhost', port=6379, db=REDIS_DB)

    def arduino_receive(self):
        dataStarted = False
        messageComplete = False
        dataBuffer = ""

        while True:
            if self.in_waiting > 0 and not messageComplete:
                x = self.read().decode("utf-8")

                if dataStarted:
                    if x is not END_MARKER:
                        dataBuffer += x
                    else:
                        dataStarted = False
                        messageComplete = True
                elif x == START_MARKER:
                    dataStarted = True
                    dataBuffer = ""

            elif messageComplete:
                messageComplete = False
                return dataBuffer
            else:
                return "XXX"

    def arduino_wait(self):
        log.debug("Waiting for Arduino")
        self.arduino_send("ping")

        msg = self.arduino_receive()
        log.info(msg)

    def arduino_send(self, command):
        cmdWMarkers = START_MARKER
        cmdWMarkers += command
        cmdWMarkers += END_MARKER

        self.write(cmdWMarkers.encode("utf-8"))
        time.sleep(0.5)

    # def _run_once(self):

    def run(self):
        self.arduino_wait()
        prevTime = time.time()
        start = prevTime

        while True:
            if time.time() - prevTime >= self.queryTime:
                log.debug("Sending Query")
                self.arduino_send("all")
                arduinoReply = self.arduino_receive()
                log.info(arduinoReply)
                prevTime = time.time()


if __name__ == "__main__":

    hemtduino = Hemtduino(port="/dev/ttyS9", baudrate=9600, timeout=1)
    hemtduino.run()
