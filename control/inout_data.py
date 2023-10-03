"""
description:
    データ保存、読み込み関連です。
"""
from __future__ import annotations
from datetime import timedelta
import os
import csv
import setting


class InOutData:
    """
    description:
        データを保存するためのクラスです。
        データを読み込みするためのクラスです。
    """

    save_file_name = os.path.join(
        setting.DATA_SAVE_DIR,
        setting.COURSE_NAME + setting.SAVE_EXTENTION
        )

    def __init__(self, id_: int, sum_time: timedelta):
        self.id_ = id_
        self.sum_time = sum_time

    def __lt__(self, other: InOutData):
        selftime = timedelta(
            seconds=self.sum_time.seconds,
            microseconds=int(self.sum_time.microseconds/1000)*1000)
        othertime = timedelta(
            seconds=other.sum_time.seconds,
            microseconds=int(other.sum_time.microseconds/1000)*1000)
        if selftime != othertime:
            return selftime < othertime
        return self.id_ < other.id_

    @staticmethod
    def to_inoutdata(
            id_: int,
            minutes: int,
            seconds: int,
            microseconds: int
            ) -> InOutData:
        """
        description:
            データをInOutDataに変換します。
        """
        return InOutData(id_, timedelta(
                minutes=minutes,
                seconds=seconds,
                microseconds=microseconds*1000
                ))

    def time_to_data(self) -> tuple[int, int, int]:
        """
        description:
            timedeltaをデータに変換します。
        return: (minutes, seconds, microseconds)
        """
        # 表示したい形式に変換（小数点第3位までに変換）
        minutes, seconds = divmod(self.sum_time.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if 0 < hours:
            raise OverflowError("時間がオーバーしました")
        if self.sum_time.microseconds != 0:
            microseconds = int(self.sum_time.microseconds/1000)
        return (minutes, seconds, microseconds)

    @staticmethod
    def in_data() -> list[InOutData]:
        """
        description:
            データを読み込みます。
        """
        in_data_list = []
        if not os.path.exists(InOutData.save_file_name):
            return in_data_list
        with open(
                InOutData.save_file_name,
                "r",
                encoding="utf-8",
                newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == "id":
                    continue
                in_data_list.append(
                    InOutData.to_inoutdata(
                        int(row[0]),
                        int(row[1]),
                        int(row[2]),
                        int(row[3])
                    )
                )
        return in_data_list

    @staticmethod
    def out_data(out_data_list: list[InOutData]):
        """
        description:
            データを保存します。
        """

        if not os.path.exists(setting.DATA_SAVE_DIR):
            os.mkdir(setting.DATA_SAVE_DIR)

        if not os.path.exists(InOutData.save_file_name):
            with open(
                    InOutData.save_file_name,
                    "w",
                    encoding="utf-8",
                    newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["id", "minutes", "seconds", "microseconds"])

        with open(
                InOutData.save_file_name,
                "a",
                encoding="utf-8",
                newline="") as file:
            writer = csv.writer(file)
            for out_data in out_data_list:
                (minutes, seconds, microseconds) = out_data.time_to_data()
                writer.writerow([out_data.id_, minutes, seconds, microseconds])

    @staticmethod
    def find_not_use_ids(
            in_data_list: list[InOutData],
            count: int
            ) -> list[int]:
        """
        description:
            未使用のidをcount個探します。
        """
        use_id_list = []
        for in_data in in_data_list:
            use_id_list.append(in_data.id_)
        not_use_id_list = []
        counter = 1
        while len(not_use_id_list) < count:
            if counter not in use_id_list:
                not_use_id_list.append(counter)
            counter += 1
        return not_use_id_list

    @staticmethod
    def save_file(sum_data_list: list[timedelta]) -> list[InOutData]:
        """
        description:
            データを保存します。
        """
        in_data_list = InOutData.in_data()
        ids = InOutData.find_not_use_ids(in_data_list, len(sum_data_list))
        out_data_list = [InOutData(id_, sum_data)
                         for id_, sum_data in zip(ids, sum_data_list)]
        InOutData.out_data(out_data_list)
        inout_data_list = in_data_list.copy()
        inout_data_list.extend(out_data_list.copy())
        inout_data_list.sort()
        return inout_data_list
