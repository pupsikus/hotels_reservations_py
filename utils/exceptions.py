class ReservationException(Exception):
    pass


class UpdateException(ReservationException):
    pass


class CreateException(ReservationException):
    pass


class DeleteException(ReservationException):
    pass


class ReadException(ReservationException):
    pass


class VisitorException(Exception):
    pass


class ReservationValueError(ReservationException):
    pass


class ReservationTypeError(ReservationException):
    pass
