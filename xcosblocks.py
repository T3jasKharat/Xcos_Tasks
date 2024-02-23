# BEGIN Xcos/common/AAAAAA.py

import re
import xml.etree.ElementTree as ET
import math

TYPE_ARRAY = 'Array'
TYPE_DOUBLE = 'ScilabDouble'
TYPE_STRING = 'ScilabString'
CLASS_LIST = 'ScilabList'
BLOCK_AFFICHE = 'AfficheBlock'
BLOCK_BASIC = 'BasicBlock'
BLOCK_BIGSOM = 'BigSom'
BLOCK_EVENT_IN = 'EventInBlock'
BLOCK_EVENT_OUT = 'EventOutBlock'
BLOCK_EXPLICIT_IN = 'ExplicitInBlock'
BLOCK_EXPLICIT_OUT = 'ExplicitOutBlock'
BLOCK_GROUND = 'GroundBlock'
BLOCK_IMPLICIT_IN = 'ImplicitInBlock'
BLOCK_IMPLICIT_OUT = 'ImplicitOutBlock'
BLOCK_PRODUCT = 'Product'
BLOCK_ROUND = 'RoundBlock'
BLOCK_SPLIT = 'SplitBlock'
BLOCK_SUMMATION = 'Summation'
BLOCK_TEXT = 'TextBlock'
BLOCK_VOLTAGESENSOR = 'VoltageSensorBlock'

BLOCKTYPE_C = 'c'
BLOCKTYPE_D = 'd'
BLOCKTYPE_H = 'h'
BLOCKTYPE_L = 'l'
BLOCKTYPE_X = 'x'
BLOCKTYPE_Z = 'z'

TYPE_INTEGER = 'ScilabInteger'
CLASS_TLIST = 'ScilabTList'
GEOMETRY = 'mxGeometry'
AS_REAL_PARAM = 'realParameters'
AS_INT_PARAM = 'integerParameters'
AS_NBZERO = 'nbZerosCrossing'
AS_NMODE = 'nmode'
AS_STATE = 'state'
AS_DSTATE = 'dState'
AS_OBJ_PARAM = 'objectsParameters'
AS_ODSTATE = 'oDState'
AS_EQUATIONS = 'equations'
TYPE_SUPER = 'SuperBlockDiagram'
TYPE_ADD = 'add'
TYPE_MODEL = 'mxGraphModel'
AS_MODEL = 'model'
TYPE_ROOT = 'root'
TYPE_MXCELL = 'mxCell'
TYPE_EVENTOUT = 'EventOutBlock'
TYPE_CNTRL = 'ControlPort'
TYPE_CMD = 'CommandPort'
TYPE_LINK = 'CommandControlLink'
AS_VALUE = 'OpAmp'


def addNode(node, subNodeType, **kwargs):
    subNode = ET.SubElement(node, subNodeType)
    for (key, value) in kwargs.items():
        if value is not None:
            subNode.set(key, str(value))
    return subNode


def addObjNode(node, subNodeType, scilabClass, type, parameters):
    subNode = addDNode(node, subNodeType,
                       **{'as': type}, scilabClass=scilabClass)
    return subNode


def addPrecisionNode(node, subNodeType, type, height, parameters):
    width = 1 if height > 0 else 0
    subNode = addAsDataNode(node,
                            subNodeType, type, height, width,
                            parameters, intPrecision='sci_int32')
    return subNode


def addTypeNode(node, subNodeType, type, height, parameters):
    width = 1 if height > 0 else 0
    subNode = addAsDataNode(node, subNodeType, type, height, width, parameters)
    return subNode


# equations node start
def addArrayNode(node, scilabClass, **kwargs):
    kwargs['scilabClass'] = scilabClass
    return addDNode(node, 'Array', **kwargs)


def addScilabStringNode(node, width, parameters):
    scilabStringNode = addDataNode(node, 'ScilabString', height=1, width=width)
    for i, param in enumerate(parameters):
        addDataData(scilabStringNode, param)


def addScilabDoubleNode(node, realParts, width):
    scilabDoubleNode = addDataNode(node, 'ScilabDouble', height=1, width=width)
    for i, realPart in enumerate(realParts):
        addDData(scilabDoubleNode, realPart, line=0, column=i)


def addDData(parent, realPart, line=None, column=None):
    data_attributes = {'realPart': str(realPart)}
    if line is not None:
        data_attributes['line'] = str(line)
    if column is not None:
        data_attributes['column'] = str(column)

    ET.SubElement(parent, 'data', **data_attributes)
# equations node ends


def addgeometryNode(node, subNodeType, height, width, x, y):
    geometryNode = addDtNode(node, subNodeType, **{'as': 'geometry'},
                             height=height, width=width, x=x, y=y)
    return geometryNode


def addOutNode(node, subNodeType,
               attribid, ordering, parent,
               interface_func_name, simulation_func_name, simulation_func_type,
               style, blockType,
               **kwargs):
    newkwargs = {'id': attribid, 'ordering': ordering, 'parent': parent,
                 'interfaceFunctionName': interface_func_name,
                 'simulationFunctionName': simulation_func_name,
                 'simulationFunctionType': simulation_func_type,
                 'style': style, 'blockType': blockType}
    newkwargs.update(kwargs)
    return addNode(node, subNodeType, **newkwargs)


def addData(node, column, line, value, isReal=False):
    data = ET.SubElement(node, 'data')
    data.set('column', str(column))
    data.set('line', str(line))
    if type(value) == float or type(value) == int or isReal:
        data.set('realPart', str(value))
    else:
        data.set('value', value)
    return data


DATA_HEIGHT = 0
DATA_WIDTH = 0
DATA_LINE = 0
DATA_COLUMN = 0


def addDataNode(node, subNodeType, **kwargs):
    global DATA_HEIGHT, DATA_WIDTH, DATA_LINE, DATA_COLUMN
    DATA_HEIGHT = kwargs['height']
    DATA_WIDTH = kwargs['width']
    DATA_LINE = 0
    DATA_COLUMN = 0
    subNode = addNode(node, subNodeType, **kwargs)
    return subNode


def addAsDataNode(node, subNodeType, a, height, width, parameters, **kwargs):
    newkwargs = {'as': a, 'height': height, 'width': width}
    newkwargs.update(kwargs)
    subNode = addDataNode(node, subNodeType, **newkwargs)

    for param in parameters:
        addDataData(subNode, param)
    return subNode


def addDNode(node, subNodeType, **kwargs):
    subNode = addNode(node, subNodeType, **kwargs)
    return subNode


# for x & y in mxgeometry
def addDtNode(node, subNodeType, **kwargs):
    subNode = addNode(node, subNodeType, **kwargs)
    return subNode


def addDataData(node, value, isReal=False):
    global DATA_HEIGHT, DATA_WIDTH, DATA_LINE, DATA_COLUMN
    if DATA_LINE >= DATA_HEIGHT or DATA_COLUMN >= DATA_WIDTH:
        print('Invalid: height=', DATA_HEIGHT, ',width=', DATA_WIDTH,
              ',line=', DATA_LINE, ',column=', DATA_COLUMN)
    data = addData(node, DATA_COLUMN, DATA_LINE, value, isReal)
    if DATA_LINE < DATA_HEIGHT - 1:
        DATA_LINE += 1
    else:
        DATA_COLUMN += 1
    return data


def addExprsNode(node, subNodeType, height, parameters):
    width = 1 if height > 0 else 0
    subNode = addDataNode(node, subNodeType, **{'as': 'exprs'},
                          height=height, width=width)
    for i in range(height):
        addDataData(subNode, parameters[i])
    return subNode


def addExprsArrayNode(node, subSubNodeType, height, parameters, codeLines):
    subNode = addDataNode(node, TYPE_ARRAY, **{'as': 'exprs'},
                          scilabClass=CLASS_LIST)

    subSubNode = addDataNode(subNode, subSubNodeType, height=height, width=1)
    for i in range(height):
        addDataData(subSubNode, parameters[i])

    codeHeight = len(codeLines)
    subSubNode = addDataNode(subNode, TYPE_STRING,
                             height=codeHeight, width=1)
    for i in range(codeHeight):
        addDataData(subSubNode, codeLines[i])

    return subNode


def getParametersFromExprsNode(node, subNodeType):
    parameters = []

    if isinstance(node, dict):
        lastindex = None
        for i in range(100):
            parameter = 'p%03d_value' % i
            if parameter in node:
                value = node[parameter]
                parameters.append(value)
                if value != '':
                    lastindex = None
                elif lastindex is None:
                    lastindex = i
            else:
                break
        if lastindex is not None:
            del parameters[lastindex:]
    else:
        tag = subNodeType + '[@as="exprs"]'
        subNodes = node.find('./' + tag)

        if subNodes is not None:
            for data in subNodes:
                value = data.attrib.get('value')
                parameters.append(value)
        else:
            print(tag, ': Not found')

    return parameters


# Super Block Diagram
def addSuperNode(node, subNodeType,
                 a, background, gridEnabled,
                 title, **kwargs):
    newkwargs = {'as': a, 'background': background,
                 'gridEnabled': gridEnabled,
                 'title': title
                 }
    newkwargs.update(kwargs)
    return addNode(node, subNodeType, **newkwargs)


def addSuperBlkNode(node, subNodeType,
                    a, scilabClass,
                    **kwargs):
    newkwargs = {'as': a, 'scilabClass': scilabClass
                 }
    newkwargs.update(kwargs)
    return addNode(node, subNodeType, **newkwargs)


def superAddNode(node, subNodeType,
                 value,
                 **kwargs):
    newkwargs = {'value': value
                 }
    newkwargs.update(kwargs)
    return addNode(node, subNodeType, **newkwargs)


def addmxGraphModelNode(node, subNodeType,
                        a,
                        **kwargs):
    newkwargs = {'as': a
                 }
    newkwargs.update(kwargs)
    return addNode(node, subNodeType, **newkwargs)


def addmxCellNode(node, subNodeType,
                  id, a,
                  **kwargs):
    newkwargs = {'id': id, 'as': a
                 }
    newkwargs.update(kwargs)
    return addNode(node, subNodeType, **newkwargs)


def addEventOutBlock(node, subNodeType,
                     id, parent,
                     interfaceFunctionName,
                     simulationFunctionName,
                     simulationFunctionType,
                     style, blockType,
                     dependsOnU, dependsOnT,
                     **kwargs):
    newkwargs = {'id': id, 'parent': parent,
                 'interfaceFunctionName': interfaceFunctionName,
                 'simulationFunctionName':
                 simulationFunctionName,
                 'simulationFunctionType':
                 simulationFunctionType,
                 'style': style,
                 'blockType': blockType,
                 'dependsOnU': dependsOnU,
                 'dependsOnT': dependsOnT}
    newkwargs.update(kwargs)
    return addNode(node, subNodeType, **newkwargs)


def addPort(node, subNodeType,
            id, parent, ordering,
            dataType, dataColumns, dataLines, initialState,
            style, value,
            **kwargs):
    newkwargs = {'id': id, 'parent': parent,
                 'ordering': ordering,
                 'dataType': dataType,
                 'dataColumns': dataColumns,
                 'dataLines': dataLines,
                 'initialState': initialState,
                 'style': style, 'value': value}
    newkwargs.update(kwargs)
    return addNode(node, subNodeType, **newkwargs)


def addLink(node, subNodeType,
            id, parent,
            source, target,
            style, value,
            **kwargs):
    newkwargs = {'id': id, 'parent': parent,
                 'source': source,
                 'target': target,
                 'style': style, 'value': value}
    newkwargs.update(kwargs)
    return addNode(node, subNodeType, **newkwargs)


def addGeoNode(node, subNodeType,
               a,
               **kwargs):
    newkwargs = {'as': a}
    newkwargs.update(kwargs)
    return addNode(node, subNodeType, **newkwargs)


def addmxPointNode(node, subNodeType,
                   a, x, y,
                   **kwargs):
    newkwargs = {'as': a, 'x': x, 'y': y}
    newkwargs.update(kwargs)
    return addNode(node, subNodeType, **newkwargs)


def addPointNode(node, subNodeType,
                 x, y,
                 **kwargs):
    newkwargs = {'x': x, 'y': y}
    newkwargs.update(kwargs)
    return addNode(node, subNodeType, **newkwargs)


def addArray(node, subNodeType,
             a,
             **kwargs):
    newkwargs = {'as': a}
    newkwargs.update(kwargs)
    return addNode(node, subNodeType, **newkwargs)


# OpAmp
def addSciStringNode(node, height, parameters):
    scilabStringNode = addDataNode(node, 'ScilabString', height=height, width=1)
    for i in range(height):
        addDataData(scilabStringNode, parameters[i])


def addScilabDBNode(node, height):
    addDataNode(node, 'ScilabDouble', height=height, width=0)


# Sine Voltage
def addTNode(node, subNodeType, type, width, parameters):
    height = 1 if width > 0 else 0
    subNode = addAsDataNode(node, subNodeType, type, height, width, parameters)
    return subNode


def addSciDBNode(node, subNodeType, type, width, realParts):
    height = 1 if width > 0 else 0
    subNode = addAsDataNode(node, subNodeType, type, height, width, realParts)
    return subNode


# CSCope
def addPrecNode(node, subNodeType, type, width, parameters):
    height = 1 if width > 0 else 0
    subNode = addAsDataNode(node,
                            subNodeType, type, height, width,
                            parameters, intPrecision='sci_int32')
    return subNode


def strarray(parameter):
    param = list(map(str, parameter[0].split(" ")))
    params = parameter[3][1:8].split(";")
    parameters = param + params + parameter
    parameters.pop(10)
    parameters.pop(12)
    parameters = parameters[0:15]
    return parameters
# def addExprsNode(node, subNodeType, height, parameters):
#     width = 1 if height > 0 else 0
#     subNode = addDataNode(node, subNodeType, **{'as': 'exprs'},
#                           height=height, width=width)
#     for i in range(height):
#         addDataData(subNode, parameters[i])
#     return subNode
# Convert number into scientific notation
# Used by blocks Capacitor,ConstantVoltage,Inductor and Resistor


LOWER_LIMIT = 'lower_limit'
UPPER_LIMIT = 'upper_limit'
SIGN = 'sign'
VALUE = 'value'


