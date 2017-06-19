import argparse
import inspect
import json
import six
import sys


class Description(object):
    """
    This class provides convenient chainable semantics to allow
    functions to describe themselves for use with girder_worker. A
    function can apply the :py:class:`pysciencedock.describe.describe`
    decorator to itself (called with an instance of this class) in order to
    describe itself.
    """

    def __init__(self, name, description, dockerImage):
        self._name = name
        self._description = description
        self._dockerImage = dockerImage
        self._inputs = []
        self._outputs = []

    def asDict(self, name, pullImage=True):
        """
        Returns this description object as an appropriately formatted dict
        """

        spec = {
            'name': self._name,
            'description': self._description,
            'mode': 'docker',
        }

        arguments = [name]
        arguments += ['--%s=$input{%s}' % (x['id'], x['id']) for x in self._inputs]
        arguments += ['--%s=$output{%s}' % (x['id'], x['id']) for x in self._outputs]
        spec['container_args'] = arguments

        spec['docker_image'] = self._dockerImage
        spec['pull_image'] = pullImage

        inputs = []
        for inputSpec in self._inputs:
            specCopy = inputSpec.copy()
            if 'deserialize' in specCopy:
                del specCopy['deserialize']
            if inputSpec['type'] == 'file':
                specCopy['target'] = 'filepath'
            if 'default' in specCopy:
                specCopy['default'] = dict(data=specCopy['default'])
            inputs.append(specCopy)
        spec['inputs'] = inputs

        outputs = []
        for outputSpec in self._outputs:
            specCopy = outputSpec.copy()
            if 'serialize' in specCopy:
                del specCopy['serialize']
            if outputSpec['type'] == 'new-file':
                specCopy['target'] = 'filepath'
            outputs.append(specCopy)
        spec['outputs'] = outputs

        return spec


    def input(self, id, name, description='', required=True, type='string', **kwargs):
        """
        This helper will build an input declaration for you.
        :param id: name of the input.
        :param name: human-readable name of the input.
        :param description: explanation of the input.
        :param type: the girder_worker type expected in the input.
        :param deserialize: a function that takes a file name and returns an object
            ready to be sent to the function.
        :param required: True if the function will fail if this parameter is not
            present, False if the parameter is optional.
        :param values: a fixed list of possible values for the field.
        :type values: list
        :param strip: For string types, set this to True if the string should be
            stripped of white space.
        :type strip: bool
        :param lower: For string types, set this to True if the string should be
            converted to lowercase.
        :type lower: bool
        :param upper: For string types, set this to True if the string should be
            converted to uppercase.
        :type upper: bool
        """

        inputSpec = {
            'id': id,
            'name': name,
            'description': description,
            'required': required,
            'type': type
        }

        for key, val in six.iteritems(kwargs):
            inputSpec[key] = val

        self._inputs.append(inputSpec)
        return self

    def output(self, id, name, description='', type='string', serialize=None):
        """
        This helper will build an output declaration for you.
        :param id: the name of the output.
        :param name: a human-readable name of the output
        :param description: an explanation of the output.
        :param type: the girder_worker type expected in the output.
        :param serialize: a function that takes the function output and a file name
            and serializes the output to that file.
        """

        outputSpec = {
            'id': id,
            'name': name,
            'description': description,
            'type': type
        }

        if serialize is not None:
            outputSpec['serialize'] = serialize

        self._outputs.append(outputSpec)
        return self

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs


