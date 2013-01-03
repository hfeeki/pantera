import unittest
import mock

from pantera import chaos
import pantera


class SimulatorCalled(Exception):
    pass


class RaisingSimulator(object):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        raise SimulatorCalled


class PanterTestCase(unittest.TestCase):
    @mock.patch("random.choice")
    def test_run_call(self, choice):
        choice.return_value = RaisingSimulator
        self.assertRaises(SimulatorCalled, pantera.run)

    @mock.patch("random.choice")
    def test_run_init(self, choice):
        mock_obj = mock.Mock()
        choice.return_value = mock_obj
        pantera.run("one", "two")
        mock_obj.assert_called_with("one", "two")


class EC2TestCase(unittest.TestCase):
    def test_init(self):
        ec2 = chaos.EC2("one", "two")
        self.assertEqual("one", ec2.access)
        self.assertEqual("two", ec2.secret)

    @mock.patch("random.choice")
    def test_choice(self, choice):
        instance = mock.Mock(id="1")
        reservation = mock.Mock(instances=[instance])
        ec2 = chaos.EC2("ac", "sec")
        ec2.conn = mock.Mock()
        choice.return_value = reservation
        vm = ec2.choice()
        self.assertEqual("1", vm)

    @mock.patch("boto.ec2.connection.EC2Connection")
    def test_connect(self, ec2con):
        ec2 = chaos.EC2("ac", "sec")
        ec2.connect()
        ec2con.assert_called_with("ac", "sec")


class RebootTestCase(unittest.TestCase):
    def test_reboot(self):
        from pantera import chaos
        vms = ["1"]
        conn = mock.Mock()
        conn.reboot_instances.return_value = vms
        choice = mock.Mock()
        choice.return_value = "1"
        reboot = chaos.Reboot("access", "secret")
        reboot.connect = mock.Mock()
        reboot.conn = conn
        reboot.choice = choice
        destroyed = reboot.reboot()
        self.assertListEqual(vms, destroyed)

    def test_call(self):
        from pantera import chaos
        reboot = chaos.Reboot("access", "secret")
        reboot.reboot = mock.Mock()
        reboot()
        reboot.reboot.assert_called_with()


class StopTestCase(unittest.TestCase):
    def test_stop(self):
        vms = ["1"]
        conn = mock.Mock()
        conn.stop_instances.return_value = vms
        choice = mock.Mock()
        choice.return_value = "1"
        stop = chaos.Stop("access", "secret")
        stop.connect = mock.Mock()
        stop.conn = conn
        stop.choice = choice
        destroyed = stop.stop()
        self.assertListEqual(vms, destroyed)

    def test_call(self):
        stop = chaos.Stop("access", "secret")
        stop.stop = mock.Mock()
        stop()
        stop.stop.assert_called_with()


class TerminateTestCase(unittest.TestCase):
    def test_terminate(self):
        vms = ["1"]
        conn = mock.Mock()
        conn.terminate_instances.return_value = vms
        choice = mock.Mock()
        choice.return_value = "1"
        terminate = chaos.Terminate("access", "secret")
        terminate.connect = mock.Mock()
        terminate.conn = conn
        terminate.choice = choice
        destroyed = terminate.terminate()
        self.assertListEqual(vms, destroyed)

    def test_call(self):
        terminate = chaos.Terminate("access", "secret")
        terminate.terminate = mock.Mock()
        terminate()
        terminate.terminate.assert_called_with()