import logging
import sys
import copy

cache_elements = {}
log = logging.getLogger(__name__)

def add_element(element_id, element, type = "DEFAULT"):
    '''
    Add the element with the element_id in the cache of type type
    If no type is specified, the default cache is used
    :param element_id:
    :param element:
    :param type:
    :return:
    '''
    if element_id:
        log.debug(msg="CACHE > adding element with ID ["+str(element_id)+"_"+type+"]")
        cache_elements[str(element_id)+"_"+type] = copy.copy(element)

def get_element(element_id, type="DEFAULT"):
    '''
    Return an element in the cache, identified by element_id
    If no type is defined, the default cache are used
    Throw a KeyError if no element is in the cache
    :param element_id:
    :param type:
    :return:
    '''
    if element_id:
        log.debug(msg="get_element with ID [" + str(element_id) + "_" + type + "]")
        return copy.copy(cache_elements[str(element_id)+"_"+type])
    else:
        log.debug(msg="get_element with None ID --> raising KeyError")
        raise KeyError


def del_element(element_id, type = "DEFAULT"):
    try:
        if element_id:
            log.debug(msg="CACHE > deleting element with ID [" + str(element_id) + "_" + type + "]")
            del(cache_elements[str(element_id)+"_"+type])
    except KeyError:
        pass

def reset(type="DEFAULT"):
    '''
    Delete all element in cache of the type specified
    :param type:
    :return:
    '''
    log.debug("CACHE > resetting element of type [" + type + "]")
    for k,v in cache_elements.items():
        if k.endswith(type):
            del(cache_elements[k])

def print_status():
    print(sys.getsizeof(cache_elements), "Bytes")
    for k,v in cache_elements.items():
        if type(v)==list:
            print(k, len(v))