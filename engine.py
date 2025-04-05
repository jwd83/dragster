# engine is defined a list of tuples with the  (rpm,  torque) value at each point.
# electric motors will have a torque value at 0. gas engine are assumed 0 at 0 rpm.


class Engine:
    def __init__(self, torque_curve: list):
        self.torque_curve = torque_curve.copy()
        self.max_rpm = max(torque[0] for torque in torque_curve)
        self.max_torque = max(torque[1] for torque in torque_curve)
        self.min_rpm = min(torque[0] for torque in torque_curve)

    def torque(self, rpm: float):
        # Interpolate the torque value based on the RPM
        for i in range(len(self.torque_curve) - 1):
            if self.torque_curve[i][0] <= rpm <= self.torque_curve[i + 1][0]:
                rpm1, torque1 = self.torque_curve[i]
                rpm2, torque2 = self.torque_curve[i + 1]
                return torque1 + (torque2 - torque1) * (rpm - rpm1) / (rpm2 - rpm1)
        return 0.0

    def horsepower(self, rpm: float):
        # Calculate horsepower based on torque and RPM
        torque = self.torque(rpm)
        return (torque * rpm) / 5252
