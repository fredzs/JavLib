

class Statistic(object):
    download_success_count = int(0)
    download_failed_count = int(0)
    db_item_success_count = int(0)
    db_item_failed_count = int(0)
    db_key_success_count = int(0)
    db_key_failed_count = int(0)

    @staticmethod
    def download_success():
        Statistic.download_success_count += 1

    @staticmethod
    def download_failed():
        Statistic.download_failed_count += 1

    @staticmethod
    def db_item_success():
        Statistic.db_item_success_count += 1

    @staticmethod
    def db_item_failed():
        Statistic.db_item_failed_count += 1

    @staticmethod
    def db_key_success():
        Statistic().db_key_success_count += 1

    @staticmethod
    def db_key_failed():
        Statistic.db_key_failed_count += 1

    @staticmethod
    def get_download_success():
        return Statistic.download_success_count

    @staticmethod
    def get_download_failed():
        return Statistic.download_failed_count

    @staticmethod
    def get_item_success():
        return Statistic.db_item_success_count

    @staticmethod
    def get_item_failed():
        return Statistic.db_item_failed_count

    @staticmethod
    def get_key_success():
        return Statistic.db_key_success_count

    @staticmethod
    def get_key_failed():
        return Statistic.db_key_failed_count
