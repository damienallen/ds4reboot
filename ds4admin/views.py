from django.contrib.auth.models import User, Group
from user.models import Housemate
from eetlijst.models import HOLog
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from decimal import Decimal
import datetime as dt


# view for ds4 admin page
def balance(request):

    if request.user.is_superuser:

        # get list of active users sorted by move-in date
        active_users = User.objects.filter(is_active=True)
        inactive_users = User.objects.filter(is_active=False)
        housemates = Housemate.objects.filter(user__id__in=active_users).exclude(display_name='Huis')\
            .order_by('movein_date')
        inactive_housemates = Housemate.objects.filter(user__id__in=inactive_users)\
            .filter(moveout_set=False).order_by('movein_date').exclude(display_name='Admin')

        huis_balance = Housemate.objects.get(display_name='Huis').balance
        active_balance = 0
        for h in housemates:
            active_balance += h.balance

        inactive_balance = 0
        for h in inactive_housemates:
            inactive_balance += h.balance

        overall_balance = active_balance + inactive_balance + huis_balance

        year = str(timezone.now().year).zfill(2)
        month = str(timezone.now().month).zfill(2)
        day = str(timezone.now().day).zfill(2)

        # build context object
        context = {
            'breadcrumbs': ['admin'],
            'housemates': housemates,
            'inactive': inactive_housemates,
            'active_balance': active_balance,
            'inactive_balance': inactive_balance,
            'remainder': huis_balance,
            'overall_balance': overall_balance,
            'focus_date': str(year) + '/' + str(month) + '/' + str(day),
            }

        return render(request, 'ds4admin/balance.html', context)

    else:
        messages.error(request, 'Admin only area.')
        return redirect('/')


# view for huisgenooten tab
def housemates(request):

    if request.user.is_superuser:

        # get list of active users sorted by move-in date
        active_users = User.objects.filter(is_active=True)
        inactive_users = User.objects.filter(is_active=False)
        housemates = Housemate.objects.filter(user__id__in=active_users).exclude(display_name='Huis')\
            .order_by('movein_date')
        inactive_housemates = Housemate.objects.filter(user__id__in=inactive_users) \
            .filter(moveout_set=None).order_by('movein_date').exclude(display_name='Admin')

        year = str(timezone.now().year).zfill(2)
        month = str(timezone.now().month).zfill(2)
        day = str(timezone.now().day).zfill(2)

        # build context object
        context = {
            'breadcrumbs': ['admin'],
            'housemates': housemates,
            'inactive': inactive_housemates,
            'current_day': timezone.now(),
            'focus_date': str(year) + '/' + str(month) + '/' + str(day),
        }

        return render(request, 'ds4admin/housemates.html', context)

    else:
        messages.error(request, 'Admin only area.')
        return redirect('/')

# view for permissionstab
def permissions(request):

    if request.user.is_superuser:

        # get list of active users sorted by move-in date
        active_users = User.objects.filter(is_active=True)
        inactive_users = User.objects.filter(is_active=False)
        housemates = Housemate.objects.filter(user__id__in=active_users).exclude(display_name='Huis')\
            .order_by('movein_date')
        inactive_housemates = Housemate.objects.filter(user__id__in=inactive_users) \
            .filter(moveout_set=None).order_by('movein_date').exclude(display_name='Admin')

        year = str(timezone.now().year).zfill(2)
        month = str(timezone.now().month).zfill(2)
        day = str(timezone.now().day).zfill(2)

        # build context object
        context = {
            'breadcrumbs': ['admin'],
            'housemates': housemates,
            'inactive': inactive_housemates,
            'current_day': timezone.now(),
            'focus_date': str(year) + '/' + str(month) + '/' + str(day),
        }

        return render(request, 'ds4admin/permissions.html', context)

    else:
        messages.error(request, 'Admin only area.')
        return redirect('/')


