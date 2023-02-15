# README.md

## Define a MQTT Topic

1. Define Topic using a combination of paramater definitions and regular string values.

    ```
    /api/<env>/<version>/<destination>/<gateway>/<command>
    ```

    - api
    - <env>
    - <version>
    - <destination>
    - <id>
    - <command>

1. Define each paramater, their datatype, and the possibe values they can be.

    - <env>
        - datatype is string
        - possible values are qa, dev, prod
    - <version>
        - datatype is string
        - possible values are v1
    - <version>
        - datatype is string
        - possible values are backend, gateway
    - <id>
        - datatype is string
    - <command>
        - datatype is string

## Datatypes

The following datatyoes are supported:

- string
- int
- date
- boolean
- lookup

### String

Any character is accepted.

### Int

An intger value.

### Number

A integer, floating point, NaN, Inf

### Date

Any date, time or date time value.

### Boolean

Excepts True, False, true, false, T, F, t, f, 1, 0, Yes, No

### Lookup

Allows a list of comma seperated values.

- lookup

    1. Examples
        - <env:lookup=(env,qa,prod)`>
        - <destination:lookup=(back,front,middle)>

### Parameter Modifiers

See if I can pass a nested Python dictionary.

1. First Trial
```Python
settings = {
    'env': {
        'type': 'string',
        'lookup': ['qa'],
        'comment': 'Only qa is running on the AWS sewrvers.'
    },
    'channel': {
        'type': 'string',
        'lookup': ['backend', 'gateway'],
    },
    'version': {
        'type': 'string'
    },
    'id': {
        'type': 'string',
        'regex': '([0-9]{4})[-]([0-9]{4})[-][0-9]{4}'
    }
}
router = Router()
router.add('/<env>/<channel>/<version>/<id>/<command>', settings)


```