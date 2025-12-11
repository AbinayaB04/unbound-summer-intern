def deduct_credit(user, db):
    if user.credits <= 0:
        return False
    user.credits -= 1
    db.commit()
    return True