# handle requests to toggle user group
def toggle_group(request, group_type, user_id):

    u = User.objects.get(id=user_id)

    if group_type == 'admin':
        u.is_superuser ^= True
        u.save()

    elif group_type == 'thesau':

        g = Group.objects.get(name='thesau')

        if u.groups.filter(name='thesau').exists():
            g.user_set.remove(u)
        else:
            g.user_set.add(u)

    else:
        messages.error(request, 'Invalid group type.')

    return redirect(request.META.get('HTTP_REFERER'))


# handle remove housemate post requests
def remove_housemate(request):

    if request.method == 'POST':
        if request.user.is_authenticated():

            # get data from POST
            remove_id = int(request.POST.get('housemate'))

            if not remove_id:
                messages.error(request, 'Must specify housemate to be removed.')

            else:
                # update housemate object
                h = Housemate.objects.get(user_id=remove_id)
                h.moveout_set = True
                h.moveout_date = timezone.now()
                remaining_balance = h.balance

                u = h.user
                u.is_active = False

                # Update housemate objects for other users
                huis = Housemate.objects.get(display_name='Huis')
                amount = -1 * remaining_balance

                active_users = User.objects.filter(is_active=True)
                other_housemates = Housemate.objects.filter(user__id__in=active_users).exclude(display_name='Huis')

                # take care of remainder
                remainder = huis.balance
                print(remainder)
                print(amount)
                split_cost = Decimal(round((amount - remainder)/len(other_housemates),2))
                huis.balance = len(other_housemates)*split_cost - amount + remainder
                print(huis.balance)
                # add log entry to eating list ho table
                ho = HOLog(user=h.user, amount=remaining_balance, note='Verhuizen')

                # Save all database tables
                for o in other_housemates:
                    o.balance -= split_cost
                    o.save()
                h.save()
                u.save()
                huis.save()
                ho.save()

        else:
            return render(request, 'base/login_page.html')

    else:
        messages.error(request, 'Method must be POST.')

    return redirect(request.META.get('HTTP_REFERER'))


# handle activation of inactive housemate
def activate_housemate(request):

    if request.method == 'POST':
        if request.user.is_authenticated():

            # get data from POST
            try:
                activate_id = int(request.POST.get('housemate'))
            except TypeError:
                activate_id = None

            try:
                activate_date = request.POST.get('activate_date')
            except TypeError:
                activate_date = None

            if not activate_id:
                messages.error(request, 'Must specify housemate to be deactivated.')
            elif not activate_date:
                messages.error(request, 'No activation date given.')
            else:
                # update housemate object
                h = Housemate.objects.get(user_id=activate_id)

                # TODO: Consider setting inactivation date instead of move-out date
                h.moveout_set = None
                h.moveout_date = timezone.now()
                h.save()

                u = h.user
                u.is_active = True

                u.save()

        else:
            return render(request, 'base/login_page.html')

    else:
        messages.error(request, 'Method must be POST.')

    return redirect(request.META.get('HTTP_REFERER'))

# handle deactivation of housemate post requests
def deactivate_housemate(request):

    if request.method == 'POST':
        if request.user.is_authenticated():

            # get data from POST
            try:
                deactivate_id = int(request.POST.get('housemate'))
            except TypeError:
                deactivate_id = None

            try:
                deactivate_date = request.POST.get('deactivate_date')
                print(deactivate_date)
            except TypeError:
                deactivate_date = None

            if not deactivate_id:
                messages.error(request, 'Must specify housemate to be deactivated.')
            elif not deactivate_date:
                messages.error(request, 'Must specify deactivation date.')
            else:
                # update housemate object
                h = Housemate.objects.get(user_id=deactivate_id)
                h.moveout_set = False

                # TODO: Consider setting inactivation date instead of move-out date
                h.moveout_date = timezone.now()
                h.save()

                u = h.user
                u.is_active = False

                u.save()

        else:
            return render(request, 'base/login_page.html')

    else:
        messages.error(request, 'Method must be POST.')

    return redirect(request.META.get('HTTP_REFERER'))

