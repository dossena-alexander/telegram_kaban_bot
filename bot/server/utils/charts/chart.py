from PIL import Image
import PIL.ImageOps  
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime

from server.utils.charts.collector import IStatClickCollector, Time


class Chart():
    """Draw chart by Collector data"""
    date_format: str = '%Y-%M-%D'
    time_format: str = '%H:%M:%S'

    def __init__(self, path: str, 
                       collector: IStatClickCollector, 
                       mode: str = 'time', 
                       dpi: int = 350) -> None:
        """Args:
            path (str): path to save figure
            collector (IStatClickCollector): _description_
            mode (str, optional): X interval format 
            dpi (int, optional): Quality of figure. Defaults to 350.
            fig_name (str, optional): File name to save. Defaults to 'stat.jpg'.
        """
        self.path = path
        self.collector = collector
        self.mode = mode
        self.dpi = dpi
        self.fig_name = f'{collector.date} ({Time(now=True).time}).jpg'
        self.fmt = dates.DateFormatter('%H:%M')
        self.colors =  [ # inverted colors
            '#00ffff',   # red
            '#ffff00',   # blue
            '#11bffe',   # orange
            '#6bff2b',   # violet
            '#ff00ff'    # green
        ]

    def draw(self) -> None:
        formatter = self.time_format
        if self.mode == 'date':
            formatter = self.date_format

        fig, ax = plt.subplots()
        plt.title('График использования', fontsize=20, fontname='Helvetica')
        plt.xlabel('Время', color='gray')
        plt.ylabel('Кол-во',color='gray')

        data_dict = self.get_data(self.collector)
        for c, target in enumerate(self.collector.targets):
            time_interval = data_dict[target]['times']
            if time_interval:
                times = [datetime.strptime(time, formatter) for time in time_interval]
                clicks = data_dict[target]['clicks']
                ax.plot(times, clicks, "-o", color=self.colors[c], label=target)
        try:
            ax.legend()
        except:
            pass

        ax.xaxis.set_major_formatter(self.fmt)
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