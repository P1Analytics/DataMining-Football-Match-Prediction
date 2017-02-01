import logging
import sys
import copy

cache_elements = {}

def add_element(element_id, element, type = "DEFAULT"):
    '''
    Add the element with the element_id in the cache of type type
    If no type is specified, the default cache is used
    :param element_id:
    :param element:
    :param type:
    :return:
    '''
    logging.debug("CACHE > adding element with ID ["+str(element_id)+"_"+type+"]")
    cache_elements[str(element_id)+"_"+type] = copy.deepcopy(element)

def get_element(element_id, type="DEFAULT"):
    '''
    Return an element in the cache, identified by element_id
    If no type is defined, the default cache are used
    Throw a KeyError if no element is in the cache
    :param element_id:
    :param type:
    :return:
    '''
    logging.debug("CACHE > reading element with ID [" + str(element_id) + "_" + type + "]")
    return copy.deepcopy(cache_elements[str(element_id)+"_"+type])

def reset(type="DEFAULT"):
    '''
    Delete all element in cache of the type specified
    :param type:
    :return:
    '''
    logging.debug("CACHE > resetting element of type [" + type + "]")
    for k,v in cache_elements.items():
        if k.endswith(type):
            del(cache_elements[k])

def print_status():
    print(sys.getsizeof(cache_elements), "Bytes")
    for k,v in cache_elements.items():
        if type(v)==list:
            print(k, len(v))