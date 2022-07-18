from typing import Dict

from src.gsop.values.terminology.attribute import AttributeEnum


class ArtifactAttrs:
    """
    A class which is used to hold stats for an artifact.
    It can hold sub-stats information, as well as providing them.
    """

    def __init__(self):
        """
        Initializes an empty class
        """
        self._attrs: Dict[AttributeEnum, float] = {}

    def set(self, attrs: Dict[AttributeEnum, float]):
        """
        Sets the class dictionary to a copy of `attrs`.
        The "scale of stat" refers to 0.7/0.8/0.9/1.0, the ratio of possible artifact sub-stat value.

        :param attrs: Dict[attribute, scale_of_stat]
        :return: self
        """
        self._attrs = attrs.copy()
        return self

    def add(self, attr: AttributeEnum, scale: float = 1) -> None:
        """
        Adds the `scale` to the `attr`, if `attr` is not one of the sub-stats yet, it will be added.
        """
        self._attrs[attr] = self._attrs.setdefault(attr, 0) + scale

    def remove(self, attr: AttributeEnum) -> None:
        """
        Removes an `attr` from the sub-stats.
        """
        self._attrs.pop(attr, None)

    def force_update(self, attr: AttributeEnum, scale: float) -> None:
        """
        Sets the scale of `attr` to `scale` unconditionally.
        """
        self._attrs[attr] = scale

    def num_of_attrs(self) -> int:
        """
        :return: number of attributes the artifact has.
        """
        return len(self._attrs)

    def attrs(self):
        """
        :return: the attributes the artifact has.
        """
        return self._attrs.keys()

    def has_attr(self, attr: AttributeEnum) -> bool:
        return attr in self._attrs

    def get_scale(self, attr: AttributeEnum) -> float:
        return self._attrs[attr]

    def get_absolute_value(self, attr: AttributeEnum) -> float:
        """
        :return: the actual value of the sub-stat that will be shown on an artifact.
                 Returns -1 if the attribute cannot be a sub-stat for some reason.
        """
        val = attr.substat_max_val()
        if val == -1:
            return -1
        return self.get_scale(attr) * val

    def get_read_only(self) -> Dict[AttributeEnum, float]:
        """
        :return: the attributes field of the class, passed by reference.
                 DO NOT USE THIS METHOD UNLESS YOU KNOW WHAT YOU ARE DOING!
        """
        return self._attrs


class Artifact:
    """
    The class for an artifact.
    """

    def __init__(self):
        self._level = 0
        self._attrs = ArtifactAttrs()
        self._set = None
        self._mainstat = None
