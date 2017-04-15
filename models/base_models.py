from sqlalchemy import Column, Integer, String, Date

from settings.set_db import Base, engine


class RoomReservation(Base):
    __tablename__ = 'room_reservations'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    room_number = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)

    def __repr__(self):
        return "<Reservation(first_name='%s', last_name='%s', " \
               "room_number='%s', start_date='%s', end_date='%s')>" % (
            self.first_name, self.last_name, self.room_number,
            self.start_date, self.end_date)

Base.metadata.create_all(engine)
