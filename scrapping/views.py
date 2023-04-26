import base64
from django.shortcuts import render
from django.views import View
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from .models import Goods
from .tasks import parse_page
from io import BytesIO


class Hello(View):
    def get(self, request):
        result = parse_page()
        return render(request, "main.html")


class GoodsPriceView(View):

    def get(self, request, name: str):
        name = request.GET.get(name)
        goods = Goods.objects.filter(name=name).order_by('date')

        dates = [good.date for good in goods]
        prices = [good.price for good in goods]
        min_price = min(prices)
        current_price = prices[-1]

        # Convert dates to numerical format
        dates_num = mdates.date2num(dates)

        # Plot graph
        fig, ax = plt.subplots()
        ax.plot_date(dates_num, prices, fmt='-', xdate=True)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
        ax.yaxis.set_major_locator(plt.MultipleLocator(1))
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.set_title('Price vs Date')

        # Return the plot as a PNG image
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)
        image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        context = {'image': f'data:image/png;base64,{image}', 'current_price': current_price, 'min_price': min_price}
        return render(request, "goods_price.html",  context=context)
