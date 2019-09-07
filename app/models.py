from datetime import datetime

from application import db


class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    statuses = db.relationship("Status", back_populates="line")
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)
    down_time = db.Column(db.Float, default=0)


    def uptime(self):
        now = datetime.now()
        total_time = now - self.create_time
        total_time_seconds = total_time.total_seconds()
        return 1 - (self.down_time / total_time_seconds)


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum('not delayed', 'delayed'),
                     nullable=False, default='not delayed')
    line_id = db.Column(db.Integer, db.ForeignKey('line.id'))
    line = db.relationship("Line", back_populates="statuses")
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    # TODO refactor ENUM column so name is valide enum type before save
