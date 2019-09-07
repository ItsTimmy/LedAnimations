import time
from enum import Enum
import json

animation_classes = []

def animation(animation_display_name, animation_description):
    def animation(animation_class):

        animate_fn = getattr(animation_class, 'animate', None)
        if not callable(animate_fn):
            raise Exception("When using the @animation decorator, you must define an animate function.")

        params = {}

        for name in dir(animation_class):
            if not name.startswith("__"):
                obj = getattr(animation_class, name)
                if type(obj) == AnimationParameter:
                    params[name] = obj

        print(params)

        class NewAnimation:

            parameters = params
            display_name = animation_display_name
            name = animation_class.__name__
            description = animation_description
            metadata = {
                'name': name,
                'displayname': display_name,
                'description': description,
                'parameters': {
                    name: param.as_dict() for name, param in parameters.items()
                }
            }

            def __init__(self, *args, **kwargs):
                self.id = kwargs['id']
                del kwargs['id']
                print("My kwargs are: {}".format(kwargs))
                # Validate parameters
                for param_name, param_metadata in NewAnimation.parameters.items():
                    if param_name not in kwargs:
                        kwargs[param_name] = None
                    kwargs[param_name] = param_metadata.validate(kwargs[param_name])

                self.instance = animation_class(*args, **kwargs)
                self.total_time = 0


            def time_animation(self, *args, **kwargs):
                start = time.time()
                retval = self.instance.animate(*args, **kwargs)
                end = time.time()
                self.total_time += (end - start)
                return retval

            def as_dict(self):
                return {
                    'name': NewAnimation.name,
                    'display_name': NewAnimation.display_name,
                    'description': NewAnimation.description,
                    'parameters': {
                        name: getattr(self.instance, name) for name in NewAnimation.parameters.keys()
                    }
                }

            def __getattribute__(self, s):
                """
                Passthrough for all other attributes. If the attribute is found in this NewAnimation class,
                it is returned. Otherwise, the attribute is returned from the original class.
                """
                try:
                    return super(NewAnimation, self).__getattribute__(s)
                except AttributeError:
                    pass

                if s == 'animate':
                    return self.time_animation
                else:
                    return self.instance.__getattribute__(s)

        animation_classes.append(NewAnimation)
        return NewAnimation
    return animation


class ParameterError(Exception):
    pass


class ParameterType(Enum):
    """
    INTEGER: A single integer
    FLOAT: A floating point number
    COLOR: A tuple of 3 floats in range [0, 1]
    POSITION: An integer position on the strand
    STRING: A string
    """
    INTEGER = 1,
    FLOAT = 2,
    COLOR = 3,
    POSITION = 4,
    STRING = 5


class AnimationParameter:

    def __init__(
            self,
            displayname: str,
            param_type: ParameterType,
            description: str = None,
            default=None,
            optional: bool = False,
            advanced: bool = False,
            minimum=None,
            maximum=None
    ):
        """
        :param displayname: String that will be shown to the user on the UI
        :param description: Description of what this parameter does. (Optional)
        :param param_type: String that contains either 'integer', 'float', 'color', or 'string'.
        :param default: Default value that will be pre-populated on the UI
        :param optional: Boolean for whether this parameter is mandatory
        :param advanced: Boolean for whether this parameter should be hidden away in an "Advanced" dropdown on the UI
        :param minimum: Minimum value of this parameter. This only applies if 'type' is 'integer' or 'float'
        :param maximum: Maximum value of this parameter. This only applies if 'type' is 'integer' or 'float'
        """
        self.description = description
        self.displayname = displayname
        self.param_type = param_type
        self.default = default
        self.optional = optional
        self.advanced = advanced
        self.minimum = minimum
        self.maximum = maximum

    def __repr__(self):
        return repr(self.as_dict())

    def as_dict(self):
        return {
            'description': self.description,
            'displayname': self.displayname,
            'type': self.param_type.name,
            'default': self.default,
            'optional': self.optional,
            'advanced': self.advanced,
            'minimum': self.minimum,
            'maximum': self.maximum
        }

    def validate(self, value):
        print("Validating {}: {}".format(self.displayname, value))
        # Get default value
        if value is None:
            if not self.optional:
                raise ParameterError("'{}' is a required parameter, but was not provided.".format(
                    self.displayname
                ))
            else:
                value = self.default

        # Validate type
        if self.param_type == ParameterType.INTEGER or self.param_type == ParameterType.POSITION:
            # TODO: Treat POSITION parameters special
            try:
                valid = int(value) == value
                value = int(value)
            except ValueError:
                valid = False
            if not valid:
                raise ParameterError("'{}' should be a whole number, but you gave {}.".format(
                    self.displayname, value
                ))
        elif self.param_type == ParameterType.FLOAT:
            try:
                value = float(value)
            except ValueError:
                raise ParameterError("'{}' should be a number, but you gave {}.".format(
                    self.displayname, value
                ))
        elif self.param_type == ParameterType.COLOR:
            if len(value) != 3:
                raise ParameterError("'{}' should be a tuple of 3 integers, but you gave {}.".format(
                    self.displayname, value
                ))
            try:
                value = tuple(int(x) / 255 for x in value)
            except ValueError:
                raise ParameterError("'{}' should be a tuple of 3 integers, but you gave {}.".format(
                    self.displayname, value
                ))

        # Validate minimum and maximum
        if self.minimum is not None and value < self.minimum:
            raise ParameterError("For '{}', you gave {}, but the minimum allowable value is {}".format(
                self.displayname, value, self.minimum
            ))

        if self.maximum is not None and value > self.maximum:
            raise ParameterError("For '{}', you gave {}, but the maximum allowable value is {}".format(
                self.displayname, value, self.maximum
            ))

        return value