def si_format(num):
    lower_limit = -11
    upper_limit = 15
    number = float(num)
    si_form = '{:.1e}'.format(number)
    neg_prefixes = (
                {SIGN: 'm', LOWER_LIMIT: -2, UPPER_LIMIT: 0, VALUE: 1E-3},
                {SIGN: 'μ', LOWER_LIMIT: -5, UPPER_LIMIT: -3, VALUE: 1E-6},
                {SIGN: 'n', LOWER_LIMIT: -8, UPPER_LIMIT: -6, VALUE: 1E-9},
                {SIGN: 'p', LOWER_LIMIT: -11, UPPER_LIMIT: -9, VALUE: 1E-12}
                )
    pos_prefixes = (
                {SIGN: '', LOWER_LIMIT: 1, UPPER_LIMIT: 3, VALUE: 1},
                {SIGN: 'k', LOWER_LIMIT: 4, UPPER_LIMIT: 6, VALUE: 1E3},
                {SIGN: 'M', LOWER_LIMIT: 7, UPPER_LIMIT: 9, VALUE: 1E6},
                {SIGN: 'G', LOWER_LIMIT: 10, UPPER_LIMIT: 12, VALUE: 1E9},
                {SIGN: 'T', LOWER_LIMIT: 13, UPPER_LIMIT: 15, VALUE: 1E12}
                )
    splits = si_form.split('e')
    base = float(splits[0])
    exp = int(splits[1])
    if exp < lower_limit or exp > upper_limit:
        return str(base) + ' 10^' + str(exp)
    else:
        if exp <= 0:
            for p in neg_prefixes:
                if exp >= p.get(LOWER_LIMIT) and exp <= p.get(UPPER_LIMIT):
                    return str(round(number/p.get(VALUE)))+' '+p.get(SIGN)
        else:
            for p in pos_prefixes:
                if exp >= p.get(LOWER_LIMIT) and exp <= p.get(UPPER_LIMIT):
                    return str(round(number/p.get(VALUE)))+' '+p.get(SIGN)


def print_affich_m(rows, columns, prec):
    s = '<TABLE>'
    for i in range(rows):
        s += '<TR>'
        for j in range(columns):
            s += '<TD>{:.{prec}f}</TD>'.format(0.0, prec=prec)
        s += '</TR>'
    s += '</TABLE>'
    return s


def print_affich_m_by_param(p0, p5):
    s = re.sub(r' *[\[\]] *', r'', p0)
    rc = re.split(' *[;,] *', s)
    rows = int(rc[0])
    columns = int(rc[1])
    prec = int(p5)
    return print_affich_m(rows, columns, prec)


def get_value_min(value):
    (v1, v2) = (value, re.sub(r'\([^()]*\)', r'', value))
    while v1 != v2:
        (v1, v2) = (v2, re.sub(r'\([^()]*\)', r'', v2))
    return get_number_power(v1)


def get_number_power(value):
    return re.sub(r'(\^|\*\*) *([a-zA-Z0-9]+|\([^()]*\)) *', r'<SUP>\2</SUP>',
                  value)


def format_real_number(parameter):
    real_number = float(parameter.replace('*10^', 'e').replace('10^', '1e'))
    formatted_number = "{:.1E}".format(real_number)
    return [formatted_number]

# END Xcos/common/AAAAAA.py
# BEGIN Xcos/blocks/ABS_VALUE.py


