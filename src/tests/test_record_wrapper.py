from util import GameRecord, GameRecordWrapper


def test_record_1():
    record = GameRecord(guild=1, channel=1)
    wrapper = GameRecordWrapper(record=record)

    record.guild = 2
    assert wrapper.updated is True


def test_record_2():
    record = GameRecord(guild=1, channel=1)
    wrapper = GameRecordWrapper(record=record)

    wrapper.record = GameRecord(guild=2, channel=2)
    assert wrapper.updated is True
