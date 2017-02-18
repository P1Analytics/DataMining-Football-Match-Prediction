import gc
import logging
import sys
import copy
import heapq

from threading import Thread
from time import sleep

import src.util.util as util

cache_elements = {}
cache_time_elements = []
max_cache_size = 1024*1024*512      # 512 MB
log = logging.getLogger(__name__)
block_caching_operation = False

def get_cache_size():
    global block_caching_operation

    block_caching_operation = True
    cache_size = 0
    for k, v in cache_elements.items():
        cache_size += sys.getsizeof(k) + sys.getsizeof(v)  # byte
    block_caching_operation = False

    if cache_size > 1024*1024:
        cache_size_str = str(cache_size // (1024*1024))
        measure = "MB"
    elif cache_size > 1024:
        cache_size_str = str(cache_size // (1024))
        measure = "KB"
    else:
        cache_size_str = str(cache_size)
        measure = "Byte"


    return cache_size, cache_size_str, measure

def threaded_function(arg):
    while True:
        cache_size, cache_size_str, measure = get_cache_size()
        log.debug("Size of the cache ["+cache_size_str+" "+measure+"]")

        if cache_size > max_cache_size:
            log.debug("Cache too big --> removing old elements")
            n_elemenent_removed = 0
            while cache_size > max_cache_size // 2 and len(cache_time_elements)>0:
                time, remove_id = heapq.heappop(cache_time_elements)
                del (cache_elements[remove_id])
                n_elemenent_removed += 1

                gc.collect()
                cache_size, cache_size_str, measure = get_cache_size()

            log.debug("Removed ["+n_elemenent_removed+"] elements")
            log.debug("New size of the cache [" + cache_size_str + " " + measure + "]")

        sleep(60)

def init_cache():
    thread = Thread(target=threaded_function, args=(10,))
    thread.start()


def add_element(element_id, element, type = "DEFAULT"):
    '''
    Add the element with the element_id in the cache of type type
    If no type is specified, the default cache is used
    :param element_id:
    :param element:
    :param type:
    :return:
    '''
    global block_caching_operation

    while block_caching_operation:
        pass
    if element_id:
        id = str(element_id)+"_"+type
        log.debug(msg="CACHE > adding element with ID ["+id+"]")
        cache_elements[id] = copy.copy(element)
        heapq.heappush(cache_time_elements, (util.get_curr_time_millis(), id))

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