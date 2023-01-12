from django.shortcuts import render, redirect
from . models import Portfolio, Cash
from . import forms
import yfinance as yf
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/accounts/login/")
def index(request):
    # Declare variables
    user = request.user
    if user:
        all_stocks = Portfolio.objects.filter(buyer=user)
        cash = Cash.objects.filter(owner=user)[0]
        
        # Get Current Price and calculate profit
        if all_stocks:
            for stock in all_stocks:
                data = yf.download(tickers=str(stock.stock), period='1d', interval='1h')
                stock.cur_price = round(float(data['Open'].iloc[-1]), 2)
                stock.profit = round((int(stock.quantity) * float(stock.cur_price)) - (int(stock.quantity) * float(stock.buy_price)), 2)
                stock.save()
        
        # For Pie Chart
        labels =[]
        data = []

        for stock in all_stocks:
            labels.append(str(stock.stock))
            data.append(int(stock.quantity) * float(stock.cur_price))
        labels.append('Cash')
        data.append(float(cash.cash))

        # Total Portfolio Value:
        total_value = 0
        for i in range(len(data)):
            total_value += data[i]
        # Store Variables in dictionary
        context = {
            'all_stocks': all_stocks,
            'cash': cash.cash,
            'labels': labels,
            'data': data,
            'total_value': total_value,
            'user': user
        }
     # Render page
    return render(request, 'index.html', context=context)

@login_required(login_url="/accounts/login/")
def interact(request):
    user = request.user
    # Data from Buy/Sell Form handled Here
    if request.method == 'POST': 
        # Store form data in form variable
        form = forms.BuyStock(request.POST, request=request)

        # Buying requests handled here
        if form.is_valid() and 'buy_stock' in request.POST:
            # Get data from yfinance
            stock = str(form.cleaned_data['stock']).upper().strip()
            in_portfolio = Portfolio.objects.filter(stock = stock).filter(buyer = request.user)
            if in_portfolio:
                quantity = form.cleaned_data['quantity']
                data = yf.download(tickers=stock, period='1d', interval='1h')
                stock_buy_price = round(float(data['Open'].iloc[-1]), 2)
                total_price = round(stock_buy_price * quantity, 2)

                p_object = in_portfolio[0]
                p_object.buy_price = (float(p_object.buy_price) + stock_buy_price) / 2
                p_object.quantity = int(p_object.quantity) + quantity
                p_object.save()
            else:
                quantity = form.cleaned_data['quantity']
                data = yf.download(tickers=stock, period='1d', interval='1h')
                stock_buy_price = round(float(data['Open'].iloc[-1]), 2)
                total_price = stock_buy_price * quantity
                # Save data to database
                instance = form.save(commit=False) # Maybe turn this into a function later becuase its repeated code for buying and selling
                instance.stock = stock
                instance.buy_price = stock_buy_price
                instance.cur_price = stock_buy_price # delete this later
                instance.profit = 0
                instance.buyer = request.user
                instance.save()

            cash = Cash.objects.filter(owner=user)[0]
            cash.cash = float(cash.cash) - total_price
            cash.save()

            return redirect('index')

        # Selling requests handled here
        if form.is_valid() and 'sell_stock' in request.POST:
            instance = form.save(commit=False)
            stock = str(form.cleaned_data['stock']).upper().strip()
            quantity = int(form.cleaned_data['quantity'])
            portfolio_stock = Portfolio.objects.filter(stock = stock).filter(buyer = request.user)
            if portfolio_stock[0].quantity - quantity == 0:
                data = yf.download(tickers=stock, period='1d', interval='1h')
                stock_sell_price = round(float(data['Open'].iloc[-1]), 2)
                sell_value = quantity * stock_sell_price
                cash = Cash.objects.filter(owner=user)[0]
                cash.cash = float(cash.cash) + sell_value
                cash.save()
                portfolio_stock.delete()
            else:
                data = yf.download(tickers=stock, period='1d', interval='1h')
                stock_sell_price = round(float(data['Open'].iloc[-1]), 2)
                sell_value = quantity * stock_sell_price
                p_object = portfolio_stock[0]
                p_object.quantity = int(p_object.quantity) - quantity
                p_object.save()
                cash = Cash.objects.filter(owner=user)[0]
                cash.cash = float(cash.cash) + sell_value
                cash.save()
                

            return redirect('index')

    # Get Request Handled here
    else:
        if user:
            cash = Cash.objects.filter(owner=user)[0].cash
            # cash.cash = 999  # change field
            # cash.save()
            form = forms.BuyStock()
    if user:
        cash = cash = Cash.objects.filter(owner=user)[0].cash # Fix this logic up
    context = {
        'form': form,
        'cash': cash,
        'user': user
    }

    return render(request, 'interact.html', context=context)