from driver import Driver
from rider import Rider


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    """

    def __init__(self):
        """Initialize a Dispatcher.

        @type self: Dispatcher
        @rtype: None
        """

        self.waiting_list = []
        self.driving_fleet = []

    def __str__(self):
        """Return a string representation.

        @type self: Dispatcher
        @rtype: str

        >>> dispatcher = Dispatcher()
        >>>print(dispatcher)
        Waiting list: []
        Drivers: []
        """
        return 'Waiting list: {}\nDrivers: {}'.format(self.waiting_list,
                                                      self.driving_fleet)

    def __eq__(self, other):
        """
        Return whether Dispatcher self is equivalent to other

        @param Dispatcher self: this Dispatcher
        @param Dispatcher|Any other: object to compare
        @rtype: bool

        >>> dispatcher = Dispatcher()
        >>> dispatcher2 = Dispatcher()
        >>> dispatcher == dispatcher2
        True
        """
        return (type(self) == type(other) and
                self.waiting_list == other.waiting_list and
                self.driving_fleet == other.driving_fleet)

    def request_driver(self, rider):
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: Driver | None
        """

        nearest_driver = self.nearest_driver(rider)

        if nearest_driver is None:
            self.waiting_list.append(rider)
            return None
        else:
            nearest_driver.is_idle = False
            return nearest_driver

    def request_rider(self, driver):
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        @type self: Dispatcher
        @type driver: Driver
        @rtype: Rider | None
        """

        if driver not in self.driving_fleet:
            self.driving_fleet.append(driver)

        if len(self.waiting_list) is 0:
            return None
        else:
            driver.is_idle = False
            return self.waiting_list.pop(0)

    def cancel_ride(self, rider):
        """Cancel the ride for rider.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: None
        """

        rider.status = 'cancelled'

        if rider in self.waiting_list:
            self.waiting_list.remove(rider)

    def nearest_driver(self, rider):
        """
        Return the closest driver to the rider, or none if no rider is available

        @param Dispatcher self: this Dispatcher
        @param Rider rider:
        @rtype: Driver | None

        >>> from location import Location
        >>> dispatcher = Dispatcher()
        >>> rider = Rider('Cerise', Location(4,2), Location(1,5), 15)
        >>> driver = Driver('Edelweiss', Location(4,2), 1)
        >>> driver2 = Driver('Crocus', Location(3,1), 1)
        >>> driver3 = Driver('Foxglove', Location(5,2), 1)
        >>> dispatcher.driving_fleet = [driver, driver2, driver3]
        >>> dispatcher.nearest_driver(rider)
        'Edelweiss'

        >>> dispatcher = Dispatcher()
        >>> rider = Rider('Cerise', Location(4,2), Location(1,5), 15)
        >>> dispatcher.nearest_driver(rider)
        None
        """

        temp_driver = None

        for driver in self.driving_fleet:
            # setting temp_driver to first idle driver
            if temp_driver is None and driver.is_idle:
                temp_driver = driver
            # replacing temp_driver with the closest idle driver
            elif temp_driver is not None and driver.is_idle:
                if (driver.get_travel_time(rider.origin) <
                   temp_driver.get_travel_time(rider.origin)):
                    temp_driver = driver

        return temp_driver
