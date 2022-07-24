from django.shortcuts import render

# Create your views here.
def homepage(request):
  # form = OrderForm()
  # #if there is an incoming submitted form
  # if request.method == "POST":
  #   form = OrderForm(request.POST)
  #   if form.is_valid():
  #     processOrder(form, request)
  #     return redirect('app:homepage')

  # wallet = Wallet.objects.filter(user=request.user).first()
  # context = {
  #   "user": request.user,
  #   "open_orders": Order.objects.filter(profile=request.user, status="pending").order_by('datetime'),
  #   "closed_orders": Order.objects.filter(profile=request.user, status="executed").order_by('-datetime'),
  #   "btc_balance":  wallet.btc_balance,
  #   "usd_balance": wallet.usd_balance,
  #   "profit": wallet.profit,
  #   "form": form
  # }
  # return render(request=request, template_name='app/home.html', context=context)
  return 