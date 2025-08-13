import openhtf as htf
from openhtf.output.servers import station_server
from openhtf.output.web_gui import web_launcher
from openhtf.plugs import user_input
from openhtf.util import configuration
from openhtf.output.callbacks import json_factory
from reachy2_testing import usb_dev
import datetime

CONF = configuration.CONF

def main():

    CONF.load(station_server_port='4444')
    now=datetime.datetime.now()


    with station_server.StationServer() as server:
        web_launcher.launch('http://localhost:4444') #might be launched on a distant computer?

        test = htf.Test(
            usb_dev.rplidar2_dev,
            usb_dev.vesc_dev,
            usb_dev.antennas_dev,
            usb_dev.grippers_dev,
        )
        test.add_output_callbacks(server.publish_final_state)
        test.add_output_callbacks(json_factory.OutputToJSON(f"test_result_{now.isoformat()}.json", indent=2))
        test.execute(test_start=user_input.prompt_for_test_start())


if __name__ == '__main__':
    main()
