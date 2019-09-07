import datetime
from app.models import Line, Status


def get_or_create(db_session, model, **kwargs):
    created = False
    instance = db_session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, created
    else:
        instance = model(**kwargs)
        db_session.add(instance)
        db_session.commit()
        created = True
        return instance, created


def update_line_and_status(line_name, status_name, db):
    line, created = get_or_create(db.session, Line, name=line_name)

    previous_status = Status.query.filter_by(
        line_id=line.id).order_by(Status.create_time.desc()).first()

    status = Status(name=status_name, line_id=line.id)
    db.session.add(status)
    db.session.commit()

    log_status_change(line, status, previous_status)
    cache_status_change(line, status, db)

    line_name = line.name
    status_name = status.name
    print(f"{line_name} {status_name}")

    return line, status


def log_status_change(line, status, previous_status):
    if previous_status is not None:
        line_name = line.name

        log = None

        if (previous_status.name == 'not delayed' and status.name == 'delayed'):
            log = f"Line {line_name} is experiecing delays"
        elif (previous_status.name == 'delayed' and status.name == 'not delayed'):
            log = f"Line {line_name} is now recovered"

        if log is not None:
            print(log)


def cache_status_change(line, status, db):
    status = Status.query.filter_by(line_id=line.id).order_by(
        Status.create_time.desc()).first()

    if status is not None:
        status_name = status.name
        if status_name == 'not delayed':
            previous_delayed_status = Status.query.filter_by(
                line_id=line.id, name='delayed').order_by(Status.create_time.desc()).first()

            previous_status = Status.query.filter(
                Status.create_time < status.create_time, Status.line_id == status.line_id).order_by(Status.create_time.desc()).first()

            should_cache = (
                previous_delayed_status is not None and
                previous_status is not None and
                previous_delayed_status.id == previous_status.id
            )

            if should_cache is True:
                previous_delayed_status_time = previous_delayed_status.create_time
                status_time = status.create_time
                diff = status_time - previous_delayed_status_time
                diff_seconds = diff.total_seconds()
                cached_downtime = line.down_time
                line.down_time = cached_downtime + diff_seconds
                db.session.add(line)
                db.session.commit()
