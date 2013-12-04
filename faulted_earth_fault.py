#!/usr/bin/env/python

"""
Prototype code for a set of classes corresponding to the Faulted Earth
data model
"""
import numpy as np
from openquake.hazardlib.geo.point import Point
from openquake.hazardlib.geo.line import Line
from openquake.hazardlib.geo.polygon import Polygon


def build_pref_min_max(value, nval):
    """
    Where data is entered as a tuple of (preferred, minimum, maximum) checks
    the logical consistency of the tuple.
    :param value:
        Value of data (any type)
    :param int nval:
        Number of expected values in tuple
    """
    if isinstance(value, tuple):
        if len(value) != nval:
            raise ValueError('Preferred-Min-Max must be a tuple of length 3!')
        # Check maximum is greater than or equal to minimum
        if (nval > 2) and value(1) and value(2) and (value(1) > value(2)):
            raise ValueError('Minimum value in tuple is greater than maximum!')
        return value
    else:
        # Data not entered as tuple, return as a tuple
         value = [value]
         value.extend([None for val in range(0, nval - 1)])
         return tuple(value)

class Parameter(object):
    """
    Class to hold parameter information, including uncertainty value
    :param value:
        The central/expected value of the distribution
    :param minimum:
        Minimum bound of the value
    :param maximum:
        Maximum bound of the value
    :param int completeness:
        Completeness category
    :param str distribution:
        Distribution type
    """
    def __init__(self, value, minimum=None, maximum=None, completeness=None,
            distribution=None):

        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        self.completeness = completeness
        self.distribution = distribution
        self.comment = None


def _assert_assign(value):
    """
    Assert that the value is an instance of the :class:
    hmtk.faults.faulted_earth_fault.Parameter
    """
    assert isinstance(value, Parameter)
    return value


class BaseObservation(object):
    """
    Base class containing attributes common to all observation data.
    :param str id:
        ID of observation
    :param location:
        Location as instance of :class: openquake.hazardlib.geo.point.Point
    :param int scale:
        Map scale
    :param int accuracy:
        Parameter describing accuracy (estimated as 2 * scale)
    :param str notes:
        Notes regarding the site
    :param str fault_section:
        ID of fault section to which the point is assigned (if any)
    :param str site_feature:
        Information regarding the site feature
    """
    def __init__(self, identifer, location, attributes):
        """
        Instantiate base object with essential attributes
        :param str identiifer:
            Unique ID of the point observation
        :param location:
            Location as instance of :class: openquake.hazardlib.geo.point.Point
        :param dict attributes:
            Dictionary of point attributes, containing keys:
            - Scale: Scale of map for deriving observation
            - Accuracy: Accruacy of observation location
            - Notes: Notes regarding location
            - Fault Section: ID of fault section (if assigned)
            - Site Feature: Information regarding the site feature
        """
        self.id = identifier
        assert isinstance(location, Point)
        self.location = location
        self.scale = attributes['Scale']
        if attributes['Accuracy']:
            self.accuracy = attributes['Accuracy']
        elif isinstance(self.scale, int) or isinstance(self.scale, float):
            self.accuracy = 2 * self.scale
        else:
            self.accuracy = None
        self.notes = attributes['Notes']
        self.fault_section = attributes['Fault Section']
        self.site_feature = attributes['Site Feature']



class ObservationDisplacement(BaseObservation):
    """
    Class to hold displacement information for site observation
    """
    def __init__(self, identifier, location, attributes):
        """
        """
        super(ObservationDisplacement, self).__init__(identifier, location,
            attributes)
        self.total_disp = attributes['Total Displacement']
        self.category = attributes['Category']
        self.horizontal_disp = attributes['Horizontal']
        self.vertical_disp = attributes['Vertical']
        self.net_disp = attributes['Net']
        self.displacement = _assert_assign(attributes['Displacement'])


class ObservationEvent(BaseObservation):
    """
    Class to hold event information for site observation
    """
    def __init__(self, identifier, location, attributes):
        """
        """
        super(ObservationEvent, self).__init__(identifier, location,
            attributes)
        self.recurrence = _assert_assign(attributes['Recurrence Interval'])
        self.recurrence_category = attributes['Recurrence Category']
        self.movement =_assert_assign(attributes['Movement'])
        self.movement_category = attributes['Movement Category']
        self.historic_event = attributes['Historic Event']
        self.prehistoric_event = attributes['Prehistoric Event']
        self.marker_age = attributes['Marker Age']


class ObservationGeometry(BaseObservation):
    """
    Class to hold information for site geometry
    """
    def __init__(self, identifier, location, attributes):
        """
        """
        super(ObservationGeometry, self).__init__(identifier, location,
            attributes)
        self.dip_dir = attributes['Dip Direction']
        self.down_side = attributes['Downthrown Side']
        self.strike = attributes['Strike']
        self.dip = attributes['Dip']


