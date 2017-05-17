import attr
from attr.validators import in_
from functools import partial
from weakref import WeakKeyDictionary
from re import sub

attrs = partial(attr.s, slots=True, frozen=True)
@attrs
class Event:
    """this is a superclass for any events that might be generated by an
    object and sent to the EventManager
    """
    @property
    def name(self):
        return sub(r"(.)(?=[A-Z])", r"\1 ", self.__class__.__name__) + " Event"

@attrs
class TickEvent(Event): pass

@attrs
class QuitEvent(Event): pass

@attrs
class NextTurn(Event): pass

@attrs
class GetPiece(Event):
    num = attr.ib(validator=in_(range(1,6)))

@attrs
class RotPiece(Event):
    rottype = attr.ib(validator=in_({'rotCW', 'rotCCW', 'flip'}))

@attrs
class NextPiece(Event):
    direction = attr.ib(validator=in_({'f', 'b'}))

@attrs
class MovePiece(Event):
    direction = attr.ib(validator=in_({'up', 'down', 'left', 'right'}))

@attrs
class PlacePiece(Event): pass

@attrs
class ResignEvent(Event): pass


class EventManager:
    """this object is responsible for coordinating most communication
    between the Model, View, and Controller.
    """
    def __init__(self ):
        self.listeners = WeakKeyDictionary()

    #----------------------------------------------------------------------
    def RegisterListener( self, listener ):
        self.listeners[ listener ] = 1

    #----------------------------------------------------------------------
    def UnregisterListener( self, listener ):
        if listener in self.listeners.keys():
            del self.listeners[ listener ]

    #----------------------------------------------------------------------
    def Post( self, event ):
        """Post a new event.  It will be broadcast to all listeners"""
        for listener in self.listeners.keys():
            #NOTE: If the weakref has died, it will be
            #automatically removed, so we don't have
            #to worry about it.
            listener.Notify( event )
