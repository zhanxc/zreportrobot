'''
 * @Author: zhanxc 
 * @Date: 2020-12-31 17:51:18 
 * @Last Modified by:   zhanxc 
 * @Last Modified time: 2020-12-31 17:51:18 
'''

import logging
import os
import time
def get_logger(log_path,log_file):
    """
    docstring
    """
    logger = logging.getLogger('Reporter')

    fh = logging.FileHandler(os.path.join(log_path,log_file),mode='a',encoding='utf8')
    sh = logging.StreamHandler()
    ft = logging.Formatter('%(asctime)s %(levelname)s  %(message)s')
    fh.setFormatter(ft)
    sh.setFormatter(ft)

    logger.addHandler(fh)
    logger.addHandler(sh)
    logger.setLevel('INFO')
    
    return logger


