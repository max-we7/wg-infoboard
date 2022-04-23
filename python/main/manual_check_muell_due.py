from zaw_query import check_muell_due
import logging
logging.basicConfig(filename="../wg-infoboard.log", filemode="a+", format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

check_muell_due()
