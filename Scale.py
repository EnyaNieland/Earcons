class Scale(object):
    major = [0, 2, 4, 5, 7, 9, 11, 12]
    minor = [0, 2, 3, 5, 7, 8, 10, 12]
    scales = [major, minor]

    def __init__(self, degree, octave, type):
        self.degree = self.determine_degree(degree, octave)
        self.scale = self.create_scale(self.scales[type])

    def determine_degree(self, degree, octave):
        octave *= 12 # octave contains 12 keys
        return degree + octave

    def create_scale(self, scale):
        new_scale = []
        for val in scale:
            new_scale.append(self.degree + val)
        return new_scale
