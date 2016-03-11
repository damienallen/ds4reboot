from django.contrib.auth.models import User
from user.models import Housemate
from eetlijst.models import HOLog, Transfer
from django.shortcuts import render
from django.utils import timezone
import datetime as dt
from django.shortcuts import redirect
from django.http import HttpResponse
from decimal import Decimal


# generate eetlijst view for current or defined date

def index(request, year=timezone.now().year, month=timezone.now().month, day=timezone.now().day):

    # build date array
    focus_date = dt.date(int(year), int(month), int(day))
    prev_monday = focus_date - dt.timedelta(days=focus_date.weekday())

    day_names = ['Ma','Di','Wo','Do','Vr','Za','Zo']
    date_list = {}

    for n in range(7):
        n_date = prev_monday + dt.timedelta(days=n)

        if n_date == focus_date:
            date_list[n] = [day_names[n], n_date, True]
        else:
            date_list[n] = [day_names[n], n_date, False]

    # get next/prev week
    week_p = focus_date - dt.timedelta(days=7)
    week_n = focus_date + dt.timedelta(days=7)
    day_p = focus_date - dt.timedelta(days=1)
    day_n = focus_date + dt.timedelta(days=1)

    date_nav = {}
    date_nav['pw'] = '/eetlijst/' + str(week_p.year) + '/' + str(week_p.month).zfill(2) + '/' + str(week_p.day).zfill(2) + '/'
    date_nav['nw'] = '/eetlijst/' + str(week_n.year) + '/' + str(week_n.month).zfill(2) + '/' + str(week_n.day).zfill(2) + '/'
    date_nav['pd'] = '/eetlijst/' + str(day_p.year) + '/' + str(day_p.month).zfill(2) + '/' + str(day_p.day).zfill(2) + '/'
    date_nav['nd'] = '/eetlijst/' + str(day_n.year) + '/' + str(day_n.month).zfill(2) + '/' + str(day_n.day).zfill(2) + '/'

    # get list of active users sorted by move-in date
    active_users = User.objects.filter(is_active=True)
    user_list = Housemate.objects.filter(user__id__in=active_users).exclude(display_name = 'Huis').order_by('movein_date')

    # calculate total balance
    total_balance = 0
    for u in user_list:
        total_balance += u.balance

    total_balance += Housemate.objects.get(display_name='Huis').balance

    # build context object
    context = {
        'breadcrumbs': ['eetlijst'],
        'user_list': user_list,
        'date_list': date_list,
        'date_nav': date_nav,
        'total_balance': total_balance,
    }

    return render(request, 'eetlijst/index.html', context)


# handle goto date post requests
def goto_date(request):

    # validate input
    sel_date = request.POST.get('date')

    if sel_date == '':
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        try:
            dt.date(int(sel_date[0:4]),int(sel_date[5:7]),int(sel_date[8:10]))
        except ValueError:
            return HttpResponse("Invalid date.")

        return redirect('/eetlijst/' + sel_date[0:10] + '/')


# handle add ho requests
def add_ho(request):

    if request.method == 'POST':
        if request.user.is_authenticated():

            user_id = int(request.user.id)
            note = request.POST.get('note')

             # validate form input
            if request.POST.get('amount') == '':
                return HttpResponse("Must add amount.")
            else:
                amount = Decimal(round(Decimal(request.POST.get('amount')),2))

            if note == '':
                return HttpResponse("Must add description.")

            # update housemate object for current user
            h = Housemate.objects.get(user_id=user_id)
            h.balance += amount
            h.save()

            #update housemate objects for other users
            huis = Housemate.objects.get(display_name='Huis')

            active_users = User.objects.filter(is_active=True)
            other_housemates = Housemate.objects.filter(user__id__in=active_users).exclude(display_name='Huis')

            remainder = huis.balance
            split_cost = round((amount - remainder)/len(other_housemates),2)
            huis.balance = len(other_housemates)*split_cost - amount + remainder

            huis.save()

            for o in other_housemates:
                o.balance -= split_cost
                o.save()

            # add entry to ho table
            ho = HOLog(user=h.user, amount=amount, note=note)
            ho.save()

        else:
            return render(request, 'base/login_page.html')

    else:
        return HttpResponse("Method must be POST.")

    return redirect(request.META.get('HTTP_REFERER'))


# handle balance transfer post requests
def bal_transfer(request):

    if request.method == 'POST':
        if request.user.is_authenticated():

            current_user = int(request.user.id)
            other_user = request.POST.get('housemate')
            amount = request.POST.get('amount')

             # validate form input
            if int(request.POST.get('housemate')) == 0:
                return HttpResponse("Must choose housemate.")

            if request.POST.get('amount') == '':
                return HttpResponse("Must add amount.")
            elif Decimal(request.POST.get('amount')) < 0:
                return HttpResponse("Amount must be positive. Use arrow button instead.")
            else:
                amount = Decimal(round(Decimal(request.POST.get('amount')),2))

            # get user data from POST
            if request.POST.get('direction') == 'to':
                from_user = Housemate.objects.get(user_id=current_user)
                to_user = Housemate.objects.get(user_id=other_user)
            else:
                from_user = Housemate.objects.get(user_id=other_user)
                to_user = Housemate.objects.get(user_id=current_user)


            # update housemate objects
            from_user.balance -= amount
            from_user.save()

            to_user.balance += amount
            to_user.save()

            # add entry to transfer table
            t = Transfer(user=request.user, from_user=from_user.user.username, to_user=to_user.user.username, amount=amount)
            t.save()

        else:
            return render(request, 'base/login_page.html')

    else:
        return HttpResponse("Method must be POST.")

    return redirect(request.META.get('HTTP_REFERER'))