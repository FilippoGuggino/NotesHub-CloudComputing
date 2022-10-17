

from kazoo.client import KazooClient

zk = KazooClient(hosts='172.16.2.40:2181', read_only=True)
zk.start()
zk.delete("/credentials/rabbitmq",recursive=True)
zk.delete("/ip_addresses/rabbitmq",recursive=True)
zk.delete("/ports/rabbitmq",recursive=True)
zk.delete("/credentials/mongodb",recursive=True)
zk.delete("/ip_addresses/mongodb",recursive=True)
zk.delete("/ports/mongodb",recursive=True)
zk.delete("/note_max_length",recursive=True)
zk.delete("/credentials",recursive=True)
zk.delete("/ip_addresses",recursive=True)
zk.delete("/ports",recursive=True)
zk.delete("/mongodb",recursive=True)
zk.delete("routing_key",recursive=True)

#Store the data
zk.ensure_path("/credentials/rabbitmq")
zk.create("/credentials/rabbitmq/username", b"guest")
zk.create("/credentials/rabbitmq/password", b"guest")

zk.ensure_path("/ip_addresses/rabbitmq")
zk.ensure_path("/ports")
zk.create("/ip_addresses/rabbitmq/master",b"172.16.1.157")
zk.create("/ports/rabbitmq",b"5672")#5762

zk.ensure_path("/credentials/mongodb")
zk.create("/credentials/mongodb/username", b"myUser")
zk.create("/credentials/mongodb/password", b"abcd")

zk.ensure_path("/ip_addresses/mongodb")
zk.create("/ip_addresses/mongodb/master",b"172.16.3.34")
zk.create("/ports/mongodb", b"2717")

zk.ensure_path("/mongodb/")
zk.create("/mongodb/database",b"notes-db")
zk.create("/mongodb/collection",b"notesCollection")
zk.create("/routing_key",b"rpc_queue")
zk.create("/note_max_length",b"500")

zk.stop()