class ObservationSlipRate(BaseObservation):
    """
    Class to hold site slip rate observation data 
    """
    def __init__(self, identifier, location, attributes):
        """
        """
        super(ObservationSlipRate, self).__init__(identifier, location,
            attributes)
        self.dip_slip = _assert_assign(attributes['Dip Slip'])
        self.strike_slip = _assert_assign(attributes['Strike-Slip'])
        self.vertical_slip = _assert_assign(attributes['Vertical'])
        self.net_slip = _assert_assign(attributes['Net Slip'])
        self.hv_ratio = _assert_assign(attributes['HV Ratio'])
        self.rake = _assert_assign(attributes['Rake'])
        self.slip_category = attributes['Slip Category']
        self.slip_type =_assert_assign(attributes['Slip Type'])
        self.aseismic =_assert_assign(attributes['Aseismic'])


class FaultTrace(object):
    """
    Class to hold simple trace data
    """
    def __init__(self, identifier, geometry, attributes):
        """
        """
        self.id = identifier
        assert isinstance(geometry, Line)
        self.geometry = geometry
        self.scale = attributes['Scale']
        self.accuracy = attributes['Accuracy']
        self.notes = attributes['Notes']
        self.name = attributes['Name']
        self.method = attributes['Location Method']
        self.expression = attributes['Geomorphic Expression']



class Displacement(object):
    """
    Simple class to gather displacement attributes
    """
    def __init__(self, attributes):
        """
        """
        self.total = attributes['Total']
        self.category = attributes['Category']
        self.horizontal = attributes['Horizontal']
        self.vertical = attributes['Vertical']
        self.net = attributes['Net']
        self.value = _assert_assign(attributes['Value'])


class BaseFault(object):
    """
    Base Class to hold fault attributes and methods common to both the
    neotectonic section and neotectonic fault classes
    """
    def __init__(identifier, name, attributes):
        """
        """
        self.id = identifier
        self.name = name
        self.geometry = None
        self.length = None
        self.is_episodic = attributes['Episodic']
        self.strike = attributes['Strike']
        self.surface_dip = attributes['Surface Dip']
        self.downside = attributes['Downthrown Side']
        self.upper_seismogenic_depth = _assert_assign(
            attributes['Upper Depth'])
        self.lower_seismogenic_depth = _assert_assign(
            attributes['Lower Depth'])
        self.dip = _assert_assign(attributes['Dip'])
        self.dip_direction = _assert_assign(attributes['Dip Direction'])
        self.dip_slip = _assert_assign(attributes['Dip Slip'])
        self.strike_slip = _assert_assign(attributes['Strike Slip'])
        self.vertical_slip = _assert_assign(attributes['Vertical Slip'])
        self.aspect = _assert_assign(attributes['HV Ratio'])
        self.slip = _assert_assign(attributes['Net Slip'])
        self.slip_category = attributes['Slip Category']
        self.rake = _assert_assign(attributes['Rake'])
        self.slip_type = _assert_assign(attributes['Slip Type'])
        self.aseismic = _assert_assign(attributes['Aseismic'])
        self.displacement = attributes['Displacement']
        # Recurrence Interval (Preferred, Min, Max, Category)
        self.recurrence = _assert_assign(attributes['Recurrence'])
        # Movement (Preferred, Min, Max, Category)
        self.movement = _assert_assign(attributes['Movement'])
        # Historical Event
        self.historic = attributes['Historical Event']
        self.prehistoric = attributes['Pre-historic']
        self.compiler = None
        self.contributor = None
        self.created = None
        self.comment = None


def NeotectonicSection(BaseFault):
    """
    Defines a neotectonic section

    """
    def __init__(self, identifier, name, attributes, geometry=None,
            slip_obs=None, event_list=None, trace_obs=None,
            disp_observation=None, geometry_obs=None):
        """
        """
        super(NeotectonicSection, self).__init__(identifier, name, attributes)
        self.geometry = geometry
        self.slip_observations = slip_obs
        self.event_list = event_list
        self.trace_observations = trace_obs
        self.displacement_observations = displacement_observations
        self.geometry_observations = geometry_obs


#    def get_slip_observations(self, slip_type='Net'):
#        """
#        Returns a numpy array of slip observations 
#        """
#        if (self.slip_observations is None) or not\
#            isinstance(self.slip_observations, list):
#            return None
#
#        slip_data = []
#        if slip_type == 'Net':
#            slip_data = [[val.location.longitude, val.location.latitude,
#                val.net_slip.minimum, val.net_slip.value, val.net_slip.maximum]
#                for val in self.slip_observations]
#        elif slip_type == 'Vertical':
#            slip_data = [[val.location.longitude, val.location.latitude,
#                val.vertical_slip.minimum, val.vertical_slip.value,
#                val.vertical_slip.maximum] for val in self.slip_observations]
#        elif slip_type == '':
#            slip_data = [[val.location.longitude, val.location.latitude,
#                val.vertical_slip.minimum, val.vertical_slip.value,
#                val.vertical_slip.maximum] for val in self.slip_observations]
#        else:
#            raise ValueError('Slip type not recognised')
#        return np.array(slip_data)


def NeotectonicFault(object):
    """

    """
    def __init__(self, identifier, name, sections, attributes=None):
        """
        """
        self.id = identifier
        self.name = name
        self.sections = sections
        if isinstance(dict, attributes):
            # Attributes defined for fault
            self.data = BaseFault(self.id, self.name, attributes)
        else:
            self.data = None
