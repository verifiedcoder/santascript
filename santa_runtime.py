# santa_runtime.py
import asyncio
from collections import deque
import random
import functools
import math


class SantaRuntime:
    def __init__(self):
        self.output = []
        self.variables = {}  # Initialize variables dictionary

    def nice_list_decorator(self, workshop):
        if workshop[0] != 'workshop':
            raise ValueError("❌ Ho ho NO! Can only decorate workshops!")

        name = workshop[1]
        params = workshop[2]
        ret_type = workshop[3]
        body = workshop[4]

        def wrapper(*args):
            if not all(isinstance(arg, (int, float)) and arg >= 0 for arg in args):
                raise ValueError("❌ Ho ho NO! Only positive values allowed on the nice list!")
            return self.execute_workshop_call(name, args)

        self.workshops[name] = {
            'params': params,
            'return_type': ret_type,
            'body': body,
            'wrapper': wrapper
        }
        return ('workshop', name, params, ret_type, body)

    def execute(self, ast):
        if not isinstance(ast, list):
            ast = [ast]
        for node in ast:
            if isinstance(node, tuple):
                node_type = node[0]
                if node_type == 'deliver':
                    value = self.evaluate(node[1])
                    if value is not None:
                        self.output.append(str(value))
        return self.output

    def execute_statement(self, statement):
        try:
            if statement[0] == 'try_catch':
                _, try_block, catch_block = statement
                try:
                    for stmt in try_block:
                        self.execute_statement(stmt)
                except Exception as e:
                    for stmt in catch_block:
                        self.execute_statement(stmt)

                stmt_type = statement[0]

                if stmt_type == 'workshop':
                    name, params, ret_type, body = statement[1:]
                    self.workshops[name] = {
                        'params': params,
                        'return_type': ret_type,
                        'body': body,
                        'name': name
                    }
                    return

                elif stmt_type == 'declare':
                    _, name, var_type = statement
                    self.variables[name] = {
                        'type': var_type,
                        'value': self.get_default_value(var_type)
                    }

                elif stmt_type == 'declare_quantum':
                    _, name, base_type = statement
                    self.variables[name] = {
                        'type': f'QUANTUM_GIFT<{base_type}>',
                        'value': None,
                        'superposition': True
                    }

                elif stmt_type == 'declare_typed_array':
                    _, name, element_type = statement
                    self.variables[name] = {
                        'type': f'GIFT<{element_type}>',
                        'value': [],
                        'element_type': element_type
                    }

                elif stmt_type == 'assign':
                    _, name, value = statement
                    if name not in self.variables:
                        raise NameError(f"❌ Ho ho NO! Variable '{name}' not declared!")

                    evaluated_value = self.evaluate(value)
                    var_type = self.variables[name]['type']

                    # Handle quantum types first
                    if var_type.startswith('QUANTUM_GIFT<'):
                        self.variables[name]['value'] = evaluated_value
                        self.variables[name]['superposition'] = True
                        return

                    # Handle chainable method results
                    if isinstance(evaluated_value, dict) and 'type' in evaluated_value:
                        if self.type_check(evaluated_value['value'], var_type):
                            self.variables[name]['value'] = evaluated_value['value']
                            return

                    # Then handle typed arrays
                    if var_type.startswith('GIFT<'):
                        element_type = self.variables[name]['element_type']
                        if isinstance(evaluated_value, list):
                            if not all(self.type_check(item, element_type) for item in evaluated_value):
                                raise TypeError(f"❌ Ho ho NO! Array elements must be of type {element_type}")
                        else:
                            raise TypeError("❌ Ho ho NO! Value must be an array!")

                    if self.type_check(evaluated_value, var_type):
                        self.variables[name]['value'] = evaluated_value
                    else:
                        raise TypeError(f"❌ Ho ho NO! Type mismatch for {name}")

                elif stmt_type == 'deliver':
                    _, value = statement
                    result = self.evaluate(value)
                    self.output.append(str(result))

                elif stmt_type == 'if':
                    _, condition, true_block, false_block = statement
                    if self.evaluate(condition):
                        for stmt in true_block:
                            self.execute_statement(stmt)
                    else:
                        for stmt in false_block:
                            self.execute_statement(stmt)

                elif stmt_type == 'while':
                    _, condition, block = statement
                    while self.evaluate(condition):
                        for stmt in block:
                            self.execute_statement(stmt)

                elif stmt_type == 'foreach':
                    _, var_name, iterable, block = statement
                    iterable_value = self.evaluate(iterable)
                    for item in iterable_value:
                        self.variables[var_name] = {'type': 'TINSEL', 'value': item}
                        for stmt in block:
                            self.execute_statement(stmt)

                elif stmt_type == 'count':
                    _, count, block = statement
                    count_val = self.evaluate(count)
                    for _ in range(count_val):
                        for stmt in block:
                            self.execute_statement(stmt)

                if statement[0] == 'workshop':
                    name, params, ret_type, body = statement[1:]
                    self.workshops[name] = {
                        'params': params,
                        'return_type': ret_type,
                        'body': body,
                        'name': name  # Add name to help with error messages
                    }

                elif stmt_type == 'magic_workshop':
                    name, params, body = statement[1:]
                    self.workshops[name] = {
                        'params': params,
                        'body': body,
                        'is_magic': True
                    }

                elif stmt_type == 'try_catch':
                    _, try_block, catch_block = statement
                    try:
                        for stmt in try_block:
                            self.execute_statement(stmt)
                    except Exception:
                        for stmt in catch_block:
                            self.execute_statement(stmt)

                elif stmt_type == 'decorator':
                    _, decorator_name, workshop = statement
                    if decorator_name in self.decorators:
                        decorated_workshop = self.decorators[decorator_name](workshop)
                        self.execute_statement(decorated_workshop)
                    else:
                        raise NameError(f"❌ Ho ho NO! Decorator '{decorator_name}' not found!")

                elif stmt_type == 'await':
                    _, promise = statement
                    self.loop.run_until_complete(asyncio.sleep(1))  # Simulate waiting

                elif stmt_type == 'lambda':
                    return  # Lambda definitions don't need immediate execution

                elif stmt_type == 'nested_conditional':
                    _, conditions, blocks = statement
                    current_block = 0
                    for condition in conditions:
                        if self.evaluate(condition):
                            for stmt in blocks[current_block]:
                                self.execute_statement(stmt)
                            break
                        current_block += 1
                    if current_block >= len(blocks):
                        for stmt in blocks[-1]:  # Execute else block
                            self.execute_statement(stmt)
        except Exception as e:
            if isinstance(e, (ValueError, ZeroDivisionError, TypeError)):
                raise
            print(f"❌ Ho ho NO! {str(e)}")

    def type_check(self, value, expected_type):
        if isinstance(expected_type, str):
            if expected_type.startswith('GIFT<'):
                element_type = expected_type[5:-1]
                if not isinstance(value, list):
                    return False
                return all(self.type_check(item, element_type) for item in value)

            if expected_type.startswith('QUANTUM_GIFT<'):
                base_type = expected_type[13:-1]
                return self.type_check(value, base_type)

        type_checks = {
            'MERRY': lambda x: isinstance(x, (int, float)),
            'JINGLE': lambda x: isinstance(x, bool),
            'SPARKLE': lambda x: isinstance(x, float),
            'TINSEL': lambda x: isinstance(x, str),
            'GIFT': lambda x: isinstance(x, (list, str, dict)),
            'SLEIGH': lambda x: isinstance(x, dict),
            'STOCKING': lambda x: isinstance(x, (list, deque)),
            'SPIRIT': lambda x: isinstance(x, (int, float)) and 0 <= x <= 100,
            'SNOWFLAKE': lambda x: True
        }

        checker = type_checks.get(expected_type)
        return checker(value) if checker else True

    def execute_method_call(self, obj_name, method_name, args):
        if isinstance(obj_name, tuple) and obj_name[0] == 'method_result':
            # Handle chained method calls
            intermediate_result = self.execute_method_call(obj_name[1][1], obj_name[1][2], obj_name[1][3])
            if isinstance(intermediate_result, dict) and 'type' in intermediate_result:
                return self._execute_single_method_call(intermediate_result['value'], method_name, args)
            return self._execute_single_method_call(intermediate_result, method_name, args)
        elif isinstance(obj_name, str):
            if obj_name not in self.variables:
                raise NameError(f"❌ Ho ho NO! Object '{obj_name}' not found!")
            var = self.variables[obj_name]
            if 'superposition' in var and var['superposition']:
                if method_name == 'MEASURE':
                    return var['value']
            value = var['value']
            result = self._execute_single_method_call(value, method_name, args)
            return result
        else:
            raise ValueError("❌ Ho ho NO! Invalid method call!")

    def _execute_single_method_call(self, obj, method_name, args):
        evaluated_args = [self.evaluate(arg) for arg in args]
        obj_type = self.get_type(obj)

        if isinstance(obj, dict) and 'type' in obj:
            obj_type = obj['type']
            obj = obj['value']

        method_handlers = {
            'TINSEL': {
                'SPARKLE': lambda s, *_: {'type': 'TINSEL', 'value': f'✨{s}✨'},
                'WRAP_TEXT': lambda s, *_: {'type': 'TINSEL', 'value': s.title()},  # Changed from WRAP
                'UNTANGLE': lambda s, *_: {'type': 'TINSEL', 'value': s.strip()},
                'COUNT_JOYS': lambda s, *_: len(s),
                'TRIM_TREE': lambda s, *_: {'type': 'TINSEL', 'value': s.strip()},
                'JINGLE_CASE': lambda s, *_: {'type': 'TINSEL', 'value': s.upper()},
                'SILENT_NIGHT': lambda s, *_: {'type': 'TINSEL', 'value': s.lower()},
                'GIFT_WRAP': lambda s, n, *_: {'type': 'TINSEL', 'value': s.center(n)},
                'FIND_CHIMNEY': lambda s, sub, *_: s.find(sub),
                'REPLACE_COAL': lambda s, old, new, *_: {'type': 'TINSEL', 'value': s.replace(old, new)}
            },
            'GIFT': {
                'PACK': lambda lst, x, *_: lst.append(x) or lst,
                'UNWRAP': lambda lst, *_: lst.pop() if lst else None,
                'PEEK_INSIDE': lambda lst, *_: lst[-1] if lst else None,
                'COUNT_JOYS': lambda lst, *_: len(lst)
            },
            'STOCKING': {
                'PACK': lambda lst, x, *_: lst.append(x) or lst,
                'PEEK_INSIDE': lambda lst, *_: lst[-1] if lst else None,
                'UNWRAP': lambda lst, *_: lst.pop() if lst else None
            },
            'MERRY': {
                'TO_TINSEL': lambda x, *_: str(x),
                'TO_JINGLE': lambda x, *_: bool(x),
                'MORE_FESTIVE': lambda x, y, *_: x > y
            },
            'SPIRIT': {
                'TO_TINSEL': lambda x, *_: str(x),
                'TO_JINGLE': lambda x, *_: bool(x)
            }
        }

        # Add quantum type handlers dynamically
        for base_type in ['TINSEL', 'MERRY']:
            method_handlers[f'QUANTUM_GIFT<{base_type}>'] = {
                'MEASURE': lambda x, *_: x
            }

        if obj_type in method_handlers and method_name in method_handlers[obj_type]:
            result = method_handlers[obj_type][method_name](obj, *evaluated_args)
            if isinstance(result, dict) and 'type' in result:
                return result
            if method_name in ['TRIM_TREE', 'JINGLE_CASE', 'SILENT_NIGHT', 'GIFT_WRAP', 'SPARKLE', 'WRAP',
                               'WRAP_STRING']:
                return {'type': 'TINSEL', 'value': result}
            return result

        raise ValueError(f"❌ Ho ho NO! Unknown method '{method_name}' for type {obj_type}")

    def get_type(self, value):
        if isinstance(value, dict) and 'type' in value:
            return value['type']  # Handle quantum types
        if isinstance(value, str):
            return 'TINSEL'
        elif isinstance(value, (int, float)):
            return 'MERRY'
        elif isinstance(value, bool):
            return 'JINGLE'
        elif isinstance(value, list):
            return 'GIFT'
        elif isinstance(value, dict):
            return 'SLEIGH'
        elif isinstance(value, deque):
            return 'STOCKING'
        return 'SNOWFLAKE'

    def evaluate(self, expression):
        if not isinstance(expression, tuple):
            return expression

        expr_type = expression[0]

        if expr_type == 'value':
            value = expression[1]
            if isinstance(value, str) and value in self.variables:
                return self.variables[value]['value']
            return value

        elif expr_type == 'arithmetic':
            op = expression[1]
            left = self.evaluate(expression[2])
            right = self.evaluate(expression[3])
            operators = {
                'GIVE': lambda x, y: x + y,
                'TAKE': lambda x, y: x - y,
                'MULTIPLY_JOY': lambda x, y: x * y,
                'SHARE': lambda x, y: x / y if y != 0 else float('inf'),  # Handle division by zero
                'LEFTOVER_MAGIC': lambda x, y: x % y if y != 0 else float('inf'),
                'POWER_OF_BELIEF': lambda x, y: x ** y,
                'FLOOR_CHIMNEY': lambda x, y: x // y if y != 0 else float('inf'),
                'ROUND_PRESENTS': lambda x, y: round(x, int(y)),
                'MIN_GIFT': lambda x, y: min(x, y),
                'MAX_GIFT': lambda x, y: max(x, y)
            }
            try:
                return operators[op](left, right)
            except ZeroDivisionError:
                raise ValueError("Cannot divide by zero!")

        elif expr_type == 'comparison':
            op = expression[1]
            left = self.evaluate(expression[2])
            right = self.evaluate(expression[3])

            operators = {
                'MORE_FESTIVE': lambda x, y: x > y,
                'LESS_FESTIVE': lambda x, y: x < y,
                'SAME_GIFT': lambda x, y: x == y
            }
            return operators[op](left, right)

        elif expr_type == 'array':
            return [self.evaluate(item) for item in expression[1]]

        elif expr_type == 'dictionary':
            return {key: self.evaluate(value) for key, value in expression[1]}

        elif expr_type == 'dictionary_access':
            _, dict_name, key = expression
            dict_obj = self.variables[dict_name]['value']
            key_value = self.evaluate(key)
            return dict_obj[key_value]

        elif expr_type == 'boolean':
            return expression[1]

        elif expr_type == 'method_call':
            _, obj_name, method_name, args = expression
            return self.execute_method_call(obj_name, method_name, args)

        elif expr_type == 'function_call':
            name, args = expression[1:]
            return self.execute_workshop_call(name, args)

        elif expr_type == 'lambda':
            param, body = expression[1:]
            return lambda x: self.evaluate_with_context({param: {'type': 'MERRY', 'value': x}}, body)

        return None

    def get_default_value(self, var_type):
        if var_type.startswith('GIFT<'):
            return []
        elif var_type == 'STOCKING':
            return deque()

        defaults = {
            'MERRY': 0,
            'JINGLE': False,
            'SPARKLE': 0.0,
            'TINSEL': "",
            'GIFT': [],
            'SNOWFLAKE': None,
            'SPIRIT': 0,
            'SLEIGH': {},
            'STOCKING': deque()
        }
        return defaults.get(var_type, None)

    def convert_type(self, value, conversion):
        conversions = {
            'TO_TINSEL': str,
            'TO_JINGLE': bool
        }
        return conversions[conversion](value)

    def cleanup(self):
        pass

    def get_variable(self, name):
        if name not in self.variables:
            raise NameError(f"Variable '{name}' not found!")
        return self.variables[name]['value']

    def set_variable(self, name, value):
        if name not in self.variables:
            raise NameError(f"❌ Ho ho NO! Variable '{name}' not declared!")
        if not self.type_check(value, self.variables[name]['type']):
            raise TypeError(f"❌ Ho ho NO! Type mismatch for {name}")
        self.variables[name]['value'] = value

    def execute_workshop_call(self, name, args):
        if isinstance(name, str) and '.' in name:  # Handle function composition
            functions = name.split('.')
            result = None
            current_args = args

            for func in functions:
                if func not in self.workshops:
                    raise NameError(f"Workshop '{func}' not found!")

                if result is not None:
                    current_args = [result]

                result = self._execute_single_workshop(func, current_args)

            return result

        return self._execute_single_workshop(name, args)

    def _execute_single_workshop(self, name, args):
        if name not in self.workshops:
            raise NameError(f"❌ Ho ho NO! Workshop '{name}' not found!")

        workshop = self.workshops[name]
        if workshop.get('is_magic'):
            return self.execute_magic_workshop(workshop, args)

        if 'wrapper' in workshop:
            return workshop['wrapper'](*[self.evaluate(arg) for arg in args])

        evaluated_args = [self.evaluate(arg) for arg in args]
        param_vars = {}

        for (param_type, param_name), arg_value in zip(workshop['params'], evaluated_args):
            if not self.type_check(arg_value, param_type):
                raise TypeError(f"❌ Ho ho NO! Parameter type mismatch for {param_name}")
            param_vars[param_name] = {'type': param_type, 'value': arg_value}

        old_vars = self.variables.copy()
        self.variables.update(param_vars)

        result = None
        for stmt in workshop['body']:
            if stmt[0] == 'deliver':
                result = self.evaluate(stmt[1])
                break
            self.execute_statement(stmt)

        self.variables = old_vars
        return result

    def execute_magic_workshop(self, workshop, args):
        async def run_magic():
            evaluated_args = [self.evaluate(arg) for arg in args]
            param_vars = {}

            for (param_type, param_name), arg_value in zip(workshop['params'], evaluated_args):
                if not self.type_check(arg_value, param_type):
                    raise TypeError(f"❌ Ho ho NO! Parameter type mismatch for {param_name}")
                param_vars[param_name] = {'type': param_type, 'value': arg_value}

            old_vars = self.variables.copy()
            self.variables.update(param_vars)

            result = None
            for stmt in workshop['body']:
                if stmt[0] == 'await':
                    await asyncio.sleep(1)  # Simulated delay
                elif stmt[0] == 'deliver':
                    result = self.evaluate(stmt[1])
                    break
                else:
                    self.execute_statement(stmt)

            self.variables = old_vars
            return result

        return self.loop.run_until_complete(run_magic())

    def evaluate_with_context(self, context, expression):
        old_vars = self.variables.copy()
        self.variables.update(context)
        result = self.evaluate(expression)
        self.variables = old_vars
        return result