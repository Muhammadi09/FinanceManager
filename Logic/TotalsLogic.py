def gatherDBDataWithDesc(DB, description):
    gatherTransaction = []

    for data in DB:
        if data.description.strip() == description.strip():
            gatherTransaction.append(data)

    return gatherTransaction


def breakdownCosts(expBreakDown, incomeBreakDown, DBdata):
    for data in DBdata:
        if data.type == 'Income':
            incomeBreakDown += data.amount
        else:
            expBreakDown += data.amount
    return (expBreakDown, incomeBreakDown)
