from PIL import Image
import PIL.ImageOps  
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime

from server.utils.charts.collector import IStatClickCollector, Time


class Chart():
    """Draw chart by Collector data"""
    def __init__(self, path: str, 
                       collector: IStatClickCollector, 
                       mode = 0, 
                       dpi = 350) -> None:
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
        self.fig_name = f'{collector.date} ({Time(now=True).time}).jpg'
        self.fmt = dates.DateFormatter('%H:%M')
        self.colors =  [ 
            '#00ffff', # red
            '#ffff00', # blue
            '#11bffe', # orange
            '#6bff2b', # violet
            '#ff00ff' # green
        ]

    def draw(self) -> None:
        fig, ax = plt.subplots()
        plt.title('График использования', fontsize=20, fontname='Helvetica')
        plt.xlabel('Время', color='gray')
        plt.ylabel('Кол-во',color='gray')
        data_dict = self.get_data(self.collector)
        for c, target in enumerate(self.collector.targets):
            time_interval = data_dict[target]['times']
            clicks = data_dict[target]['clicks']
            if time_interval[0] == '0':
                pass
            else:
                ax.plot(time_interval, clicks, "-o", color=self.colors[c], label=target)
        # ax.xaxis.set_major_formatter(self.fmt)
        try:
            ax.legend()
        except:
            pass
        fig.autofmt_xdate()
        plt.savefig(self.path+self.fig_name, dpi=self.dpi)
        image = Image.open(self.path+self.fig_name)
        inverted_image = PIL.ImageOps.invert(image)
        inverted_image.save(self.path+self.fig_name)

    def get_data(self, collector: IStatClickCollector) -> tuple[list[str], list[int]]:
        """Collecting data from Collector object. \n
        Collector needs to be setted up. \n

        Returns:
            tuple[list[datetime], int]: times_interval, clicks
        """
        return collector.get_data()

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