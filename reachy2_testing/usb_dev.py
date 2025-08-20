import os
import openhtf as htf



@htf.measures(
    htf.Measurement("is_rplidar_s2_dev_exists")
    .equals(True)
)
def rplidar_s2_dev(test):
    test.logger.info("checking /dev/rplidar_s2")
    test.measurements.is_rplidar_s2_dev_exists= os.path.exists("/dev/rplidar_s2")
    if test.measurements.is_rplidar_s2_dev_exists:
        test.logger.info("/dev/rplidar_s2 exists")
        return htf.PhaseResult.CONTINUE
    else:
        test.logger.error("/dev/rplidar_s2 not found!")
        return htf.PhaseResult.FAIL_AND_CONTINUE

@htf.measures(
    htf.Measurement("is_vesc_dev_exists")
    .equals(True)
)
def vesc_dev(test):
    test.measurements.is_vesc_dev_exists= os.path.exists("/dev/vesc_wheels")
    if test.measurements.is_vesc_dev_exists:
        test.logger.info("/dev/vesc_wheels exists")
        return htf.PhaseResult.CONTINUE
    else:
        test.logger.error("/dev/vesc_wheels not found!")
        return htf.PhaseResult.FAIL_AND_CONTINUE

@htf.measures(
    htf.Measurement("is_antennas_dev_exists")
    .equals(True)
)
def antennas_dev(test):
    test.measurements.is_antennas_dev_exists= os.path.exists("/dev/antennas")
    if test.measurements.is_antennas_dev_exists:
        test.logger.info("/dev/antennas exists")
        return htf.PhaseResult.CONTINUE
    else:
        test.logger.error("/dev/antennas not found!")
        return htf.PhaseResult.FAIL_AND_CONTINUE


@htf.measures(
    htf.Measurement("is_grippers_dev_exists")
    .equals(True)
)
def grippers_dev(test):
    test.measurements.is_grippers_dev_exists= os.path.exists("/dev/grippers")
    if test.measurements.is_grippers_dev_exists:
        test.logger.info("/dev/grippers exists")
        return htf.PhaseResult.CONTINUE
    else:
        test.logger.error("/dev/grippers not found!")
        return htf.PhaseResult.FAIL_AND_CONTINUE
