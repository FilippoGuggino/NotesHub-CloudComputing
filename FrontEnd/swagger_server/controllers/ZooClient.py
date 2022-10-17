from kazoo.client import KazooClient

class ZooClient:

    def __init__(self, ipAddress):
        self.client = KazooClient(hosts=ipAddress, read_only=True)

    def getRabbitCredentials(self):
        self.client.start()
        username, stats= self.client.get("/credentials/rabbitmq/username")
        psw, stats = self.client.get("/credentials/rabbitmq/password")
        username = username.decode("utf-8")
        psw = psw.decode("utf-8")
        self.client.stop()
        return username, psw

    def get_NOTE_MAX_LEN(self):
        self.client.start()
        max_len, stats = self.client.get("/note_max_length")
        max_len.decode("utf-8")
        self.client.stop()
        return int(max_len)

    def getMongoCredentials(self):
        self.client.start()
        username, stats = self.client.get("/credentials/mongodb/username")
        psw, stats = self.client.get("/credentials/mongodb/password")
        username = username.decode("utf-8")
        psw = psw.decode("utf-8")
        self.client.stop()
        return username, psw

    def getMongoAddress(self):
        self.client.start()
        ip, stats = self.client.get("/ip_addresses/mongodb/master")
        port, stats = self.client.get("/ports/mongodb")
        ip = ip.decode("utf-8")
        port = port.decode("utf-8")
        self.client.stop()
        return ip, port

    def getRabbitAddress(self):
        self.client.start()
        ip, stats = self.client.get("/ip_addresses/rabbitmq/master")
        port, stats = self.client.get("/ports/rabbitmq")
        ip = ip.decode("utf-8")
        port = port.decode("utf-8")
        self.client.stop()
        return ip, port
