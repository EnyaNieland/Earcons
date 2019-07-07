import rtmidi
import time


class MidiPlayer(object):
    note_on_event = 0x90
    note_off_event = 0x80
    finished_playing_motive = False

    def __init__(self):
        self.midiout = rtmidi.MidiOut()
        available_ports = self.midiout.get_ports()

        if available_ports:
            self.midiout.open_port(0)
        else:
            self.midiout.open_virtual_port("MIDI output")

    # def play_scale(self, scale, duration_seconds=1, velocity=127):
    #     if self.__can_play__():
    #         for note in scale:
    #             self.__play_note__(note, velocity)
    #             time.sleep(duration_seconds)
    #             self.__stop_note__(note)

    def play_motive(self, motive, velocity=127):
        # TODO: motive should contain frequency and duration, now only contains frequencies
        if self.__can_play__():
            for note in motive:
                print(note)
                self.__play_note__(note["frequency"], velocity)
                time.sleep(note["duration"])
                self.__stop_note__(note["frequency"])
            self.finished_playing_motive = True

    def __can_play__(self):
        return self.midiout.is_port_open()

    def __play_note__(self, note, velocity):
        self.midiout.send_message([self.note_on_event, note, velocity])

    def __stop_note__(self, note):
        self.midiout.send_message([self.note_off_event, note, 0])

    def __del__(self):
        del self.midiout
