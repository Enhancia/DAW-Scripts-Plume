from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
from _Framework import Task

NOT_ARMED = 0
ARMED = 1
UNKNOWN_ARM = 1

class TrackDetector(ControlSurfaceComponent):

	track = None
	device_name = None
	track_name = None

	def __init__(self, track, *a, **k):
		super(TrackDetector, self).__init__(*a, **k)
		self.track = track

		if self.track:
			assert self._track_has_plume(), "Track must use Plume as a Plugin"
			
			self.device_name = "-".join ([device.name for device in self.track.devices]) if self.track.devices else "None"
			self.track_name = self.track.name if self.track else "None"

			if self.track.can_be_armed:
				self._on_arm_changed.subject = self.track
				self._on_implicit_arm_changed.subject = self.track

				for device in self.track.devices:
					if device.name == "Plume":
						self._on_parameters_changed.subject = device

		self._on_arm_changed()
		self._display_plume_parameters()

	def disconnect(self):
		super(TrackDetector, self).disconnect()
		self.unbind_from_track()
		self.device_name = None
		self.track_name = None

	def unbind_from_track(self):
		self._on_arm_changed.subject = None
		self._on_implicit_arm_changed.subject = None
		self._on_parameters_changed.subject = None
		self.track = None
		self.device_name = "None"
		self.track_name = "None"


	def _track_has_plume(self):
		for device in self.track.devices:
			if device.name == "Plume":
				return True
		return False

	def _display_plume_parameters(self): # FOR DEBUG
		for device in self.track.devices:
			if device.name == "Plume":
				log_string = "Plume Parameters :\n"
				
				if device.parameters:
					for parameter in device.parameters:
						log_string += str(parameter.name) + " (" + str(parameter.value) + ")\n"
				else:
					log_string += "None"

				self.canonical_parent.log_message (log_string)
				return

	def _set_plume_armed_parameter_value(self, armed_value_to_set):
		assert self._track_has_plume(), "Track must use Plume as a Plugin"
		
		for device in self.track.devices:
			if device.name == "Plume":
				for parameter in device.parameters:
					if parameter.name == "track_arm":
						self._tasks.add(Task.run(self._change_parameter_value, parameter, armed_value_to_set))
						return

	def _get_plume_armed_parameter_value(self):
		assert self._track_has_plume(), "Track must use Plume as a Plugin"
		
		for device in self.track.devices:
			if device.name == "Plume":
				for parameter in device.parameters:
					if parameter.name == "track_arm":
						return parameter.value
		return -1

	def _change_parameter_value(self, parameter, armed_value_to_set):
		parameter.value = armed_value_to_set

	def to_string(self):
		if self.track:
			return "Arm Detector (" + str(id(self)) + ") | Track : " + str(self.track.name) + " (" + str(id(self.track)) + ") | Devices : " + "-".join([device.name for device in self.track.devices]) + " | Arm status : " + ("True" if self.track.arm else "False") + "\n"
		else:
			return "Unknown Detector (" + str (id(self)) + ")\n"

	@subject_slot ('arm')
	def _on_arm_changed(self):
		self.canonical_parent.log_message("\n[DETECTOR CALLBACK] ARM changed\n" + self.to_string())
		self._set_plume_armed_parameter_value(float (ARMED) if self.track.arm else float (NOT_ARMED))

	@subject_slot ('implicit_arm')
	def _on_implicit_arm_changed(self):
		self.canonical_parent.log_message("\n[DETECTOR CALLBACK] IMPLICIT ARM changed\n" + self.to_string())
		self._set_plume_armed_parameter_value(float (ARMED) if self.track.arm else float (NOT_ARMED))

	@subject_slot ('parameters')
	def _on_parameters_changed(self):
		self.canonical_parent.log_message("\n[DETECTOR CALLBACK] PARAMETERS changed\n" + self.to_string())
		parameter_value = self._get_plume_armed_parameter_value()
		
		if parameter_value != -1:
			self._set_plume_armed_parameter_value(float (ARMED) if self.track.arm else float (NOT_ARMED))