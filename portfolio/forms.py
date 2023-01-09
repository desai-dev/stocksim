from django import forms
from . import models 
import yfinance as yf

class BuyStock(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BuyStock, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("stock"):
            stock = cleaned_data.get("stock").upper().strip()
        else:
            stock = cleaned_data.get("stock")
        quantity = cleaned_data.get("quantity")

        if stock and quantity:
            buy_req = self.data.get('buy_stock')
            if buy_req:
                data = yf.download(tickers=stock, period='1d', interval='1h')
                price = round(float(data['Open'].iloc[-1]), 2)
                cash = float(models.Cash.objects.filter(owner=self.request.user)[0].cash)
                total_price = quantity * price

                if total_price > cash:
                    raise forms.ValidationError("Not enough cash")
                else:
                    return cleaned_data
            else:
                in_portfolio = models.Portfolio.objects.filter(stock = stock).filter(buyer=self.request.user)
                if in_portfolio:
                    portfolio_quantity = in_portfolio[0].quantity
                    if quantity <= portfolio_quantity:
                        return cleaned_data
                    else:
                        raise forms.ValidationError("You don't own enough of this stock")
                else: 
                    raise forms.ValidationError("You don't own this stock")

    def clean_stock(self):
        try:
            stock = self.cleaned_data.get('stock').upper().strip()
            data = yf.download(tickers=stock, period='1d', interval='1h')
            price = round(float(data['Open'].iloc[-1]), 2)
            return stock
        except IndexError:
            raise forms.ValidationError("Not a valid stock ticker")
        except TypeError:
            raise forms.ValidationError("Not a valid stock ticker")


    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity > 0:
            return quantity
        else:
            raise forms.ValidationError("Quantity must be greater than 0")

    class Meta:
        model = models.Portfolio
        fields = ['stock', 'quantity']