def ABS_VALUE(outroot, attribid, ordering, geometry, parameters):
    func_name = 'ABS_VALUE'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'absolute_value', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_ABS_VALUE(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/ABS_VALUE.py
# BEGIN Xcos/blocks/AFFICH_m.py


def AFFICH_m(outroot, attribid, ordering, geometry, parameters):
    func_name = 'AFFICH_m'

    outnode = addOutNode(outroot, BLOCK_AFFICHE,
                         attribid, ordering, 1,
                         func_name, 'affich2', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 7, parameters)

    return outnode


def get_from_AFFICH_m(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = print_affich_m_by_param(parameters[0], parameters[5])

    eiv = ''
    iiv = ''
    con = 1 if parameters[6] == '0' else 0
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/AFFICH_m.py
# BEGIN Xcos/blocks/ANDBLK.py


def ANDBLK(outroot, attribid, ordering, geometry, parameters):
    func_name = 'ANDBLK'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_H)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_ANDBLK(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/ANDBLK.py
# BEGIN Xcos/blocks/ANDLOG_f.py


def ANDLOG_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'ANDLOG_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'andlog', 'DEFAULT',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_ANDLOG_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/ANDLOG_f.py
# BEGIN Xcos/blocks/AUTOMAT.py


def AUTOMAT(outroot, attribid, ordering, geometry, parameters):
    func_name = 'AUTOMAT'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'automat', 'IMPLICIT_C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 7, parameters)

    return outnode


def get_from_AUTOMAT(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)
    display_parameter = parameters[0] + ',' + parameters[2]

    eiv = int(float(parameters[0]))
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/AUTOMAT.py
# BEGIN Xcos/blocks/BACKLASH.py


def BACKLASH(outroot, attribid, ordering, geometry, parameters):
    func_name = 'BACKLASH'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'backlash', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_BACKLASH(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/BACKLASH.py
# BEGIN Xcos/blocks/BARXY.py


def BARXY(outroot, attribid, ordering, geometry, parameters):
    func_name = 'BARXY'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'BARXY_sim', 'SCILAB',
                         func_name, BLOCKTYPE_D,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 5, parameters)

    return outnode


def get_from_BARXY(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/BARXY.py
# BEGIN Xcos/blocks/BIGSOM_f.py


def BIGSOM_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'BIGSOM_f'

    outnode = addOutNode(outroot, BLOCK_BIGSOM,
                         attribid, ordering, 1,
                         func_name, 'sum', 'TYPE_2',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1',
                         value='+')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_BIGSOM_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''
    inputs = parameters[0].split(';')

    eiv = len(inputs)
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/BIGSOM_f.py
# BEGIN Xcos/blocks/BITCLEAR.py


def BITCLEAR(outroot, attribid, ordering, geometry, parameters):
    func_name = 'BITCLEAR'

    datatype = ['', '', '', '32', '16', '8', '32', '16', '8']
    para1 = int(float(parameters[0]))

    simulation_func_name = 'bit_clear_' + datatype[para1]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_BITCLEAR(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[1]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/BITCLEAR.py
# BEGIN Xcos/blocks/BITSET.py


def BITSET(outroot, attribid, ordering, geometry, parameters):
    func_name = 'BITSET'

    datatype = ['', '', '', '32', '16', '8', '32', '16', '8']
    para1 = int(float(parameters[0]))

    simulation_func_name = 'bit_set_' + datatype[para1]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_BITSET(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[1]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/BITSET.py
# BEGIN Xcos/blocks/BOUNCE.py


def BOUNCE(outroot, attribid, ordering, geometry, parameters):
    func_name = 'BOUNCE'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'bounce_ball', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 7, parameters)

    return outnode


def get_from_BOUNCE(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/BOUNCE.py
# BEGIN Xcos/blocks/BOUNCEXY.py


def BOUNCEXY(outroot, attribid, ordering, geometry, parameters):
    func_name = 'BOUNCEXY'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'bouncexy', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 8, parameters)

    return outnode


def get_from_BOUNCEXY(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/BOUNCEXY.py
# BEGIN Xcos/blocks/BPLATFORM.py


def BPLATFORM(outroot, attribid, ordering, geometry, parameters):
    func_name = 'BPLATFORM'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'bplatform2', 'SCILAB',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 7, parameters)

    return outnode


def get_from_BPLATFORM(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/BPLATFORM.py
# BEGIN Xcos/blocks/Bache.py


def Bache(outroot, attribid, ordering, geometry, parameters):
    func_name = 'Bache'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'Bache', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 9, parameters)

    return outnode


def get_from_Bache(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/Bache.py
# BEGIN Xcos/blocks/CANIMXY.py


def CANIMXY(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CANIMXY'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'canimxy', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 11, parameters)

    return outnode


def get_from_CANIMXY(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CANIMXY.py
# BEGIN Xcos/blocks/CANIMXY3D.py


def CANIMXY3D(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CANIMXY3D'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'canimxy3d', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 11, parameters)

    return outnode


def get_from_CANIMXY3D(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CANIMXY3D.py
# BEGIN Xcos/blocks/CBLOCK.py


def CBLOCK(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CBLOCK'

    if parameters[1] == 'y':
        type = 'IMPLICIT'
    else:
        type = 'EXPLICIT'

    simulation_func_type = 'DYNAMIC_' + type + '_4'

    if parameters[12] == 'y':
        depends_u = '1'
    else:
        depends_u = '0'

    if parameters[13] == 'y':
        depends_t = '1'
    else:
        depends_t = '0'

    code = parameters[14]
    codeLines = code.split('\n')

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, parameters[0], simulation_func_type,
                         func_name, BLOCKTYPE_C,
                         dependsOnU=depends_u,
                         dependsOnT=depends_t)

    addExprsArrayNode(outnode, TYPE_STRING, 14, parameters, codeLines)

    return outnode


def get_from_CBLOCK(cell):
    parameters = getParametersFromExprsNode(cell)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = 1 if parameters[4] != '[]' and int(float(parameters[4])) == 1 else 0
    eov = ''
    iov = ''
    com = 1 if parameters[5] != '[]' and int(float(parameters[5])) == 1 else 0

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CBLOCK.py
# BEGIN Xcos/blocks/CBLOCK4.py


def CBLOCK4(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CBLOCK4'

    if parameters[1] == 'y':
        type = 'IMPLICIT'
    else:
        type = 'EXPLICIT'

    simulation_func_type = 'DYNAMIC_' + type + '_4'

    if parameters[17] == 'y':
        depends_u = '1'
    else:
        depends_u = '0'

    if parameters[18] == 'y':
        depends_t = '1'
    else:
        depends_t = '0'

    code = parameters[19]
    codeLines = code.split('\n')

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, parameters[0], simulation_func_type,
                         func_name, BLOCKTYPE_C,
                         dependsOnU=depends_u,
                         dependsOnT=depends_t)

    addExprsArrayNode(outnode, TYPE_STRING, 19, parameters, codeLines)

    return outnode


def get_from_CBLOCK4(cell):
    parameters = getParametersFromExprsNode(cell)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = 1 if parameters[6] != '[]' and int(float(parameters[6])) == 1 else 0
    eov = ''
    iov = ''
    com = 1 if parameters[7] != '[]' and int(float(parameters[7])) == 1 else 0

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CBLOCK4.py
# BEGIN Xcos/blocks/CCS.py


def CCS(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CCS'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'CCS', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_CCS(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CCS.py
# BEGIN Xcos/blocks/CEVENTSCOPE.py


def CEVENTSCOPE(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CEVENTSCOPE'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cevscpe', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 6, parameters)

    return outnode


def get_from_CEVENTSCOPE(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = int(float(parameters[0]))
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CEVENTSCOPE.py
# BEGIN Xcos/blocks/CFSCOPE.py


def CFSCOPE(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CFSCOPE'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cfscope', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 9, parameters)

    return outnode


def get_from_CFSCOPE(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CFSCOPE.py
# BEGIN Xcos/blocks/CLINDUMMY_f.py


def CLINDUMMY_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CLINDUMMY_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cdummy', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_CLINDUMMY_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CLINDUMMY_f.py
# BEGIN Xcos/blocks/CLKFROM.py


def CLKFROM(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CLKFROM'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'clkfrom', 'DEFAULT',
                         func_name, BLOCKTYPE_D,
                         value='From')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_CLKFROM(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CLKFROM.py
# BEGIN Xcos/blocks/CLKGOTO.py


def CLKGOTO(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CLKGOTO'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'clkgoto', 'DEFAULT',
                         func_name, BLOCKTYPE_D,
                         value='Goto')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_CLKGOTO(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CLKGOTO.py
# BEGIN Xcos/blocks/CLKGotoTagVisibility.py


def CLKGotoTagVisibility(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CLKGotoTagVisibility'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'clkgototagvisibility', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_CLKGotoTagVisibility(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CLKGotoTagVisibility.py
# BEGIN Xcos/blocks/CLKINV_f.py


def CLKINV_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CLKINV_f'

    outnode = addOutNode(outroot, BLOCK_EVENT_IN,
                         attribid, ordering, 1,
                         func_name, 'input', 'DEFAULT',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_CLKINV_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CLKINV_f.py
# BEGIN Xcos/blocks/CLKOUTV_f.py


def CLKOUTV_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CLKOUTV_f'

    outnode = addOutNode(outroot, BLOCK_EVENT_OUT,
                         attribid, ordering, 1,
                         func_name, 'output', 'DEFAULT',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_CLKOUTV_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CLKOUTV_f.py
# BEGIN Xcos/blocks/CLKOUT_f.py


def CLKOUT_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CLKOUT_f'

    outnode = addOutNode(outroot, BLOCK_EVENT_OUT,
                         attribid, ordering, 1,
                         func_name, 'output', 'DEFAULT',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)
    addTypeNode(outnode, TYPE_DOUBLE, AS_REAL_PARAM, 0,
                [])
    array = ['0']
    addPrecisionNode(outnode, TYPE_INTEGER, AS_INT_PARAM, 1, array)
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_OBJ_PARAM, parameters)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NBZERO, 1, array)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NMODE, 1, array)
    addTypeNode(outnode, TYPE_DOUBLE, AS_STATE, 0, [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_DSTATE, 0, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_ODSTATE, parameters)
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_EQUATIONS, parameters)
    addgeometryNode(outnode, GEOMETRY, geometry['height'],
                    geometry['width'], geometry['x'], geometry['y'])

    return outnode


def get_from_CLKOUT_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CLKOUT_f.py
# BEGIN Xcos/blocks/CLKSOMV_f.py


def CLKSOMV_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CLKSOMV_f'

    outnode = addOutNode(outroot, BLOCK_ROUND,
                         attribid, ordering, 1,
                         func_name, 'sum', 'DEFAULT',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_CLKSOMV_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CLKSOMV_f.py
# BEGIN Xcos/blocks/CLOCK_c.py


block_id = ['128c18ea:1383ab8277d:-748d', '-73e75f0:167968eb73f:-7955',
            '-73e75f0:167968eb73f:-7953', '-73e75f0:167968eb73f:-7950']
link_id = ['-63efee48:189fd5ed04e:-73d5', '-63efee48:189fd5ed04e:-73d4',
           '-63efee48:189fd5ed04e:-73d3', '128c18ea:1383ab8277e:-748d'
           ]
port_id = ['-63efee48:189fd5ed04e:-73dd', '-63efee48:189fd5ed04e:-73db',
           '-63efee48:189fd5ed04e:-73da', '-63efee48:189fd5ed04e:-73d8',
           '-63efee48:189fd5ed04e:-73d7', '-63efee48:189fd5ed04e:-73d6'
           ]


def CLOCK_c(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CLOCK_c'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_H)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)
    addTypeNode(outnode, TYPE_DOUBLE, AS_REAL_PARAM, 0,
                [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_INT_PARAM, 0, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_OBJ_PARAM, parameters)
    array = ['0']
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NBZERO, 1, array)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NMODE, 1, array)
    addTypeNode(outnode, TYPE_DOUBLE, AS_STATE, 0, [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_DSTATE, 0, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_ODSTATE, parameters)
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_EQUATIONS, parameters)
    addgeometryNode(outnode, GEOMETRY, geometry['height'],
                    geometry['width'], geometry['x'], geometry['y'])

    # Create the SuperBlockDiagram element
    SuperBlockDiagram = addSuperNode(outnode, TYPE_SUPER,
                                     a="child",
                                     background="-1",
                                     gridEnabled="1",
                                     title="")

    Array = addSuperBlkNode(SuperBlockDiagram, TYPE_ARRAY,
                            a="context",
                            scilabClass="String[]")
    superAddNode(Array, TYPE_ADD, value="")

    mxGraphModel = addmxGraphModelNode(SuperBlockDiagram,
                                       TYPE_MODEL, a="model")
    root = addNode(mxGraphModel, TYPE_ROOT)
    addmxCellNode(root, TYPE_MXCELL,
                  id=block_id[0], a='')
    addmxCellNode(root, TYPE_MXCELL,
                  id=block_id[0],
                  parent=block_id[0], a='')

    # Create the EventOutBlock node inside the root tag
    CLKOUT_f(root, block_id[1], ordering, geometry, parameters)

    addPort(root, TYPE_CNTRL, id=port_id[0],
            parent=block_id[1], ordering="1",
            dataType="REAL_MATRIX", dataColumns="1",
            dataLines="-1", initialState="0.0",
            style="ControlPort", value="")

    EVTDLY_c(root, block_id[2], ordering, geometry, parameters)

    addPort(root, TYPE_CNTRL, id=port_id[1],
            parent=block_id[2], ordering="1",
            dataType="REAL_MATRIX", dataColumns="1",
            dataLines="-1", initialState="0.0",
            style="ControlPort", value="")
    addPort(root, TYPE_CMD, id=port_id[2],
            parent=block_id[2], ordering="1",
            dataType="REAL_MATRIX", dataColumns="1",
            dataLines="-1", initialState="0.0",
            style="CommandPort", value="")

    SplitBlock(root, attribid, ordering, geometry)

    addPort(root, TYPE_CNTRL, id=port_id[3],
            parent=block_id[3], ordering="1",
            dataType="REAL_MATRIX", dataColumns="1",
            dataLines="-1", initialState="0.0",
            style="ControlPort", value="")
    addPort(root, TYPE_CMD, id=port_id[4],
            parent=block_id[3], ordering="1",
            dataType="REAL_MATRIX", dataColumns="1",
            dataLines="-1", initialState="-1.0",
            style="CommandPort", value="")
    addPort(root, TYPE_CMD, id=port_id[5],
            parent=block_id[3], ordering="2",
            dataType="REAL_MATRIX", dataColumns="1",
            dataLines="-1", initialState="-1.0",
            style="CommandPort", value="")

    CCLink = addLink(root, TYPE_LINK, id=link_id[0],
                     parent=link_id[3],
                     source=port_id[5],
                     target=port_id[1],
                     style="CommandControlLink", value="")
    gemotryNode = addGeoNode(CCLink, GEOMETRY, a="geometry")
    addmxPointNode(gemotryNode, 'mxPoint',
                   a="sourcePoint", x="0.0", y="11.0")
    ArrayNode = addArray(gemotryNode, TYPE_ARRAY, a="points")
    addPointNode(ArrayNode, 'mxPoint',
                 x="100.70999999999998", y="40.0")
    addPointNode(ArrayNode, 'mxPoint', x="60.0",
                 y="40.0")
    addmxPointNode(gemotryNode, 'mxPoint',
                   a="targetPoint", x="20.0", y="-4.0")
    CCLink = addLink(root, TYPE_LINK, id=link_id[1],
                     parent=link_id[3],
                     source=port_id[4],
                     target=port_id[0],
                     style="CommandControlLink", value="")
    gemotryNode = addGeoNode(CCLink, GEOMETRY, a="geometry")
    addmxPointNode(gemotryNode, 'mxPoint', a="sourcePoint",
                   x="0.0", y="11.0")
    ArrayNode = addArray(gemotryNode, TYPE_ARRAY, a="points")
    addmxPointNode(gemotryNode, 'mxPoint', a="targetPoint",
                   x="10.0", y="-4.0")
    CCLink = addLink(root, TYPE_LINK, id=link_id[2],
                     parent=link_id[3],
                     source=port_id[2],
                     target=port_id[3],
                     style="CommandControlLink", value="")
    gemotryNode = addGeoNode(CCLink, GEOMETRY, a="geometry")
    addmxPointNode(gemotryNode, 'mxPoint', a="sourcePoint",
                   x="20.0", y="44.0")
    ArrayNode = addArray(gemotryNode, TYPE_ARRAY, a="points")
    addPointNode(ArrayNode, 'mxPoint', x="60.0", y="170.0")
    addmxPointNode(gemotryNode, 'mxPoint', a="targetPoint",
                   x="0.0", y="-4.0")
    addmxCellNode(SuperBlockDiagram, TYPE_MXCELL,
                  id=block_id[0],
                  parent=block_id[0],
                  a="defaultParent")

    return outnode


def get_from_CLOCK_c(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CLOCK_c.py
# BEGIN Xcos/blocks/CLR.py


def CLR(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CLR'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csslti4', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_CLR(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    dp1 = get_value_min(parameters[0])
    dp2 = get_value_min(parameters[1])
    display_parameter = dp1 + ',' + dp2

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CLR.py
# BEGIN Xcos/blocks/CLSS.py


def CLSS(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CLSS'

    para4 = int(float(parameters[3]))

    if para4 == 0:
        depends_u = '0'
    else:
        depends_u = '1'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csslti4', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU=depends_u,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 5, parameters)

    return outnode


def get_from_CLSS(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CLSS.py
# BEGIN Xcos/blocks/CMAT3D.py


def CMAT3D(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CMAT3D'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cmat3d', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 5, parameters)

    return outnode


def get_from_CMAT3D(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CMAT3D.py
# BEGIN Xcos/blocks/CMATVIEW.py


def CMATVIEW(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CMATVIEW'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cmatview', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_CMATVIEW(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CMATVIEW.py
# BEGIN Xcos/blocks/CMSCOPE.py


def CMSCOPE(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CMSCOPE'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cmscope', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1',
                         value=parameters[10])

    addExprsNode(outnode, TYPE_STRING, 11, parameters)

    return outnode


def get_from_CMSCOPE(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''
    input = parameters[0].split(' ')

    eiv = len(input)
    iiv = ''
    con = 1 if int(float(parameters[9])) == 0 else 0
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CMSCOPE.py
# BEGIN Xcos/blocks/CONST.py


def CONST(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CONST'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cstblk4', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_CONST(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = get_number_power(parameters[0])

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CONST.py
# BEGIN Xcos/blocks/CONSTRAINT2_c.py


def CONSTRAINT2_c(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CONSTRAINT2_c'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'constraint_c', 'IMPLICIT_C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_CONSTRAINT2_c(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0] + ',' + parameters[1]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CONSTRAINT2_c.py
# BEGIN Xcos/blocks/CONSTRAINT_c.py


def CONSTRAINT_c(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CONSTRAINT_c'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'constraint_c', 'IMPLICIT_C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_CONSTRAINT_c(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CONSTRAINT_c.py
# BEGIN Xcos/blocks/CONST_f.py


def CONST_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CONST_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cstblk', 'TYPE_1',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_CONST_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = get_number_power(parameters[0])

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CONST_f.py
# BEGIN Xcos/blocks/CONST_m.py


def CONST_m(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CONST_m'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cstblk4_m', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_CONST_m(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = get_number_power(parameters[0])

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CONST_m.py
# BEGIN Xcos/blocks/CONVERT.py


def CONVERT(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CONVERT'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'convert', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_CONVERT(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    types = ['decim.', 'decim.', 'int32', 'int16',
             'int8', 'uint32', 'uint16', 'uint8']
    input_t = int(float(parameters[0]))
    output_t = int(float(parameters[1]))

    input_type = types[input_t-1]
    output_type = types[output_t-1]

    display_parameter = input_type + ',' + output_type

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CONVERT.py
# BEGIN Xcos/blocks/COSBLK_f.py


def COSBLK_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'COSBLK_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cosblk', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_COSBLK_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/COSBLK_f.py
# BEGIN Xcos/blocks/CSCOPE.py


def CSCOPE(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CSCOPE'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cscope', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 10, parameters)
    addSciDBNode(outnode, TYPE_DOUBLE, AS_REAL_PARAM,
                 4, realParts=[0.0, -2.7, -2.0, 1.0])
    # print(parameters)

    param = strarray(parameters)
    addPrecNode(outnode, TYPE_INTEGER, AS_INT_PARAM, 15, param)
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_OBJ_PARAM, parameters)
    array = ['0']
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NBZERO, 1, array)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NMODE, 1, array)
    addTypeNode(outnode, TYPE_DOUBLE, AS_STATE, 0, [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_DSTATE, 0, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_ODSTATE, parameters)
    addObjNode(outnode, TYPE_ARRAY,
               CLASS_LIST, AS_EQUATIONS, parameters)
    addgeometryNode(outnode, GEOMETRY, geometry['height'],
                    geometry['width'], geometry['x'], geometry['y'])

    return outnode


def get_from_CSCOPE(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = 1 if int(float(parameters[8])) == 0 else 0
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CSCOPE.py
# BEGIN Xcos/blocks/CSCOPXY.py


def CSCOPXY(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CSCOPXY'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cscopxy', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 11, parameters)

    return outnode


def get_from_CSCOPXY(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CSCOPXY.py
# BEGIN Xcos/blocks/CSCOPXY3D.py


def CSCOPXY3D(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CSCOPXY3D'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cscopxy3d', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 11, parameters)

    return outnode


def get_from_CSCOPXY3D(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CSCOPXY3D.py
# BEGIN Xcos/blocks/CUMSUM.py


def CUMSUM(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CUMSUM'

    para1 = int(parameters[0])
    para2 = int(parameters[1])

    if para1 == 1:
        datatype = 'z'
    else:
        datatype = ''

    if para2 == 1:
        sum = 'r'
    elif para2 == 2:
        sum = 'c'
    else:
        sum = 'm'

    simulation_func_name = 'cumsum' + datatype + '_' + sum

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_CUMSUM(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CUMSUM.py
# BEGIN Xcos/blocks/CURV_f.py


def CURV_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CURV_f'
    para = parameters[0].split(' ')

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'intplt', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    node = addNode(outnode, TYPE_STRING, height=1, width=len(para))

    for i in range(len(para)):

        addData(node, i, 0, para[i])

    return outnode


def get_from_CURV_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CURV_f.py
# BEGIN Xcos/blocks/CVS.py


def CVS(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CVS'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'CVS', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_CVS(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CVS.py
# BEGIN Xcos/blocks/Capacitor.py


def Capacitor(outroot, attribid, ordering, geometry, parameters):
    func_name = 'Capacitor'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'Capacitor', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)
    addTypeNode(outnode, TYPE_DOUBLE, AS_REAL_PARAM, 1,
                format_real_number(parameters[0]))
    addTypeNode(outnode, TYPE_DOUBLE, AS_INT_PARAM, 0, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_OBJ_PARAM, parameters)
    array = ['0']
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NBZERO, 1, array)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NMODE, 1, array)
    addTypeNode(outnode, TYPE_DOUBLE, AS_STATE, 0, [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_DSTATE, 0, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_ODSTATE, parameters)
    # Create the outer Array node for equations
    equationsArrayNode = addArrayNode(outnode, scilabClass="ScilabTList",
                                      **{'as': 'equations'})

    # Add ScilabString nodes to equationsArrayNode
    scilabStringParameters = ["modelica", "model",
                              "inputs", "outputs",
                              "parameters"]
    addScilabStringNode(equationsArrayNode, width=5,
                        parameters=scilabStringParameters)

    # Add additional ScilabString nodes to equationsArrayNode
    additionalScilabStrings = ["Capacitor", "p", "n"]
    for param in additionalScilabStrings:
        additionalStringNode = addDataNode(equationsArrayNode,
                                           'ScilabString',
                                           height=1, width=1)
        addDataData(additionalStringNode, param)

    # Create the inner Array node for ScilabList
    innerArrayNode = addArrayNode(equationsArrayNode,
                                  scilabClass="ScilabList")

    scilabStringParameters = ["C", "v"]
    addScilabStringNode(innerArrayNode, width=2,
                        parameters=scilabStringParameters)

    # Add nested Array node inside innerArrayNode
    nestedArrayNode = addArrayNode(innerArrayNode,
                                   scilabClass="ScilabList")
    addScilabDoubleNode(nestedArrayNode, width=1, realParts=["4.7E-6"])
    addScilabDoubleNode(nestedArrayNode, width=1, realParts=["2.0"])
    addScilabDoubleNode(innerArrayNode, width=2, realParts=["0.0", "1.0"])
    addgeometryNode(outnode, GEOMETRY, geometry['height'],
                    geometry['width'], geometry['x'], geometry['y'])
    return outnode


def get_from_Capacitor(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = si_format(parameters[0])

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/Capacitor.py
# BEGIN Xcos/blocks/ConstantVoltage.py


def ConstantVoltage(outroot, attribid, ordering, geometry, parameters):
    func_name = 'ConstantVoltage'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'ConstantVoltage', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_ConstantVoltage(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = si_format(parameters[0])

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/ConstantVoltage.py
# BEGIN Xcos/blocks/Counter.py


def Counter(outroot, attribid, ordering, geometry, parameters):
    func_name = 'Counter'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'counter', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_Counter(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0] + ',' + parameters[1]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/Counter.py
# BEGIN Xcos/blocks/CurrentSensor.py


def CurrentSensor(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CurrentSensor'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'CurrentSensor', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_CurrentSensor(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/CurrentSensor.py
# BEGIN Xcos/blocks/DEADBAND.py


def DEADBAND(outroot, attribid, ordering, geometry, parameters):
    func_name = 'DEADBAND'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'deadband', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_DEADBAND(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/DEADBAND.py
# BEGIN Xcos/blocks/DEBUG.py


def DEBUG(outroot, attribid, ordering, geometry, parameters):
    func_name = 'DEBUG'

    code = parameters[0]
    codeLines = code.split('\n')

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, '%debug_scicos', 'DEBUG',
                         func_name, BLOCKTYPE_D)

    addExprsArrayNode(outnode, TYPE_STRING, 1, [''], codeLines)

    return outnode


def get_from_DEBUG(cell):
    parameters = getParametersFromExprsNode(cell)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/DEBUG.py
# BEGIN Xcos/blocks/DELAYV_f.py


def DELAYV_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'DELAYV_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'delayv', 'TYPE_1',
                         func_name, BLOCKTYPE_D,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_DELAYV_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/DELAYV_f.py
# BEGIN Xcos/blocks/DELAY_f.py


def DELAY_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'DELAY_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_H)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_DELAY_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/DELAY_f.py
# BEGIN Xcos/blocks/DEMUX.py


def DEMUX(outroot, attribid, ordering, geometry, parameters):
    func_name = 'DEMUX'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'multiplex', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_DEMUX(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = int(float(parameters[0]))
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/DEMUX.py
# BEGIN Xcos/blocks/DEMUX_f.py


def DEMUX_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'DEMUX_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'demux', 'TYPE_1',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_DEMUX_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = int(float(parameters[0]))
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/DEMUX_f.py
# BEGIN Xcos/blocks/DERIV.py


def DERIV(outroot, attribid, ordering, geometry, parameters):
    func_name = 'DERIV'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'deriv', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_X,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_DERIV(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/DERIV.py
# BEGIN Xcos/blocks/DFLIPFLOP.py


def DFLIPFLOP(outroot, attribid, ordering, geometry, parameters):
    func_name = 'DFLIPFLOP'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_H,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_DFLIPFLOP(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/DFLIPFLOP.py
# BEGIN Xcos/blocks/DIFF_f.py


def DIFF_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'DIFF_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'diffblk', 'OLDBLOCKS',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_DIFF_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/DIFF_f.py
# BEGIN Xcos/blocks/DLATCH.py


def DLATCH(outroot, attribid, ordering, geometry, parameters):
    func_name = 'DLATCH'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_H,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_DLATCH(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/DLATCH.py
# BEGIN Xcos/blocks/DLR.py


def DLR(outroot, attribid, ordering, geometry, parameters):
    func_name = 'DLR'

    depends_on_flag = 0

    num_str = parameters[0]
    den_str = parameters[1]

    num_exponents = []
    den_exponents = []

    num_matches = re.findall(r'z\s*\^\s*\d+|z', num_str)
    den_matches = re.findall(r'z\s*\^\s*\d+|z', den_str)

    if len(num_matches) == 0 and len(den_matches) == 0:
        depends_on_flag = 1
    else:

        for match in num_matches:
            splits = match.split('^')

            if len(splits) == 1:
                num_exponents.append(1)
            else:
                num_exponents.append(int(splits[1]))

        for match in den_matches:
            splits = match.split('^')

            if len(splits) == 1:
                den_exponents.append(1)
            else:
                den_exponents.append(int(splits[1]))

        if max(num_exponents) == max(den_exponents):
            depends_on_flag = 1

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'dsslti4', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D,
                         dependsOnU=depends_on_flag)

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_DLR(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    dp1 = get_value_min(parameters[0])
    dp2 = get_value_min(parameters[1])
    display_parameter = dp1 + ',' + dp2

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/DLR.py
# BEGIN Xcos/blocks/DLRADAPT_f.py


def DLRADAPT_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'DLRADAPT_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'dlradp', 'DEFAULT',
                         func_name, BLOCKTYPE_D,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 6, parameters)

    return outnode


def get_from_DLRADAPT_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/DLRADAPT_f.py
# BEGIN Xcos/blocks/DLSS.py


def DLSS(outroot, attribid, ordering, geometry, parameters):
    func_name = 'DLSS'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'dsslti4', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 5, parameters)

    return outnode


def get_from_DLSS(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/DLSS.py
# BEGIN Xcos/blocks/DOLLAR.py


def DOLLAR(outroot, attribid, ordering, geometry, parameters):
    func_name = 'DOLLAR'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'dollar4', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_DOLLAR(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = 1 if float(parameters[1]) == 0.0 else 0
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/DOLLAR.py
# BEGIN Xcos/blocks/DOLLAR_f.py


def DOLLAR_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'DOLLAR_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'dollar', 'DEFAULT',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_DOLLAR_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = 1 if float(parameters[1]) == 0.0 else 0
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/DOLLAR_f.py
# BEGIN Xcos/blocks/DOLLAR_m.py


def DOLLAR_m(outroot, attribid, ordering, geometry, parameters):
    func_name = 'DOLLAR_m'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'dollar4', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_DOLLAR_m(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = 1 if float(parameters[1]) == 0.0 else 0
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/DOLLAR_m.py
# BEGIN Xcos/blocks/Diode.py


def Diode(outroot, attribid, ordering, geometry, parameters):
    func_name = 'Diode'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'Diode', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 4, parameters)

    return outnode


def get_from_Diode(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/Diode.py
# BEGIN Xcos/blocks/EDGE_TRIGGER.py


def EDGE_TRIGGER(outroot, attribid, ordering, geometry, parameters):
    func_name = 'EDGE_TRIGGER'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_EDGE_TRIGGER(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/EDGE_TRIGGER.py
# BEGIN Xcos/blocks/ENDBLK.py


def ENDBLK(outroot, attribid, ordering, geometry, parameters):
    func_name = 'ENDBLK'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_H)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_ENDBLK(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/ENDBLK.py
# BEGIN Xcos/blocks/END_c.py


def END_c(outroot, attribid, ordering, geometry, parameters):
    func_name = 'END_c'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'scicosexit', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_END_c(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/END_c.py
# BEGIN Xcos/blocks/ESELECT_f.py


def ESELECT_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'ESELECT_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'eselect', 'ESELECT',
                         func_name, BLOCKTYPE_L,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_ESELECT_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = 0 if float(parameters[1]) == 0.0 else 1
    eov = ''
    iov = ''
    com = int(float(parameters[0]))

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/ESELECT_f.py
# BEGIN Xcos/blocks/EVTDLY_c.py


def EVTDLY_c(outroot, attribid, ordering, geometry, parameters):
    func_name = 'EVTDLY_c'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'evtdly4', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 2, parameters)
    addTypeNode(outnode, TYPE_DOUBLE, AS_REAL_PARAM, 0,
                [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_INT_PARAM, 0, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_OBJ_PARAM, parameters)
    array = ['0']
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NBZERO, 1, array)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NMODE, 1, array)
    addTypeNode(outnode, TYPE_DOUBLE, AS_STATE, 0, [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_DSTATE, 0, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_ODSTATE, parameters)
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_EQUATIONS, parameters)
    addgeometryNode(outnode, GEOMETRY, geometry['height'],
                    geometry['width'], geometry['x'], geometry['y'])

    return outnode


def get_from_EVTDLY_c(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/EVTDLY_c.py
# BEGIN Xcos/blocks/EVTGEN_f.py


def EVTGEN_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'EVTGEN_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'trash', 'DEFAULT',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_EVTGEN_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/EVTGEN_f.py
# BEGIN Xcos/blocks/EVTVARDLY.py


def EVTVARDLY(outroot, attribid, ordering, geometry, parameters):
    func_name = 'EVTVARDLY'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'evtvardly', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_EVTVARDLY(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/EVTVARDLY.py
# BEGIN Xcos/blocks/EXPBLK_m.py


def EXPBLK_m(outroot, attribid, ordering, geometry, parameters):
    func_name = 'EXPBLK_m'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'expblk_m', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_EXPBLK_m(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/EXPBLK_m.py
# BEGIN Xcos/blocks/EXPRESSION.py


def EXPRESSION(outroot, attribid, ordering, geometry, parameters):
    func_name = 'EXPRESSION'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'evaluate_expr', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_EXPRESSION(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[1]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/EXPRESSION.py
# BEGIN Xcos/blocks/EXTRACT.py


def EXTRACT(outroot, attribid, ordering, geometry, parameters):
    func_name = 'EXTRACT'

    data_type = ['', 'extract', 'extractz']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_EXTRACT(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/EXTRACT.py
# BEGIN Xcos/blocks/EXTRACTBITS.py


def EXTRACTBITS(outroot, attribid, ordering, geometry, parameters):
    func_name = 'EXTRACTBITS'

    d_type = ['', 'UH', 'LH', 'MSB', 'LSB', 'RB']
    type1 = ['', '', '', '32', '16', '8', 'u32', 'u16', 'u8']
    type2 = ['', '', '', '32', '16', '8', '32', '16', '8']

    para1 = int(float(parameters[0]))
    para2 = int(float(parameters[1]))
    para4 = int(float(parameters[3]))

    if para2 == 2 or para2 == 4:
        bits_extract = type2[para1] + '_' + d_type[para2]
        bit_int = ''
    else:
        if para4 == 0:
            bits_extract = type2[para1] + '_' + d_type[para2]
        else:
            bits_extract = type1[para1] + '_' + d_type[para2]
        bit_int = str(para4)

    simulation_func_name = 'extract_bit_' + bits_extract + bit_int

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 4, parameters)

    return outnode


def get_from_EXTRACTBITS(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[1]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/EXTRACTBITS.py
# BEGIN Xcos/blocks/EXTRACTOR.py


def EXTRACTOR(outroot, attribid, ordering, geometry, parameters):
    func_name = 'EXTRACTOR'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'extractor', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_EXTRACTOR(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/EXTRACTOR.py
# BEGIN Xcos/blocks/EXTTRI.py


def EXTTRI(outroot, attribid, ordering, geometry, parameters):
    func_name = 'EXTTRI'

    extration_type = ['', 'exttril', 'exttriu', 'extdiag']
    data_type = ['', '', 'z']
    para1 = int(parameters[0])
    para2 = int(parameters[1])

    simulation_func_name = extration_type[para2] + data_type[para1]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_EXTTRI(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/EXTTRI.py
# BEGIN Xcos/blocks/Extract_Activation.py


def Extract_Activation(outroot, attribid, ordering, geometry, parameters):
    func_name = 'Extract_Activation'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_Extract_Activation(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/Extract_Activation.py
# BEGIN Xcos/blocks/FROM.py


def FROM(outroot, attribid, ordering, geometry, parameters):
    func_name = 'FROM'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'from', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_FROM(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/FROM.py
# BEGIN Xcos/blocks/FROMMO.py


def FROMMO(outroot, attribid, ordering, geometry, parameters):
    func_name = 'FROMMO'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'frommo', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_FROMMO(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/FROMMO.py
# BEGIN Xcos/blocks/FROMWSB.py


def FROMWSB(outroot, attribid, ordering, geometry, parameters):
    func_name = 'FROMWSB'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_H)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_FROMWSB(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/FROMWSB.py
# BEGIN Xcos/blocks/Flowmeter.py


def Flowmeter(outroot, attribid, ordering, geometry, parameters):
    func_name = 'Flowmeter'
    parameters = ['1']

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'Flowmeter', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_Flowmeter(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/Flowmeter.py
# BEGIN Xcos/blocks/GAINBLK.py


def GAINBLK(outroot, attribid, ordering, geometry, parameters):
    func_name = 'GAINBLK'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'gainblk', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_GAINBLK(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/GAINBLK.py
# BEGIN Xcos/blocks/GAINBLK_f.py


def GAINBLK_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'GAINBLK_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'gain', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_GAINBLK_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/GAINBLK_f.py
# BEGIN Xcos/blocks/GAIN_f.py


def GAIN_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'GAIN_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'gain', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_GAIN_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/GAIN_f.py
# BEGIN Xcos/blocks/GENERAL_f.py


def GENERAL_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'GENERAL_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'zcross', 'TYPE_1',
                         func_name, BLOCKTYPE_Z,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_GENERAL_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = int(float(parameters[1]))

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/GENERAL_f.py
# BEGIN Xcos/blocks/GENSIN_f.py


def GENSIN_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'GENSIN_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'gensin', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_GENSIN_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/GENSIN_f.py
# BEGIN Xcos/blocks/GENSQR_f.py


def GENSQR_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'GENSQR_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'gensqr', 'DEFAULT',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_GENSQR_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/GENSQR_f.py
# BEGIN Xcos/blocks/GOTO.py


def GOTO(outroot, attribid, ordering, geometry, parameters):
    func_name = 'GOTO'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'goto', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_GOTO(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/GOTO.py
# BEGIN Xcos/blocks/GOTOMO.py


def GOTOMO(outroot, attribid, ordering, geometry, parameters):
    func_name = 'GOTOMO'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'gotomo', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_GOTOMO(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/GOTOMO.py
# BEGIN Xcos/blocks/GotoTagVisibility.py


def GotoTagVisibility(outroot, attribid, ordering, geometry, parameters):
    func_name = 'GotoTagVisibility'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'gototagvisibility', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_GotoTagVisibility(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/GotoTagVisibility.py
# BEGIN Xcos/blocks/GotoTagVisibilityMO.py


def GotoTagVisibilityMO(outroot, attribid, ordering, geometry, parameters):
    func_name = 'GotoTagVisibilityMO'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'gototagvisibilitymo', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_GotoTagVisibilityMO(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/GotoTagVisibilityMO.py
# BEGIN Xcos/blocks/Ground.py


def Ground(outroot, attribid, ordering, geometry, parameters):
    func_name = 'Ground'
    parameters = [""]
    outnode = addOutNode(outroot, BLOCK_GROUND,
                         attribid, ordering, 1,
                         func_name, 'Ground', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)
    addTypeNode(outnode, TYPE_DOUBLE, AS_REAL_PARAM, 0,
                [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_INT_PARAM, 0,
                [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_OBJ_PARAM, parameters)
    array = ['0']
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NBZERO, 1, array)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NMODE, 1, array)
    addTypeNode(outnode, TYPE_DOUBLE, AS_STATE, 0, [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_DSTATE, 0, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_ODSTATE, parameters)
    equationsArrayNode = addObjNode(outnode, TYPE_ARRAY,
                                    CLASS_TLIST, AS_EQUATIONS, parameters)
    scilabStringParameters = ["modelica", "model",
                              "inputs", "outputs",
                              "parameters"]
    addScilabStringNode(equationsArrayNode, width=5,
                        parameters=scilabStringParameters)
    param = ['Ground']
    addSciStringNode(equationsArrayNode, 1, param)

    param1 = ["p"]
    addSciStringNode(equationsArrayNode, 1, param1)
    addScilabDBNode(equationsArrayNode, 0)
    innerArrayNode = addArrayNode(equationsArrayNode,
                                  scilabClass="ScilabList")
    addScilabDBNode(innerArrayNode, 0)
    addArrayNode(innerArrayNode, scilabClass="ScilabList")
    addgeometryNode(outnode, GEOMETRY, geometry['height'],
                    geometry['width'], geometry['x'], geometry['y'])

    return outnode


def get_from_Ground(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/Ground.py
# BEGIN Xcos/blocks/Gyrator.py


def Gyrator(outroot, attribid, ordering, geometry, parameters):
    func_name = 'Gyrator'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'Gyrator', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_Gyrator(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/Gyrator.py
# BEGIN Xcos/blocks/HALT_f.py


def HALT_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'HALT_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'hltblk', 'DEFAULT',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_HALT_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/HALT_f.py
# BEGIN Xcos/blocks/HYSTHERESIS.py


def HYSTHERESIS(outroot, attribid, ordering, geometry, parameters):
    func_name = 'HYSTHERESIS'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'hystheresis', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 5, parameters)

    return outnode


def get_from_HYSTHERESIS(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/HYSTHERESIS.py
# BEGIN Xcos/blocks/IFTHEL_f.py


def IFTHEL_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'IFTHEL_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'ifthel', 'IFTHENELSE',
                         func_name, BLOCKTYPE_L,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_IFTHEL_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = 1 if float(parameters[0]) == 1.0 else 0
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/IFTHEL_f.py
# BEGIN Xcos/blocks/INIMPL_f.py


def INIMPL_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'INIMPL_f'

    outnode = addOutNode(outroot, BLOCK_IMPLICIT_IN,
                         attribid, ordering, 1,
                         func_name, 'inimpl', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_INIMPL_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/INIMPL_f.py
# BEGIN Xcos/blocks/INTEGRAL_f.py


def INTEGRAL_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'INTEGRAL_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'integr', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_INTEGRAL_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/INTEGRAL_f.py
# BEGIN Xcos/blocks/INTEGRAL_m.py


def INTEGRAL_m(outroot, attribid, ordering, geometry, parameters):
    func_name = 'INTEGRAL_m'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'integral_func', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 5, parameters)

    return outnode


def get_from_INTEGRAL_m(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = 2 if parameters[1] == '1' else 1
    iiv = ''
    con = 1 if parameters[1] == '1' else 0
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/INTEGRAL_m.py
# BEGIN Xcos/blocks/INTMUL.py


def INTMUL(outroot, attribid, ordering, geometry, parameters):
    func_name = 'INTMUL'

    datatype = ['', '', '', 'i32', 'i16', 'i8', 'ui32', 'ui16', 'ui8']
    para1 = int(float(parameters[0]))
    para2 = int(float(parameters[1]))

    if para2 == 1:
        overflow = 's'
    elif para2 == 2:
        overflow = 'e'
    else:
        overflow = 'n'

    simulation_func_name = 'matmul_' + datatype[para1] + overflow

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_INTMUL(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/INTMUL.py
# BEGIN Xcos/blocks/INTRP2BLK_f.py


def INTRP2BLK_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'INTRP2BLK_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'intrp2', 'TYPE_1',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_INTRP2BLK_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/INTRP2BLK_f.py
# BEGIN Xcos/blocks/INTRPLBLK_f.py


def INTRPLBLK_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'INTRPLBLK_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'intrpl', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_INTRPLBLK_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/INTRPLBLK_f.py
# BEGIN Xcos/blocks/INVBLK.py


def INVBLK(outroot, attribid, ordering, geometry, parameters):
    func_name = 'INVBLK'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'invblk4', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_INVBLK(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/INVBLK.py
# BEGIN Xcos/blocks/IN_f.py


def IN_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'IN_f'

    outnode = addOutNode(outroot, BLOCK_EXPLICIT_IN,
                         attribid, ordering, 1,
                         func_name, 'input', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_IN_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/IN_f.py
# BEGIN Xcos/blocks/ISELECT_m.py


def ISELECT_m(outroot, attribid, ordering, geometry, parameters):
    func_name = 'ISELECT_m'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'selector_m', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_ISELECT_m(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = int(float(parameters[1]))
    eov = int(float(parameters[1]))
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/ISELECT_m.py
# BEGIN Xcos/blocks/IdealTransformer.py


def IdealTransformer(outroot, attribid, ordering, geometry, parameters):
    func_name = 'IdealTransformer'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'IdealTransformer', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_IdealTransformer(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/IdealTransformer.py
# BEGIN Xcos/blocks/Inductor.py


def Inductor(outroot, attribid, ordering, geometry, parameters):
    func_name = 'Inductor'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'Inductor', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_Inductor(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = si_format(parameters[0])

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/Inductor.py
# BEGIN Xcos/blocks/JKFLIPFLOP.py


def JKFLIPFLOP(outroot, attribid, ordering, geometry, parameters):
    func_name = 'JKFLIPFLOP'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_H,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_JKFLIPFLOP(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/JKFLIPFLOP.py
# BEGIN Xcos/blocks/LOGBLK_f.py


def LOGBLK_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'LOGBLK_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'logblk', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_LOGBLK_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/LOGBLK_f.py
# BEGIN Xcos/blocks/LOGIC.py


def LOGIC(outroot, attribid, ordering, geometry, parameters):
    func_name = 'LOGIC'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'logic', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_LOGIC(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''
    inputs = parameters[0].split(';')

    eiv = int(math.log2(len(inputs)))
    iiv = ''
    con = 1 if parameters[1] == '0' else 0
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/LOGIC.py
# BEGIN Xcos/blocks/LOGICAL_OP.py


def LOGICAL_OP(outroot, attribid, ordering, geometry, parameters):
    func_name = 'LOGICAL_OP'

    d_type = ['', '', '', 'i32', 'i16', 'i8', 'ui32', 'ui16', 'ui8']

    para3 = int(float(parameters[2]))

    if para3 != 1:
        datatype = '_' + d_type[para3]
    else:
        datatype = ''

    simulation_func_name = 'logicalop' + datatype

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 4, parameters)

    return outnode


def get_from_LOGICAL_OP(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    logical_operators = ['AND', 'OR', 'NAND', 'NOR', 'XOR', 'NOT']
    display_parameter = logical_operators[int(float(parameters[1]))]

    eiv = int(float(parameters[0]))
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/LOGICAL_OP.py
# BEGIN Xcos/blocks/LOOKUP_f.py


def LOOKUP_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'LOOKUP_f'
    para = parameters[0].split(' ')

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'lookup', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    node = addNode(outnode, TYPE_STRING, height=1, width=len(para))

    for i in range(len(para)):
        addData(node, i, 0, para[i])

    return outnode


def get_from_LOOKUP_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/LOOKUP_f.py
# BEGIN Xcos/blocks/MATBKSL.py


def MATBKSL(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATBKSL'

    data_type = ['', 'mat_bksl', 'matz_bksl']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_MATBKSL(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATBKSL.py
# BEGIN Xcos/blocks/MATCATH.py


def MATCATH(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATCATH'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'mat_cath', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_MATCATH(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = int(float(parameters[0]))
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATCATH.py
# BEGIN Xcos/blocks/MATCATV.py


def MATCATV(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATCATV'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'mat_catv', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_MATCATV(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = int(float(parameters[0]))
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATCATV.py
# BEGIN Xcos/blocks/MATDET.py


def MATDET(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATDET'

    data_type = ['', 'mat_det', 'matz_det']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_MATDET(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATDET.py
# BEGIN Xcos/blocks/MATDIAG.py


def MATDIAG(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATDIAG'

    data_type = ['', 'mat_diag', 'matz_diag']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_MATDIAG(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATDIAG.py
# BEGIN Xcos/blocks/MATDIV.py


def MATDIV(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATDIV'

    data_type = ['', 'mat_div', 'matz_div']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_MATDIV(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATDIV.py
# BEGIN Xcos/blocks/MATEIG.py


def MATEIG(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATEIG'

    data_type = ['', 'mat_', 'matz_']
    decomposition_type = ['', 'vps', 'vpv']
    para1 = int(parameters[0])
    para2 = int(parameters[1])

    simulation_func_name = data_type[para1] + decomposition_type[para2]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_MATEIG(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = int(parameters[1])
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATEIG.py
# BEGIN Xcos/blocks/MATEXPM.py


def MATEXPM(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATEXPM'

    data_type = ['', 'mat_expm', 'matz_expm']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_MATEXPM(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATEXPM.py
# BEGIN Xcos/blocks/MATINV.py


def MATINV(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATINV'

    data_type = ['', 'mat_inv', 'matz_inv']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_MATINV(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATINV.py
# BEGIN Xcos/blocks/MATLU.py


def MATLU(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATLU'

    data_type = ['', 'mat_lu', 'matz_lu']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_MATLU(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATLU.py
# BEGIN Xcos/blocks/MATMAGPHI.py


def MATMAGPHI(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATMAGPHI'

    data_type = ['', 'matz_abs', 'matz_absc']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_MATMAGPHI(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = int(parameters[0])
    iiv = ''
    con = ''
    eov = 2 if parameters[0] == '1' else 1
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATMAGPHI.py
# BEGIN Xcos/blocks/MATMUL.py


def MATMUL(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATMUL'

    data_type = ['', 'matmul_m', 'matzmul_m',
                 'matmul_i32', 'matmul_i16', 'matmul_i8',
                 'matmul_ui32', 'matmul_ui16', 'matmul_ui8']
    overflow = ['n', 's', 'e']

    para1 = int(float(parameters[0]))
    para2 = int(float(parameters[1]))
    para3 = int(float(parameters[2]))

    if para2 == 1:
        if para1 == 1 or para1 == 2:
            simulation_func_name = data_type[para1]
        else:
            simulation_func_name = data_type[para1] + overflow[para3]
    elif para2 == 2:
        if para3 == 2:
            if para1 != 2:
                simulation_func_name = 'matmul2_m'
            else:
                simulation_func_name = 'mutmul2_e'
        elif para3 == 1:
            simulation_func_name = 'matmul2_s'
        else:
            simulation_func_name = 'matmul2_m'
    elif para2 == 3:
        if para1 != 2:
            if para3 == 1 or para3 == 2:
                simulation_func_name = 'matbyscal_' + overflow[para3]
            else:
                simulation_func_name = ''
        else:
            simulation_func_name = 'matbyscal'
    else:
        simulation_func_name = ''

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_MATMUL(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATMUL.py
# BEGIN Xcos/blocks/MATPINV.py


def MATPINV(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATPINV'

    data_type = ['', 'mat_pinv', 'matz_pinv']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_MATPINV(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATPINV.py
# BEGIN Xcos/blocks/MATRESH.py


def MATRESH(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATRESH'

    data_type = ['', 'mat_reshape', 'matz_reshape']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_MATRESH(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATRESH.py
# BEGIN Xcos/blocks/MATSING.py


def MATSING(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATSING'

    data_type = ['', 'mat_', 'matz_']
    decomposition_type = ['', 'sing', 'svd']
    para1 = int(parameters[0])
    para2 = int(parameters[1])

    simulation_func_name = data_type[para1] + decomposition_type[para2]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_MATSING(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = 3 if parameters[1] == '2' else 1
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATSING.py
# BEGIN Xcos/blocks/MATSUM.py


def MATSUM(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATSUM'

    data_type = ['', 'mat_', 'matz_']
    sum_along = ['sum', 'sumc', 'suml']
    para1 = int(parameters[0])
    para2 = int(parameters[1])

    simulation_func_name = data_type[para1] + sum_along[para2]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_MATSUM(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATSUM.py
# BEGIN Xcos/blocks/MATTRAN.py


def MATTRAN(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATTRAN'

    data_type = ['', 'mattran_m', 'matztran_m']

    para1 = int(parameters[0])
    para2 = int(parameters[1])

    if para2 == 2 and para1 == 2:
        simulation_func_name = 'mathermit_m'
    else:
        simulation_func_name = data_type[para1]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_MATTRAN(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATTRAN.py
# BEGIN Xcos/blocks/MATZCONJ.py


def MATZCONJ(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATZCONJ'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'matz_conj', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_MATZCONJ(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATZCONJ.py
# BEGIN Xcos/blocks/MATZREIM.py


def MATZREIM(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATZREIM'

    data_type = ['', 'matz_reim', 'matz_reimc']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_MATZREIM(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = int(parameters[0])
    iiv = ''
    con = ''
    eov = 2 if parameters[0] == '1' else 1
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MATZREIM.py
# BEGIN Xcos/blocks/MAXMIN.py


def MAXMIN(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MAXMIN'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'minmax', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_MAXMIN(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = 'MIN' if parameters[0] == '1' else 'MAX'

    eiv = 1 if parameters[1] == '1' else 2
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MAXMIN.py
# BEGIN Xcos/blocks/MAX_f.py


def MAX_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MAX_f'
    parameters = [' ']

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'maxblk', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_MAX_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MAX_f.py
# BEGIN Xcos/blocks/MBLOCK.py


def MBLOCK(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MBLOCK'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cscope', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 0, parameters)

    return outnode


def get_from_MBLOCK(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MBLOCK.py
# BEGIN Xcos/blocks/MCLOCK_f.py


def MCLOCK_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MCLOCK_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_H)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_MCLOCK_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MCLOCK_f.py
# BEGIN Xcos/blocks/MFCLCK_f.py


def MFCLCK_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MFCLCK_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'mfclck', 'DEFAULT',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_MFCLCK_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MFCLCK_f.py
# BEGIN Xcos/blocks/MIN_f.py


def MIN_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MIN_f'
    parameters = ['-1']

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'minblk', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_MIN_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MIN_f.py
# BEGIN Xcos/blocks/MUX.py


def MUX(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MUX'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'multiplex', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_MUX(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = int(float(parameters[0]))
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MUX.py
# BEGIN Xcos/blocks/MUX_f.py


def MUX_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MUX_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'mux', 'TYPE_1',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_MUX_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = int(float(parameters[0]))
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/MUX_f.py
# BEGIN Xcos/blocks/M_SWITCH.py


def M_SWITCH(outroot, attribid, ordering, geometry, parameters):
    func_name = 'M_SWITCH'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'mswitch', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_M_SWITCH(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = int(float(parameters[0])) + 1
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/M_SWITCH.py
# BEGIN Xcos/blocks/M_freq.py


def M_freq(outroot, attribid, ordering, geometry, parameters):
    func_name = 'M_freq'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'm_frequ', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_M_freq(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''
    inputs = parameters[0].split(';')

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = (len(inputs)**2)-1

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/M_freq.py
# BEGIN Xcos/blocks/Modulo_Count.py


def Modulo_Count(outroot, attribid, ordering, geometry, parameters):
    func_name = 'Modulo_Count'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'modulo_count', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_Modulo_Count(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[1]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/Modulo_Count.py
# BEGIN Xcos/blocks/NEGTOPOS_f.py


def NEGTOPOS_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'NEGTOPOS_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'zcross', 'TYPE_1',
                         func_name, BLOCKTYPE_Z,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_NEGTOPOS_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/NEGTOPOS_f.py
# BEGIN Xcos/blocks/NMOS.py


def NMOS(outroot, attribid, ordering, geometry, parameters):
    func_name = 'NMOS'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'NMOS', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 9, parameters)

    return outnode


def get_from_NMOS(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/NMOS.py
# BEGIN Xcos/blocks/NPN.py


def NPN(outroot, attribid, ordering, geometry, parameters):
    func_name = 'NPN'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'NPN', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 17, parameters)

    return outnode


def get_from_NPN(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/NPN.py
# BEGIN Xcos/blocks/NRMSOM_f.py


def NRMSOM_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'NRMSOM_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'junk', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_NRMSOM_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = int(float(parameters[0]))
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/NRMSOM_f.py
# BEGIN Xcos/blocks/OUTIMPL_f.py


def OUTIMPL_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'OUTIMPL_f'

    outnode = addOutNode(outroot, BLOCK_IMPLICIT_OUT,
                         attribid, ordering, 1,
                         func_name, 'outimpl', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_OUTIMPL_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/OUTIMPL_f.py
# BEGIN Xcos/blocks/OUT_f.py


def OUT_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'OUT_f'

    outnode = addOutNode(outroot, BLOCK_EXPLICIT_OUT,
                         attribid, ordering, 1,
                         func_name, 'output', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_OUT_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/OUT_f.py
# BEGIN Xcos/blocks/OpAmp.py


def OpAmp(outroot, attribid, ordering, geometry, parameters):
    func_name = 'OpAmp'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'OpAmp', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)
    addTypeNode(outnode, TYPE_DOUBLE, AS_REAL_PARAM, 0,
                [])
    array = ['0']
    addTypeNode(outnode, TYPE_DOUBLE, AS_INT_PARAM, 0,
                [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_OBJ_PARAM, parameters)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NBZERO, 1, array)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NMODE, 1, array)
    addTypeNode(outnode, TYPE_DOUBLE, AS_STATE, 0, [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_DSTATE, 0, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_ODSTATE, parameters)
    equationsArrayNode = addObjNode(outnode, TYPE_ARRAY,
                                    CLASS_TLIST, AS_EQUATIONS, parameters)
    # Add ScilabString nodes to equationsArrayNode
    scilabStringParameters = ["modelica", "model",
                              "inputs", "outputs",
                              "parameters"]
    addScilabStringNode(equationsArrayNode, width=5,
                        parameters=scilabStringParameters)
    param = ['OpAmp']
    addSciStringNode(equationsArrayNode, 1, param)

    param1 = ["in_p", "in_n"]
    addSciStringNode(equationsArrayNode, 2, param1)
    param = ['out']
    addSciStringNode(equationsArrayNode, 1, param)
    # Create the inner Array node for ScilabList
    innerArrayNode = addArrayNode(equationsArrayNode,
                                  scilabClass="ScilabList")
    addScilabDBNode(innerArrayNode, height=0)
    addScilabDBNode(innerArrayNode, height=0)

    addgeometryNode(outnode, GEOMETRY, geometry['height'],
                    geometry['width'], geometry['x'], geometry['y'])

    return outnode


def get_from_OpAmp(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/OpAmp.py
# BEGIN Xcos/blocks/PDE.py


def PDE(outroot, attribid, ordering, geometry, parameters):
    func_name = 'PDE'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cscope', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 0, parameters)

    return outnode


def get_from_PDE(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/PDE.py
# BEGIN Xcos/blocks/PID.py


def PID(outroot, attribid, ordering, geometry, parameters):
    func_name = 'PID'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_H)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_PID(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/PID.py
# BEGIN Xcos/blocks/PMOS.py


def PMOS(outroot, attribid, ordering, geometry, parameters):
    func_name = 'PMOS'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'PMOS', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 9, parameters)

    return outnode


def get_from_PMOS(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/PMOS.py
# BEGIN Xcos/blocks/PNP.py


def PNP(outroot, attribid, ordering, geometry, parameters):
    func_name = 'PNP'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'PNP', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 17, parameters)

    return outnode


def get_from_PNP(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/PNP.py
# BEGIN Xcos/blocks/POSTONEG_f.py


def POSTONEG_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'POSTONEG_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'zcross', 'TYPE_1',
                         func_name, BLOCKTYPE_Z,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_POSTONEG_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/POSTONEG_f.py
# BEGIN Xcos/blocks/POWBLK_f.py


def POWBLK_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'POWBLK_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'powblk', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_POWBLK_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/POWBLK_f.py
# BEGIN Xcos/blocks/PRODUCT.py


def PRODUCT(outroot, attribid, ordering, geometry, parameters):
    func_name = 'PRODUCT'

    outnode = addOutNode(outroot, BLOCK_PRODUCT,
                         attribid, ordering, 1,
                         func_name, 'product', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_PRODUCT(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''
    inputs = parameters[0].split(';')

    eiv = len(inputs)
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/PRODUCT.py
# BEGIN Xcos/blocks/PROD_f.py


def PROD_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'PROD_f'

    outnode = addOutNode(outroot, BLOCK_ROUND,
                         attribid, ordering, 1,
                         func_name, 'prod', 'TYPE_2',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_PROD_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/PROD_f.py
# BEGIN Xcos/blocks/PULSE_SC.py


def PULSE_SC(outroot, attribid, ordering, geometry, parameters):
    func_name = 'PULSE_SC'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_H)

    addExprsNode(outnode, TYPE_STRING, 4, parameters)

    return outnode


def get_from_PULSE_SC(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/PULSE_SC.py
# BEGIN Xcos/blocks/PerteDP.py


def PerteDP(outroot, attribid, ordering, geometry, parameters):
    func_name = 'PerteDP'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'PerteDP', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 6, parameters)

    return outnode


def get_from_PerteDP(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/PerteDP.py
# BEGIN Xcos/blocks/PotentialSensor.py


def PotentialSensor(outroot, attribid, ordering, geometry, parameters):
    func_name = 'PotentialSensor'
    parameters = ['']

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'PotentialSensor', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_PotentialSensor(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/PotentialSensor.py
# BEGIN Xcos/blocks/PuitsP.py


def PuitsP(outroot, attribid, ordering, geometry, parameters):
    func_name = 'PuitsP'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'Puits', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 4, parameters)

    return outnode


def get_from_PuitsP(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/PuitsP.py
# BEGIN Xcos/blocks/QUANT_f.py


def QUANT_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'QUANT_f'

    data_type = ['', 'qzrnd', 'qztrn', 'qzflr', 'qzcel']

    simulation_func_name = data_type[int(parameters[1])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_QUANT_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/QUANT_f.py
# BEGIN Xcos/blocks/RAMP.py


def RAMP(outroot, attribid, ordering, geometry, parameters):
    func_name = 'RAMP'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'ramp', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_RAMP(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/RAMP.py
# BEGIN Xcos/blocks/RAND_m.py


def RAND_m(outroot, attribid, ordering, geometry, parameters):
    func_name = 'RAND_m'

    data_type = ['', 'rndblk_m', 'rndblkz_m']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 5, parameters)

    return outnode


def get_from_RAND_m(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/RAND_m.py
# BEGIN Xcos/blocks/RATELIMITER.py


def RATELIMITER(outroot, attribid, ordering, geometry, parameters):
    func_name = 'RATELIMITER'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'ratelimiter', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_RATELIMITER(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/RATELIMITER.py
# BEGIN Xcos/blocks/READAU_f.py


def READAU_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'READAU_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'readau', 'TYPE_2',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_READAU_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/READAU_f.py
# BEGIN Xcos/blocks/READC_f.py


def READC_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'READC_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'readc', 'TYPE_2',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 8, parameters)

    return outnode


def get_from_READC_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    temp = parameters[0]
    temp = temp.replace('[', '')
    temp = temp.replace(']', '')

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = 1 if len(temp) > 0 else 0

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/READC_f.py
# BEGIN Xcos/blocks/REGISTER.py


def REGISTER(outroot, attribid, ordering, geometry, parameters):
    func_name = 'REGISTER'

    data_type = ['', '', '', '_i32', '_i16', '_i8', '_ui32', '_ui16', '_ui8']

    para2 = int(parameters[1])

    if para2 >= 3:
        simulation_func_name = 'delay4' + data_type[para2]
    else:
        simulation_func_name = 'delay4'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_REGISTER(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/REGISTER.py
# BEGIN Xcos/blocks/RELATIONALOP.py


def RELATIONALOP(outroot, attribid, ordering, geometry, parameters):
    func_name = 'RELATIONALOP'

    data_type = ['', '', '', '_i32', '_i16', '_i8', '_ui32', '_ui16', '_ui8']

    para3 = int(parameters[2])

    if para3 >= 3:
        simulation_func_name = 'relational_op' + data_type[para3]
    else:
        simulation_func_name = 'relational_op'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_RELATIONALOP(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    operators = ['==', '~=', '<', '<=', '>', '>=']
    display_parameter = operators[int(float(parameters[0]))]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/RELATIONALOP.py
# BEGIN Xcos/blocks/RELAY_f.py


def RELAY_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'RELAY_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'relay', 'TYPE_2',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1',
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_RELAY_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = int(float(parameters[0]))
    iiv = ''
    con = int(float(parameters[0]))
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/RELAY_f.py
# BEGIN Xcos/blocks/RFILE_f.py


def RFILE_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'RFILE_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'readf', 'DEFAULT',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 5, parameters)

    return outnode


def get_from_RFILE_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''
    temp = parameters[0]
    temp = temp.replace('[', '')
    temp = temp.replace(']', '')

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = 1 if len(temp) > 0 else 0

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/RFILE_f.py
# BEGIN Xcos/blocks/RICC.py


def RICC(outroot, attribid, ordering, geometry, parameters):
    func_name = 'RICC'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'ricc_m', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_RICC(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/RICC.py
# BEGIN Xcos/blocks/ROOTCOEF.py


def ROOTCOEF(outroot, attribid, ordering, geometry, parameters):
    func_name = 'ROOTCOEF'

    data_type = ['', 'root_coef', 'rootz_coef']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_ROOTCOEF(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/ROOTCOEF.py
# BEGIN Xcos/blocks/Resistor.py


def Resistor(outroot, attribid, ordering, geometry, parameters):
    func_name = 'Resistor'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'resistor', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)
    addSciDBNode(outnode, TYPE_DOUBLE, AS_REAL_PARAM,
                 1, realParts=[10000.0])
    array = ['0']
    addTypeNode(outnode, TYPE_DOUBLE, AS_INT_PARAM, 0,
                [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_OBJ_PARAM, parameters)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NBZERO, 1, array)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NMODE, 1, array)
    addTypeNode(outnode, TYPE_DOUBLE, AS_STATE, 0, [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_DSTATE, 0, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_ODSTATE, parameters)
    equationsArrayNode = addObjNode(outnode, TYPE_ARRAY,
                                    CLASS_TLIST, AS_EQUATIONS, parameters)
    scilabStringParameters = ["modelica", "model",
                              "inputs", "outputs",
                              "parameters"]
    addScilabStringNode(equationsArrayNode, width=5,
                        parameters=scilabStringParameters)
    param = ['Resistor']
    addSciStringNode(equationsArrayNode, 1, param)

    param1 = ["p"]
    addSciStringNode(equationsArrayNode, 1, param1)
    param = ["n"]
    addSciStringNode(equationsArrayNode, 1, param)
    innerArrayNode = addArrayNode(equationsArrayNode,
                                  scilabClass="ScilabList")
    scilabStringParameters = ["R"]
    addSciStringNode(innerArrayNode, height=1,
                     parameters=scilabStringParameters)

    innerNode = addArrayNode(innerArrayNode,
                             scilabClass="ScilabList")
    addScilabDoubleNode(innerNode, width=1, realParts=["10000.0"])
    addgeometryNode(outnode, GEOMETRY, geometry['height'],
                    geometry['width'], geometry['x'], geometry['y'])

    return outnode


def get_from_Resistor(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = si_format(parameters[0])

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/Resistor.py
# BEGIN Xcos/blocks/SAMPHOLD_m.py


def SAMPHOLD_m(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SAMPHOLD_m'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'samphold4_m', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_SAMPHOLD_m(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SAMPHOLD_m.py
# BEGIN Xcos/blocks/SATURATION.py


def SATURATION(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SATURATION'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'satur', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_SATURATION(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SATURATION.py
# BEGIN Xcos/blocks/SAWTOOTH_f.py


def SAWTOOTH_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SAWTOOTH_f'
    parameters = [' ']

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'sawtth', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_SAWTOOTH_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SAWTOOTH_f.py
# BEGIN Xcos/blocks/SCALAR2VECTOR.py


def SCALAR2VECTOR(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SCALAR2VECTOR'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'scalar2vector', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_SCALAR2VECTOR(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SCALAR2VECTOR.py
# BEGIN Xcos/blocks/SELECT_m.py


def SELECT_m(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SELECT_m'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'selector_m', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_SELECT_m(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[10]

    eiv = int(float(parameters[1]))
    iiv = ''
    con = int(float(parameters[1]))
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SELECT_m.py
# BEGIN Xcos/blocks/SELF_SWITCH.py


def SELF_SWITCH(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SELF_SWITCH'
    if parameters[0] == 'on':
        style = func_name + '_ON'
    else:
        style = func_name + '_OFF'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         style, BLOCKTYPE_H)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_SELF_SWITCH(cell):
    style = cell.attrib['style']
    if style == 'SELF_SWITCH_ON':
        value = 'on'
    else:
        value = 'off'

    parameters = [value]

    style = cell.attrib.get('style')
    display_parameter = 'on' if style == 'SELF_SWITCH_ON' else 'off'

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SELF_SWITCH.py
# BEGIN Xcos/blocks/SHIFT.py


def SHIFT(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SHIFT'

    data_type = ['', '', '',
                 'shift_32_', 'shift_16_', 'shift_8_',
                 'shift_32_', 'shift_16_', 'shift_8_']
    shift_type = ['A', 'C']

    para1 = int(parameters[0])
    bits_to_shift = int(parameters[1])
    para3 = int(parameters[2])

    if bits_to_shift != 0:
        if bits_to_shift > 0:
            simulation_func_name = data_type[para1] + 'L' + shift_type[para3]
        else:
            simulation_func_name = data_type[para1] + 'R' + shift_type[para3]
    else:
        simulation_func_name = 'shift_32_LA'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_SHIFT(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[1]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SHIFT.py
# BEGIN Xcos/blocks/SIGNUM.py


def SIGNUM(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SIGNUM'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'signum', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_SIGNUM(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SIGNUM.py
# BEGIN Xcos/blocks/SINBLK_f.py


def SINBLK_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SINBLK_f'
    parameters = [' ']

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'sinblk', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_SINBLK_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SINBLK_f.py
# BEGIN Xcos/blocks/SOM_f.py


def SOM_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SOM_f'
    parameters = ['1', '[1;1;1]']

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'sum', 'TYPE_2',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_SOM_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SOM_f.py
# BEGIN Xcos/blocks/SQRT.py


def SQRT(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SQRT'

    data_type = ['', 'mat_sqrt', 'matz_sqrt']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_SQRT(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SQRT.py
# BEGIN Xcos/blocks/SRFLIPFLOP.py


def SRFLIPFLOP(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SRFLIPFLOP'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_H,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_SRFLIPFLOP(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SRFLIPFLOP.py
# BEGIN Xcos/blocks/STEP_FUNCTION.py


def STEP_FUNCTION(outroot, attribid, ordering, geometry, parameters):
    func_name = 'STEP_FUNCTION'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_STEP_FUNCTION(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/STEP_FUNCTION.py
# BEGIN Xcos/blocks/SUBMAT.py


def SUBMAT(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SUBMAT'

    data_type = ['', 'submat', 'submatz']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 6, parameters)

    return outnode


def get_from_SUBMAT(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SUBMAT.py
# BEGIN Xcos/blocks/SUMMATION.py


def SUMMATION(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SUMMATION'

    data_type = ['', '', '_z', '_i32', '_i16', '_i8', '_ui32', '_ui16', '_ui8']
    overflow = ['n', 's', 'e']

    para1 = int(float(parameters[0]))
    para3 = int(float(parameters[2]))

    if para1 == 1 or para1 == 2:
        simulation_func_name = 'summation' + data_type[para1]
    else:
        simulation_func_name = 'summation' + data_type[para1] + overflow[para3]

    outnode = addOutNode(outroot, BLOCK_SUMMATION,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_SUMMATION(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''
    inputs = parameters[1].split(';')

    eiv = len(inputs)
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SUMMATION.py
# BEGIN Xcos/blocks/SUM_f.py


def SUM_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SUM_f'

    outnode = addOutNode(outroot, BLOCK_ROUND,
                         attribid, ordering, 1,
                         func_name, 'plusblk', 'TYPE_2',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_SUM_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SUM_f.py
# BEGIN Xcos/blocks/SUPER_f.py


def SUPER_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SUPER_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cscope', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 0, parameters)

    return outnode


def get_from_SUPER_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SUPER_f.py
# BEGIN Xcos/blocks/SWITCH2_m.py


def SWITCH2_m(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SWITCH2_m'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'switch2_m', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 4, parameters)

    return outnode


def get_from_SWITCH2_m(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SWITCH2_m.py
# BEGIN Xcos/blocks/SWITCH_f.py


def SWITCH_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SWITCH_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'switchn', 'TYPE_2',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1',
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_SWITCH_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[1]

    eiv = int(float(parameters[0]))
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SWITCH_f.py
# BEGIN Xcos/blocks/SampleCLK.py


def SampleCLK(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SampleCLK'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'sampleclk', 'DEFAULT',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_SampleCLK(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SampleCLK.py
# BEGIN Xcos/blocks/Sigbuilder.py


def Sigbuilder(outroot, attribid, ordering, geometry, parameters):
    func_name = 'Sigbuilder'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_H)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_Sigbuilder(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/Sigbuilder.py
# BEGIN Xcos/blocks/SineVoltage.py


def SineVoltage(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SineVoltage'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'SineVoltage', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 5, parameters)
    addSciDBNode(outnode, TYPE_DOUBLE, AS_REAL_PARAM,
                 5, realParts=[1.5, 0.0, 15.92356687898089, 0.0, 0.0])
    array = ['0']
    addTypeNode(outnode, TYPE_DOUBLE, AS_INT_PARAM, 0,
                [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_OBJ_PARAM, parameters)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NBZERO, 1, array)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NMODE, 1, array)
    addTypeNode(outnode, TYPE_DOUBLE, AS_STATE, 0, [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_DSTATE, 0, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_ODSTATE, parameters)
    equationsArrayNode = addObjNode(outnode, TYPE_ARRAY,
                                    CLASS_TLIST, AS_EQUATIONS, parameters)
    # Add ScilabString nodes to equationsArrayNode
    scilabStringParameters = ["modelica", "model",
                              "inputs", "outputs",
                              "parameters"]
    addScilabStringNode(equationsArrayNode, width=5,
                        parameters=scilabStringParameters)
    param = ['SineVoltage']
    addSciStringNode(equationsArrayNode, 1, param)

    param1 = ["p"]
    addSciStringNode(equationsArrayNode, 1, param1)
    param = ["n"]
    addSciStringNode(equationsArrayNode, 1, param)
    # Create the inner Array node for ScilabList
    innerArrayNode = addArrayNode(equationsArrayNode,
                                  scilabClass="ScilabList")
    scilabStringParameters = ["V", "phase",
                              "freqHz", "offset",
                              "startTime"]
    addSciStringNode(innerArrayNode, height=5,
                     parameters=scilabStringParameters)
    nestedArrayNode = addArrayNode(innerArrayNode, scilabClass="ScilabList")
    addScilabDoubleNode(nestedArrayNode, width=1, realParts=["1.5"])
    addScilabDoubleNode(nestedArrayNode, width=1, realParts=["0.0"])
    addScilabDoubleNode(nestedArrayNode, width=1, realParts=["15.92356687898089"])
    addScilabDoubleNode(nestedArrayNode, width=1, realParts=["0.0"])
    addScilabDoubleNode(nestedArrayNode, width=1, realParts=["0.0"])

    addgeometryNode(outnode, GEOMETRY, geometry['height'],
                    geometry['width'], geometry['x'], geometry['y'])

    return outnode


def get_from_SineVoltage(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0] + ',' + parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SineVoltage.py
# BEGIN Xcos/blocks/SourceP.py


def SourceP(outroot, attribid, ordering, geometry, parameters):
    func_name = 'SourceP'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'Source', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 4, parameters)

    return outnode


def get_from_SourceP(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SourceP.py
# BEGIN Xcos/blocks/SplitBlock.py


def SplitBlock(outroot, attribid, ordering, geometry):
    outnode = addOutNode(outroot, BLOCK_SPLIT,
                         attribid, ordering, 1,
                         None, None, 'DEFAULT',
                         '', None,
                         value='',
                         connectable=0,
                         vertex=1)
    addExprsNode(outnode, TYPE_DOUBLE, 0, [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_REAL_PARAM, 0,
                [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_INT_PARAM, 0, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_OBJ_PARAM, [])
    array = ['0']
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NBZERO, 1, array)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NMODE, 1, array)
    addTypeNode(outnode, TYPE_DOUBLE, AS_STATE, 0, [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_DSTATE, 0, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_ODSTATE, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_EQUATIONS, [])
    addNode(outnode, 'mxGeometry', **{'as': 'geometry'},
            height=geometry['height'], width=geometry['width'],
            x=geometry['x'], y=geometry['y'])

    return outnode


def get_from_SplitBlock(cell):
    parameters = []

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/SplitBlock.py
# BEGIN Xcos/blocks/Switch.py


def Switch(outroot, attribid, ordering, geometry, parameters):
    func_name = 'Switch'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'Switch', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_Switch(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/Switch.py
# BEGIN Xcos/blocks/TANBLK_f.py


def TANBLK_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'TANBLK_f'
    parameters = ['-1']

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'tanblk', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_TANBLK_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/TANBLK_f.py
# BEGIN Xcos/blocks/TCLSS.py


def TCLSS(outroot, attribid, ordering, geometry, parameters):
    func_name = 'TCLSS'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'tcslti4', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 5, parameters)

    return outnode


def get_from_TCLSS(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/TCLSS.py
# BEGIN Xcos/blocks/TEXT_f.py


def TEXT_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'TEXT_f'

    outnode = addOutNode(outroot, BLOCK_TEXT,
                         attribid, ordering, 1,
                         func_name, None, None,
                         func_name, None,
                         value=parameters[0])

    return outnode


def get_from_TEXT_f(cell):
    parameters = [cell.attrib['value']]

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/TEXT_f.py
# BEGIN Xcos/blocks/TIME_DELAY.py


def TIME_DELAY(outroot, attribid, ordering, geometry, parameters):
    func_name = 'TIME_DELAY'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'time_delay', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_X,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_TIME_DELAY(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/TIME_DELAY.py
# BEGIN Xcos/blocks/TIME_f.py


def TIME_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'TIME_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'timblk', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnT='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_TIME_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/TIME_f.py
# BEGIN Xcos/blocks/TKSCALE.py


def TKSCALE(outroot, attribid, ordering, geometry, parameters):
    func_name = 'TKSCALE'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'tkscaleblk', 'SCILAB',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_TKSCALE(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/TKSCALE.py
# BEGIN Xcos/blocks/TOWS_c.py


def TOWS_c(outroot, attribid, ordering, geometry, parameters):
    func_name = 'TOWS_c'

    para3 = int(parameters[2])

    if para3 == 1:
        b_type = BLOCKTYPE_X
    else:
        b_type = BLOCKTYPE_D

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'tows_c', 'C_OR_FORTRAN',
                         func_name, b_type)

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_TOWS_c(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[1] + ',' + parameters[0]

    eiv = ''
    iiv = ''
    con = 1 if parameters[2] == '0' else 0
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/TOWS_c.py
# BEGIN Xcos/blocks/TRASH_f.py


def TRASH_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'TRASH_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'trash', 'DEFAULT',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 0, parameters)

    return outnode


def get_from_TRASH_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/TRASH_f.py
# BEGIN Xcos/blocks/TrigFun.py


def TrigFun(outroot, attribid, ordering, geometry, parameters):
    func_name = 'TrigFun'

    simulation_func_name = str(parameters[0]) + '_blk'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, simulation_func_name, 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_TrigFun(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/TrigFun.py
# BEGIN Xcos/blocks/VARIABLE_DELAY.py


def VARIABLE_DELAY(outroot, attribid, ordering, geometry, parameters):
    func_name = 'VARIABLE_DELAY'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'variable_delay', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_VARIABLE_DELAY(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/VARIABLE_DELAY.py
# BEGIN Xcos/blocks/VVsourceAC.py


def VVsourceAC(outroot, attribid, ordering, geometry, parameters):
    func_name = 'VVsourceAC'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'VVsourceAC', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_VVsourceAC(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/VVsourceAC.py
# BEGIN Xcos/blocks/VanneReglante.py


def VanneReglante(outroot, attribid, ordering, geometry, parameters):
    func_name = 'VanneReglante'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'VanneReglante', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_VanneReglante(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/VanneReglante.py
# BEGIN Xcos/blocks/VariableResistor.py


def VariableResistor(outroot, attribid, ordering, geometry, parameters):
    func_name = 'VariableResistor'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'VariableResistor', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_VariableResistor(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/VariableResistor.py
# BEGIN Xcos/blocks/VirtualCLK0.py


def VirtualCLK0(outroot, attribid, ordering, geometry, parameters):
    func_name = 'VirtualCLK0'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'vrtclk0', 'DEFAULT',
                         func_name, BLOCKTYPE_D)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_VirtualCLK0(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/VirtualCLK0.py
# BEGIN Xcos/blocks/VoltageSensor.py


def VoltageSensor(outroot, attribid, ordering, geometry, parameters):
    func_name = 'VoltageSensor'

    outnode = addOutNode(outroot, BLOCK_VOLTAGESENSOR,
                         attribid, ordering, 1,
                         func_name, 'VoltageSensor', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)
    addTypeNode(outnode, TYPE_DOUBLE, AS_REAL_PARAM, 0,
                [])
    array = ['0']
    addTypeNode(outnode, TYPE_DOUBLE, AS_INT_PARAM, 0,
                [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_OBJ_PARAM, parameters)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NBZERO, 1, array)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NMODE, 1, array)
    addTypeNode(outnode, TYPE_DOUBLE, AS_STATE, 0, [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_DSTATE, 0, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_ODSTATE, parameters)
    equationsArrayNode = addObjNode(outnode, TYPE_ARRAY,
                                    CLASS_TLIST, AS_EQUATIONS, parameters)
    # Add ScilabString nodes to equationsArrayNode
    scilabStringParameters = ["modelica", "model",
                              "inputs", "outputs",
                              "parameters"]
    addScilabStringNode(equationsArrayNode, width=5,
                        parameters=scilabStringParameters)
    param = ['VoltageSensor']
    addSciStringNode(equationsArrayNode, 1, param)

    param1 = ["p"]
    addSciStringNode(equationsArrayNode, 1, param1)
    param = ["n", "v"]
    addSciStringNode(equationsArrayNode, 2, param)
    # Create the inner Array node for ScilabList
    innerArrayNode = addArrayNode(equationsArrayNode,
                                  scilabClass="ScilabList")
    addScilabDBNode(innerArrayNode, height=0)
    addArrayNode(innerArrayNode, scilabClass="ScilabList")

    addgeometryNode(outnode, GEOMETRY, geometry['height'],
                    geometry['width'], geometry['x'], geometry['y'])
    return outnode


def get_from_VoltageSensor(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/VoltageSensor.py
# BEGIN Xcos/blocks/VsourceAC.py


def VsourceAC(outroot, attribid, ordering, geometry, parameters):
    func_name = 'VsourceAC'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'VsourceAC', 'DEFAULT',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_VsourceAC(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0] + ',' + parameters[1]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/VsourceAC.py
# BEGIN Xcos/blocks/WRITEAU_f.py


def WRITEAU_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'WRITEAU_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'writeau', 'TYPE_2',
                         func_name, BLOCKTYPE_D,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 2, parameters)

    return outnode


def get_from_WRITEAU_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/WRITEAU_f.py
# BEGIN Xcos/blocks/WRITEC_f.py


def WRITEC_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'WRITEC_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'writec', 'TYPE_2',
                         func_name, BLOCKTYPE_D,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 5, parameters)

    return outnode


def get_from_WRITEC_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/WRITEC_f.py
# BEGIN Xcos/blocks/ZCROSS_f.py


def ZCROSS_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'ZCROSS_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'zcross', 'TYPE_1',
                         func_name, BLOCKTYPE_Z,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_ZCROSS_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/ZCROSS_f.py
# BEGIN Xcos/blocks/c_block.py


def c_block(outroot, attribid, ordering, geometry, parameters):
    func_name = 'c_block'

    code = parameters[4]
    codeLines = code.split('\n')

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, parameters[3], 'DYNAMIC_C_1',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsArrayNode(outnode, TYPE_STRING, 4, parameters, codeLines)

    return outnode


def get_from_c_block(cell):
    parameters = getParametersFromExprsNode(cell)

    display_parameter = parameters[3]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/c_block.py
# BEGIN Xcos/blocks/fortran_block.py


def fortran_block(outroot, attribid, ordering, geometry, parameters):
    func_name = 'fortran_block'

    code = parameters[4]
    codeLines = code.split('\n')

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, parameters[3], 'DYNAMIC_FORTRAN_1',
                         func_name, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsArrayNode(outnode, TYPE_STRING, 4, parameters, codeLines)

    return outnode


def get_from_fortran_block(cell):
    parameters = getParametersFromExprsNode(cell)

    display_parameter = parameters[3]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/fortran_block.py
# BEGIN Xcos/blocks/freq_div.py


def freq_div(outroot, attribid, ordering, geometry, parameters):
    func_name = 'freq_div'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'csuper', 'DEFAULT',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_freq_div(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/freq_div.py
# BEGIN Xcos/blocks/generic_block3.py


def generic_block3(outroot, attribid, ordering, geometry, parameters):
    func_name = 'generic_block3'

    if parameters[17] == 'y':
        depends_u = '1'
    else:
        depends_u = '0'

    if parameters[18] == 'y':
        depends_t = '1'
    else:
        depends_t = '0'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, parameters[0], 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C,
                         dependsOnU=depends_u,
                         dependsOnT=depends_t)

    addExprsNode(outnode, TYPE_STRING, 19, parameters)

    return outnode


def get_from_generic_block3(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[0]

    eiv = ''
    iiv = ''
    con = 1 if parameters[6] != '[]' and int(float(parameters[6])) == 1 else 0
    eov = ''
    iov = ''
    com = 1 if parameters[7] != '[]' and int(float(parameters[7])) == 1 else 0

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/generic_block3.py
# BEGIN Xcos/blocks/scifunc_block_m.py


def scifunc_block_m(outroot, attribid, ordering, geometry, parameters):
    func_name = 'scifunc_block_m'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'cscope', 'C_OR_FORTRAN',
                         func_name, BLOCKTYPE_C)

    addExprsNode(outnode, TYPE_STRING, 0, parameters)

    return outnode


def get_from_scifunc_block_m(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = parameters[10]

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)

# END Xcos/blocks/scifunc_block_m.py
# BEGIN Xcos/ports/CommandPort.py


def CommandPort(outroot, attribid, parentattribid, ordering, geometry,
                value='', forSplitBlock=False):
    func_name = 'CommandPort'

    if forSplitBlock:
        outnode = addNode(outroot, func_name, connectable=0,
                          dataType='UNKNOW_TYPE', **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=func_name, visible=0)
    else:
        outnode = addNode(outroot, func_name, initialState="-1.0",
                          dataType='UNKNOW_TYPE', **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=func_name, value=value)

    # addNode(outnode, 'mxGeometry', **{'as': 'geometry'},
    #         height=geometry['height'], width=geometry['width'],
    #         x=geometry['x'], y=geometry['y'])

    return outnode

# END Xcos/ports/CommandPort.py
# BEGIN Xcos/ports/ControlPort.py


def ControlPort(outroot, attribid, parentattribid, ordering, geometry,
                value='', forSplitBlock=False):
    func_name = 'ControlPort'

    if forSplitBlock:
        outnode = addNode(outroot, func_name, connectable=0,
                          dataType='UNKNOW_TYPE', **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=func_name, visible=0)
    else:
        outnode = addNode(outroot, func_name, initialState="-1.0",
                          dataType='UNKNOW_TYPE', **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=func_name, value=value)

    # addNode(outnode, 'mxGeometry', **{'as': 'geometry'},
    #         height=geometry['height'], width=geometry['width'],
    #         x=geometry['x'], y=geometry['y'])

    return outnode

# END Xcos/ports/ControlPort.py
# BEGIN Xcos/ports/ExplicitInputPort.py


def ExplicitInputPort(outroot, attribid, parentattribid, ordering, geometry,
                      addDataLines=False, value='', forSplitBlock=False):
    func_name = 'ExplicitInputPort'

    if forSplitBlock:
        outnode = addNode(outroot, func_name, connectable=0,
                          dataType='UNKNOW_TYPE', **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=func_name, visible=0)
    elif addDataLines:
        outnode = addNode(outroot, func_name, dataColumns=1, dataLines=1,
                          dataType='REAL_MATRIX', **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=func_name, value=value)
    else:
        outnode = addNode(outroot, func_name, dataColumns=1,
                          initialState="-1.0", dataType='REAL_MATRIX',
                          **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=func_name, value=value)

    # addNode(outnode, 'mxGeometry', **{'as': 'geometry'},
    #         height=geometry['height'], width=geometry['width'],
    #         x=geometry['x'], y=geometry['y'])

    return outnode


def addExplicitInputPortForSplit(outroot, splitBlock, sourceVertex, targetVertex,
                                 sourceType, targetType, edgeDict, inputCount,
                                 outputCount, nextAttrib, nextAttribForSplit):
    inputCount += 1
    geometry = {}
    geometry['width'] = 8
    geometry['height'] = 8
    geometry['x'] = -8
    geometry['y'] = -4
    ExplicitInputPort(outroot, nextAttrib, splitBlock, inputCount, geometry,
                      forSplitBlock=True)
    edgeDict[nextAttribForSplit] = ('ExplicitLink', sourceVertex, nextAttrib,
                                    sourceType, 'ExplicitInputPort')
    nextAttrib += 1
    nextAttribForSplit += 1
    return (inputCount, outputCount, nextAttrib, nextAttribForSplit)

# END Xcos/ports/ExplicitInputPort.py
# BEGIN Xcos/ports/ExplicitOutputPort.py


def ExplicitOutputPort(outroot, attribid, parentattribid, ordering, geometry,
                       addDataLines=False, value='', forSplitBlock=False):
    func_name = 'ExplicitOutputPort'

    if forSplitBlock:
        outnode = addNode(outroot, func_name, connectable=0,
                          dataType='UNKNOW_TYPE', **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=func_name, visible=0)
    elif addDataLines:
        outnode = addNode(outroot, func_name, dataColumns=1, dataLines=1,
                          dataType='REAL_MATRIX', **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=func_name, value=value)
    else:
        outnode = addNode(outroot, func_name, dataColumns=1,
                          initialState="-1.0", dataType='REAL_MATRIX',
                          **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=func_name, value=value)

    # addNode(outnode, 'mxGeometry', **{'as': 'geometry'},
    #         height=geometry['height'], width=geometry['width'],
    #         x=geometry['x'], y=geometry['y'])

    return outnode


def addExplicitOutputPortForSplit(outroot, splitBlock, sourceVertex, targetVertex,
                                  sourceType, targetType, edgeDict, inputCount,
                                  outputCount, nextAttrib, nextAttribForSplit):
    outputCount += 1
    geometry = {}
    geometry['width'] = 8
    geometry['height'] = 8
    geometry['x'] = 7
    geometry['y'] = -4
    ExplicitOutputPort(outroot, nextAttrib, splitBlock, outputCount, geometry,
                       forSplitBlock=True)
    edgeDict[nextAttribForSplit] = ('ExplicitLink', nextAttrib, targetVertex,
                                    'ExplicitOutputPort', targetType)
    nextAttrib += 1
    nextAttribForSplit += 1
    return (inputCount, outputCount, nextAttrib, nextAttribForSplit)

# END Xcos/ports/ExplicitOutputPort.py
# BEGIN Xcos/ports/ImplicitInputPort.py


def ImplicitInputPort(outroot, attribid, parentattribid, ordering, geometry,
                      addDataLines=False, value='', forSplitBlock=False):
    func_name = 'ImplicitInputPort'

    if forSplitBlock:
        outnode = addNode(outroot, func_name, connectable=0,
                          dataType='UNKNOW_TYPE', **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=func_name, visible=0)
    elif addDataLines:
        outnode = addNode(outroot, func_name, dataColumns=1, dataLines=1,
                          dataType='REAL_MATRIX', **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=func_name, value=value)
    else:
        outnode = addNode(outroot, func_name, dataColumns=1,
                          initialState="-1.0", dataType='REAL_MATRIX',
                          **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=func_name, value=value)

    # addNode(outnode, 'mxGeometry', **{'as': 'geometry'},
    #         height=geometry['height'], width=geometry['width'],
    #         x=geometry['x'], y=geometry['y'])

    return outnode

# END Xcos/ports/ImplicitInputPort.py
# BEGIN Xcos/ports/ImplicitOutputPort.py


def ImplicitOutputPort(outroot, attribid, parentattribid, ordering, geometry,
                       addDataLines=False, value='', forSplitBlock=False):
    func_name = 'ImplicitOutputPort'

    if forSplitBlock:
        outnode = addNode(outroot, func_name, connectable=0,
                          dataType='UNKNOW_TYPE', **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=func_name, visible=0)
    elif addDataLines:
        outnode = addNode(outroot, func_name, dataColumns=1, dataLines=1,
                          dataType='REAL_MATRIX', **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=func_name, value=value)
    else:
        outnode = addNode(outroot, func_name, dataColumns=1,
                          initialState="-1.0", dataType='REAL_MATRIX',
                          **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=func_name, value=value)

    # addNode(outnode, 'mxGeometry', **{'as': 'geometry'},
    #         height=geometry['height'], width=geometry['width'],
    #         x=geometry['x'], y=geometry['y'])

    return outnode

# END Xcos/ports/ImplicitOutputPort.py
# BEGIN Xcos/links/CommandControlLink.py


def CommandControlLink(outroot, attribid, sourceVertex, targetVertex):
    func_name = 'CommandControlLink'

    outnode = addNode(outroot, func_name, **{'id': attribid},
                      parent=1, source=sourceVertex, target=targetVertex,
                      style=func_name, value='')

    mxGeoNode = addNode(outnode, 'mxGeometry', **{'as': 'geometry'})
    addNode(mxGeoNode, 'mxPoint', **{'as': 'sourcePoint', 'x': "0.0", 'y': "0.0"})
    addNode(mxGeoNode, 'Array', **{'as': 'points'})
    addNode(mxGeoNode, 'mxPoint', **{'as': 'targetPoint', 'x': "0.0", 'y': "0.0"})

    return outnode

# END Xcos/links/CommandControlLink.py
# BEGIN Xcos/links/ExplicitLink.py


def ExplicitLink(outroot, attribid, sourceVertex, targetVertex):
    func_name = 'ExplicitLink'

    outnode = addNode(outroot, func_name, **{'id': attribid},
                      parent=1, source=sourceVertex, target=targetVertex,
                      style=func_name, value='')

    mxGeoNode = addNode(outnode, 'mxGeometry', **{'as': 'geometry'})
    addNode(mxGeoNode, 'mxPoint', **{'as': 'sourcePoint', 'x': "0.0", 'y': "0.0"})
    addNode(mxGeoNode, 'Array', **{'as': 'points'})
    addNode(mxGeoNode, 'mxPoint', **{'as': 'targetPoint', 'x': "0.0", 'y': "0.0"})

    return outnode

# END Xcos/links/ExplicitLink.py
# BEGIN Xcos/links/ImplicitLink.py


def ImplicitLink(outroot, attribid, sourceVertex, targetVertex):
    func_name = 'ImplicitLink'

    outnode = addNode(outroot, func_name, **{'id': attribid},
                      parent=1, source=sourceVertex, target=targetVertex,
                      style=func_name, value='')

    mxGeoNode = addNode(outnode, 'mxGeometry', **{'as': 'geometry'})
    addNode(mxGeoNode, 'mxPoint', **{'as': 'sourcePoint', 'x': "0.0", 'y': "0.0"})
    addNode(mxGeoNode, 'mxPoint', **{'as': 'targetPoint', 'x': "0.0", 'y': "0.0"})

    return outnode

# END Xcos/links/ImplicitLink.py