class describe(object):  # noqa: class name
    def __init__(self, description):
        """
        This returns a decorator to set the API documentation on a route
        handler. Pass the Description object (or None) that you want to use to
        describe this route. It should be used like the following example:
            @describe(
                Description('Do something')
               .input('foo', 'Some parameter', ...)
            )
            def myFunction(...)
        :param description: The description for the route.
        :type description: :py:class:`girder.api.describe.Description` or None

        Like describeRoute, but this decorator also controls behavior of the
        underlying method. It handles parameter validation and transformation
        based on the Description object passed.
        :param description: The description object.
        :type description: Description
        """
        self.description = description

    def __call__(self, fun):
        @six.wraps(fun)
        def wrapped(*args, **kwargs):
            """
            Transform any passed params according to the spec, or
            fill in default values for any params not passed.
            """

            mode = kwargs.get('_mode')
            if mode == 'cli':
                args = kwargs.get('args', sys.argv[1:])
                if len(args) == 1 and args[0] == '--json':
                    json.dump(self.description.asDict(fun.__name__), sys.stdout, indent=2)
                    sys.stdout.write('\n')
                    return
                parser = argparse.ArgumentParser(
                    prog=fun.__name__, description=self.description.name + '\n' + self.description.description)
                for descInput in self.description.inputs:
                    parser.add_argument('--' + descInput['id'],
                        help=descInput.get('name', descInput['id'] + '. ' + descInput['description']),
                        required=descInput.get('required', False),
                        default=descInput.get('default', None)
                    )
                for descOutput in self.description.outputs:
                    parser.add_argument('--' + descOutput['id'],
                        help=descOutput.get('name', descOutput['id'] + '. ' + descOutput['description']),
                        required=False
                    )
                kwargs = {}
                cliParams = {k: v for k, v in six.iteritems(vars(parser.parse_args(args))) if v != None}
                for descInput in self.description.inputs:
                    inputId = descInput['id']
                    inputType = descInput['type']
                    if inputId in cliParams:
                        if inputType == 'file' and 'deserialize' in descInput:
                            kwargs[inputId] = descInput['deserialize'](cliParams[inputId])
                        else:
                            kwargs[inputId] = cliParams[inputId]
            elif mode == 'json':
                return self.description.asDict(fun.__name__)
            else:
                # Roll positional args into kwargs
                argNames = inspect.getargspec(fun).args
                for arg in range(len(args)):
                    kwargs[argNames[arg]] = args[arg]

            for descInput in self.description.inputs:
                id = descInput['id']
                if id in kwargs:
                    kwargs[id] = self._validateInput(id, descInput, kwargs[id])
                elif 'default' in descInput:
                    kwargs[id] = descInput['default']
                elif descInput['required']:
                    raise Exception('Input "%s" is required.' % id)
                else:
                    # If required=False but no default is specified, use None
                    kwargs[id] = None

            result = fun(**kwargs)

            if mode == 'cli':
                if len(self.description.outputs) == 0:
                    return
                if len(self.description.outputs) == 1:
                    result = {self.description.outputs[0]['id']: result}
                for outputDesc in self.description.outputs:
                    outputId = outputDesc['id']
                    outputType = outputDesc['type']
                    if outputId in result:
                        if outputType == 'new-file':
                            if outputId in cliParams:
                                fileName = cliParams[outputId]
                            else:
                                fileName = descOutput.get('path', outputId)
                            if 'serialize' in outputDesc:
                                outputDesc['serialize'](result[outputId], fileName)
                            result[outputId] = fileName
                json.dump(result, sys.stdout, indent=2)
                sys.stdout.write('\n')
                return

            return result

        wrapped.description = self.description
        return wrapped

    def _handleString(self, name, descInput, value):
        if descInput['_strip']:
            value = value.strip()
        if descInput['_lower']:
            value = value.lower()
        if descInput['_upper']:
            value = value.upper()

        format = descInput.get('format')
        if format in ('date', 'date-time'):
            try:
                value = dateutil.parser.parse(value)
            except ValueError:
                raise Exception('Invalid date format for parameter %s: %s.' % (name, value))

            if format == 'date':
                value = value.date()

        return value

    def _handleInt(self, name, descInput, value):
        try:
            return int(value)
        except ValueError:
            raise Exception('Invalid value for integer parameter %s: %s.' % (name, value))

    def _handleNumber(self, name, descInput, value):
        try:
            return float(value)
        except ValueError:
            raise Exception('Invalid value for numeric parameter %s: %s.' % (name, value))

    def _validateInput(self, name, descInput, value):
        """
        Validates and transforms a single parameter that was passed. Raises
        RestException if the passed value is invalid.
        :param name: The name of the param.
        :type name: str
        :param descInput: The formal parameter in the Description.
        :type descInput: dict
        :param value: The value passed in for this param for the current request.
        :returns: The value transformed
        """
        type = descInput.get('type')

        # Coerce to the correct data type
        if type == 'string':
            value = self._handleString(name, descInput, value)
        elif type == 'boolean':
            value = toBool(value)
        elif type == 'integer':
            value = self._handleInt(name, descInput, value)
        elif type == 'number':
            value = self._handleNumber(name, descInput, value)

        # Enum validation (should be afer type coercion)
        if 'values' in descInput and value not in descInput['values']:
            raise Exception('Invalid value for %s: "%s". Allowed values: %s.' % (
                name, value, ', '.join(descInput['values'])))

        return value
