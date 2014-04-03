
class ChildNotFoundError(Exception):
    """ Raised on attempts to look up a non-existent path 
    """
    def __init__(self, node, child):
        self.strerror = "Node %s has no child %s" % (node, child)

class ChildAlreadyExistsError(Exception):
    """ Raised on attempts to insert the same child more than one time
    """
    def __init__(self, node, child):
        self.strerror = "Node %s already has child %s" % (node, child)

class Node(object):
    """ The base class for configuration and reference tree nodes.

        This class is not supposed to be used directly.
    """

    def __init__(self, name, **kwargs):
        self.__name = name
        self.__children = []

    def get_name(self):
        """ Returns node name.
        """
        return(self.__name)

    def find_child(self, name):
        """ Finds an immediate child by name.

            Args:                 
                name (str): Child name

            Returns:
                Node 

            Raises:
                ChildNotFoundError
        """
        result = None
        for child in self.__children:
            if child.get_name() == name:
                result = child
        if result:
            return(result)
        else:
            raise ChildNotFoundError(self.get_name(), name)

    def list_children(self):
        """ Lists immediate children
        
            Returns:
                List of node names
        """
        names = [ x.get_name() for x in self.__children ]
        return(names)

    def get_child(self, path):
        """ Finds a child node by path

            Args:
                path (list): Child node path, bottom-up ordered
                (e.g. ['departments', 'branches', 'organization'])

            Returns:
                Node: Child node

            Raises:
                ChildNotFoundError
        """
        next_level = path.pop()
        if not path:
            # It was the last path level
            # So it's either an immediate child or there's no such node
            child = self.find_child(next_level)
            return(child)
        else:
            # It's not, we need to recurse
            child = self.find_child(next_level)
            return( child.get_child(path) )

    def insert_child(self, path, **kwargs):
        """ Inserts a new child

            Args:
                path (list): The path to child node

            Returns:
                child (node): the inserted node

            Raises:
                ChildNotFoundError, ChildAlreadyExistsError
        """
        next_level = path.pop()
        if not path:
            # That was the last item of the path, 
            # so the node is going to be an immediate child

            # Check if we are not trying to add the same name twice
            children = self.list_children()
            if next_level in children:
                raise ChildAlreadyExistsError(self.get_name(), next_level)

            child = Node(next_level, **kwargs)
            self.__children.append(child)
            return(child)
        else:
            # It is not, so we need to recurse,
            # but first decide if we have where to recurse.
            next_child = self.find_child(next_level)
            if not next_child:
                # We have no such child
                raise ChildNotFoundError(self.get_name(), next_level)
            else:
                # We do, recurse there
                return next_child.insert_child(path)

    def delete(self, path):
        """ A stub for delete method.

            Config tree and reference tree need different delete semantics,
            so we leave it empty.
        """
        pass