import Scale
import Mapper


class Earcon(object):
    mapper = Mapper.Mapper()

    def __init__(self, mapped_values):
        scale = self.retrieve_scale()
        self.earcon = self.create_motive(scale, mapped_values)

    def retrieve_scale(self):
        scale = Scale.Scale(self.mapper.degree, self.mapper.octave, self.mapper.type).scale
        return scale

    def create_motive(self, scale, mapped_values):

        for item in mapped_values:
            for key, value in item.items():
                if key == "frequency":
                    if value is not None:
                        new_value = scale[value]
                    else:
                        new_value = scale[0]
                else:
                    if value is not None:
                        new_value = self.mapper.durations[value]
                    else:
                        new_value = self.mapper.durations[-1]

                item[key] = new_value

        return mapped_values
