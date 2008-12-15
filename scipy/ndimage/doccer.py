''' Utilities to allow inserting docstring fragments for common
parameters into function and method docstrings'''

import sys

def docformat(docstring, docdict=None):
    ''' Fill a function docstring from variables in dictionary

    Adapt the indent of the inserted docs

    Parameters
    ----------
    docstring : string
        docstring from function, possibly with dict formatting strings
    docdict : dict
        dictionary with keys that match the dict formatting strings
        and values that are docstring fragments to be inserted.  The
        indentation of the inserted docstrings is set to match the
        indentation of the ``docstring``.  The string values in the
        docdict are assumed to have no indent in the first line, and
        only indent relative to the first line for following lines.

    Returns
    -------
    outstring : string
        string with any formatted strings inserted
    '''
    if not docstring:
        return docstring
    if docdict is None:
        docdict = {}
    if not docdict:
        return docstring
    lines = docstring.expandtabs().splitlines()
    # Find the minimum indent of the main docstring, after first line
    if len(lines) < 2:
        icount = 0
    else:
        icount = indentcount_lines(lines[1:])
    indent = ' ' * icount
    # Insert this indent to dictionary docstrings
    indented = {}
    for name, dstr in docdict.items():
        lines = dstr.expandtabs().splitlines()
        newlines = [lines[0]]
        for line in lines[1:]:
            newlines.append(indent+line)
        indented[name] = '\n'.join(newlines)
    return docstring % indented


def indentcount_lines(lines):
    ''' Minumum indent for all lines in line list '''
    indentno = sys.maxint
    for line in lines:
        stripped = line.lstrip()
        if stripped:
            indentno = min(indentno, len(line) - len(stripped))
    if indentno == sys.maxint:
        return 0
    return indentno


def filldoc(docdict, unindent_params=True):
    ''' Return docstring decorator using docdict variable dictionary

    Parameters
    ----------
    docdict : dictionary
        dictionary containing name, docstring fragment pairs
    unindent_params : {False, True}, boolean, optional
        If True, strip common indentation from all parameters in
        docdict
    
    Returns
    -------
    decfunc : function
        decorator that applies dictionary to input function docstring
    '''
    if unindent_params:
        docdict = unindent_dict(docdict)
    def decorate(f):
        f.__doc__ = docformat(f.__doc__, docdict)
        return f
    return decorate


def unindent_dict(docdict):
    ''' Unindent all strings in a docdict '''
    can_dict = {}
    for name, dstr in docdict.items():
        can_dict[name] = unindent_string(dstr)
    return can_dict


def unindent_string(docstring):
    ''' Set docstring to minimum indent for all lines, including first '''
    lines = docstring.expandtabs().splitlines()
    icount = indentcount_lines(lines)
    if icount == 0:
        return docstring
    return '\n'.join([line[icount:] for line in lines])