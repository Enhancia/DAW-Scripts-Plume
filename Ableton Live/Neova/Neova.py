from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
try:
    from .TrackDetector import TrackDetector
except ImportError:
    from TrackDetector import TrackDetector


class Neova(ControlSurface):

	_track_detectors = []
	_current_track = None

	def __init__(self, c_instance):
		ControlSurface.__init__(self, c_instance)
		with self.component_guard():
			self.__c_instance = c_instance

		self._initialize_track_detectors()
		self._current_track = self.song().view.selected_track
		self._on_current_track_devices_changed.subject = self._current_track if self._current_track else None

		#self._show_tracks_description()
		#self._show_track_detectors()
		
	def _show_tracks_description(self):
		log_string = "\n[Current Tracks]\n"

		for track in self.song().tracks:
			log_string += ("   - " + str(track.name)
									  + (" |     Armed" if (track.arm == 1) else " | Not Armed")
									  + " | Devices : " + "-".join([device.name for device in track.devices])
									  + "\n")
		self.log_message (log_string)

	def _show_track_detectors(self):
		log_string = "\n[Current Detectors]\n"

		for detector in self._track_detectors:
			log_string += detector.to_string() + "\n"
		self.log_message (log_string)

	def _initialize_track_detectors(self):
		with self.component_guard():
			del self._track_detectors[:]
			for track in self.song().tracks:
				for device in track.devices:
					if device.name == "Plume":
						self._track_detectors.append (TrackDetector(track))

	def _update_track_detectors(self):
		with self.component_guard():
			self._remove_outdated_track_detectors()

			for track in self.song().tracks:
				self._update_arm_detector_for_track(track)

	def _track_has_plume(self, track_to_check):
		for device in track_to_check.devices:
			if device.name == "Plume":
				return True
		return False

	def _track_has_arm_detector(self, track_to_check):
		for detector in self._track_detectors:
			if detector.track == track_to_check:
				return True
		return False

	def _get_arm_detector_for_track(self, track_to_get_detector_for):
		for detector in self._track_detectors:
			if detector.track == track_to_get_detector_for:
				return detector
		return None

	def _get_arm_detector_id(self, track_to_get_detector_for):
		for id in range(len(self._track_detectors)):
			if self._track_detectors[id].track == track_to_get_detector_for:
				return id
		return -1 #default value

	def _update_arm_detector_for_track(self, track_to_update_detector_in):
		if ((not self._track_has_arm_detector(track_to_update_detector_in)) and self._track_has_plume(track_to_update_detector_in)):
			# New plume track needs a detector : appends detector to the list
			self._track_detectors.append (TrackDetector(track_to_update_detector_in))

		elif (self._track_has_arm_detector(track_to_update_detector_in) and (not self._track_has_plume(track_to_update_detector_in))):
			# Former plume track no longer needs a detector: removes its detector from the list
			id_to_remove = self._get_arm_detector_id(track_to_update_detector_in)
			if id_to_remove != -1:
				self._track_detectors[id_to_remove].unbind_from_track()
				del self._track_detectors[id_to_remove]

	def _remove_outdated_track_detectors(self):
		for detector in self._track_detectors:
			if not detector.track:
				self._track_detectors.remove (detector)

	def _on_track_list_changed(self):
		self._update_track_detectors()

	def _on_selected_track_changed(self):
		self._current_track = self.song().view.selected_track
		self._on_current_track_devices_changed.subject = self._current_track

		with self.component_guard():
			self._update_arm_detector_for_track(self._current_track)

	@subject_slot("devices")
	def _on_current_track_devices_changed(self):
		with self.component_guard():
			self._update_arm_detector_for_track(self._current_track)