# -*- coding: utf-8 -*-
class Chibi_hybrid:
    def __init__( self, fclass, finstance=None, doc=None ):
        self.fclass = fclass
        self.finstance = finstance
        self.__doc__ = doc or fclass.__doc__
        self.__isabstractmethod__ = bool(
            getattr( fclass, '__isabstractmethod__', False ) )

    def classmethod( self, fclass ):
        return type( self )( fclass, self.finstance, None )

    def instancemethod( self, finstance ):
        return type( self )( self.fclass, finstance, self.__doc__ )

    def __get__( self, instance, cls ):
        if instance is None or self.finstance is None:
              # either bound to the class, or no instance method available
            return self.fclass.__get__( cls, None )
        return self.finstance.__get__( instance, cls )


class Descriptor_class_property:
    def __init__( self, fget, fset=None ):
        self.fget = fget
        self.fset = fset
        self.f_get_instance = None

    def __get__( self, obj, cls=None ):
        if cls is None:
            cls = type( obj )
        if obj is not None and self.f_get_instance is not None:
            return self.f_get_instance.__get__( obj, cls )
        return self.fget.__get__( obj, cls )()

    def __set__( self, obj, value ):
        if not self.fset:
            raise AttributeError( "can not set the attribute" )
        return self.fset.__get__( obj, type( obj ) )( value )

    def setter( self, func ):
        if not isinstance( func, ( classmethod, staticmethod ) ):
            func = classmethod( func )
        self.fset = func
        return self

    def instance( self, func ):
        if not isinstance( func, ( property ) ):
            func = property( func )
        self.f_get_instance = func
        return self


def Class_property( func ):
    if not isinstance( func, ( classmethod, staticmethod )):
        func = classmethod( func )

    return Descriptor_class_property( func )
