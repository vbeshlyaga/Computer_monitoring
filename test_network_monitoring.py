import unittest
from network_monitoring import Network, Host, CPU, Memory, HDD, Partition


class TestNetworkMonitoring(unittest.TestCase):
    def test_hierarchy_output(self):
        network = Network("MISIS network")

        host1 = Host("server1.misis.ru", ["192.168.1.1"])
        host1.add_component(CPU(4, 2500))
        host1.add_component(Memory(16000))

        hdd2 = HDD(2000)
        hdd2.add_partition(Partition(500, "0: system"))
        hdd2.add_partition(Partition(1500, "1: data"))

        host2 = Host("server2.misis.ru", ["10.0.0.1"])
        host2.add_component(CPU(8, 3200))
        host2.add_component(hdd2)

        network.add_host(host1)
        network.add_host(host2)

        expected_output = (
            "Network: MISIS network\n"
            "+-Host: server1.misis.ru\n"
            "| +-192.168.1.1\n"
            "| +-CPU, 4 cores @ 2500MHz\n"
            "| \\-Memory, 16000 MiB\n"
            "\\-Host: server2.misis.ru\n"
            "  +-10.0.0.1\n"
            "  +-CPU, 8 cores @ 3200MHz\n"
            "  \\-HDD, 2000 GiB\n"
            "    +-[0: system], 500 GiB\n"
            "    \\-[1: data], 1500 GiB\n"
        )

        actual_output = network.print_me()
        self.assertEqual(actual_output.strip(), expected_output.strip())


if __name__ == "__main__":
    unittest.main()
