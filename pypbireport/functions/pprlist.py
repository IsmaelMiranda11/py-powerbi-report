'''Module for PPRList class.

PPRList class is intended to modified behavior of `list` type to accept
slicing and indexing by string.
'''

class PPRList(list):
    '''Class to hold visual objects. 

    Simple modification of list class to work with visual id indexing 
    by string.

    '''
    def __getitem__(self, index):
        '''Modification of __getitem__ magic method to get item by string'''
        if isinstance(index, str): #string
            for i, item in enumerate(self.__iter__()):
                if item.id == index:                
                    return list.__getitem__(self,i)
        elif isinstance(index, list): #list of strings
            list_items = []
            for idx in index:
                list_items.append(self.__getitem__(idx))
            return list_items
        else:
            return list.__getitem__(self,index)