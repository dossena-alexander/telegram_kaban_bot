import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime

from server.utils.charts.collector import IStatClickCollector


class Chart():
    """Draw chart by Collector data"""
    def __init__(self, path: str, 
                       collector: IStatClickCollector, 
                       mode = 0, 
                       dpi = 350,
                       fig_name = 'chart.jpg') -> None:
        """Args:
            path (str): path to save figure
            collector (IStatClickCollector): _description_
            mode (int, optional): _description_. Defaults to 0.
            dpi (int, optional): Quality of figure. Defaults to 350.
            fig_name (str, optional): File name to save. Defaults to 'stat.jpg'.
        """
        self.path = path
        self.collector = collector
        self.mode = mode
        self.dpi = dpi
        self.fig_name = fig_name
        self.fmt = dates.DateFormatter('%H:%M:%S')

    def draw(self) -> None:
        fig, ax = plt.subplots()
        plt.title('График нажатий', fontsize=20, fontname='Helvetica')
        plt.xlabel('Время', color='gray')
        plt.ylabel('Кол-во',color='gray')
        time_interval, clicks = self.get_data(self.collector)
        ax.plot(time_interval, clicks, "-o")
        # ax.xaxis.set_major_formatter(self.fmt)
        fig.autofmt_xdate()
        plt.savefig(self.path+self.fig_name, dpi=self.dpi)

    def get_data(self, collector: IStatClickCollector) -> tuple[list[datetime], list[int]]:
        """Collecting data from Collector object. \n
        Collector needs to be setted up. \n

        Returns:
            tuple[list[datetime], int]: times_interval, clicks
        """
        interval, clicks = collector.get_data()
        return interval, clicks

    def set_data_type(self, data_type: str) -> None:
        """For getting data from DataBase table must be named as data_type.\n
        data_type could be:
            'wct_clicks',
            'photo_clicks',
            'joke_clicks'

        Args:
            data_type (str): Table name
        """
        self.data_type = data_type