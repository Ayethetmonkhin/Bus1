from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from calendar import monthrange
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.db.models.functions import ExtractYear
from django.conf import settings
from django.conf.urls.static import static
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core import serializers
from .models import *
from datetime import datetime
from django.template.loader import render_to_string
from.models import BusRoute
# Create your views here.

def index(request):
    return render (request, 'index.html')

def home(request): #seat function +
    return render (request, 'home.html')


def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            print(username, password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'username or password invalid')
        context ={}
        return render(request, 'login.html', context)
    
def logoutview(request):
    logout(request)
    return redirect('login')

@login_required
def buslist(request):
    return render(request, 'bus_list.html')

# def searchbus(request):  #search bus 
#     fromname = request.GET.get('fromname')
#     toname = request.GET.get('toname')
#     departure_date = request.GET.get('departure_date')
#     print(fromname)
#     print(toname)

       
#     busroute = BusRoute.objects.filter(
#         from_location=fromname,
#         # to_location=toname,
#         date=departure_date,
#         path__icontains = toname 
#     )

#     bus_list = []
#     for route in busroute:
        
#         bid = route.bus.id

#         bus_list.append({
#             'bus_name': route.bus.operator.Bus_name,
#             'bus_type': route.bus.bus_type,
#             'bus_number': route.bus.bus_number,
#             'from_location': route.from_location,
#             'to_location': route.to_location,
#             'price':route.price,
#             'time':route.time,
#             'busid': bid,
#             'sid': route.id,
#         })

#     print(busroute)
#     return JsonResponse({'status': 'success', 'busroute': bus_list})

from django.http import JsonResponse
from datetime import datetime, date
from .models import BusRoute  # သင့် project structure ထဲက model import လိုက်ပါ

def searchbus(request):
    fromname = request.GET.get('fromname')
    toname = request.GET.get('toname')
    departure_date_str = request.GET.get('departure_date')

    try:
        departure_date = datetime.strptime(departure_date_str, '%Y-%m-%d').date()
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'Invalid date format'})

    today = date.today()
    if departure_date < today:
        return JsonResponse({'status': 'error', 'message': 'Cannot search past dates'})

    busroute = BusRoute.objects.filter(
        from_location__iexact=fromname,
        date=departure_date,
        path__icontains=toname
    )

    bus_list = []
    for route in busroute:
        bid = route.bus.id
        bus_list.append({
            'bus_name': route.bus.operator.Bus_name,
            'bus_type': route.bus.bus_type,
            'bus_number': route.bus.bus_number,
            'from_location': route.from_location,
            'to_location': route.to_location,
            'price': route.price,
            'time': route.time,
            'busid': bid,
            'sid': route.id,
        })

    return JsonResponse({'status': 'success', 'busroute': bus_list})


def seat_list_view(request):
    seats = Seat.objects.all()
    buses = Bus.objects.all()
    operators = BusOperator.objects.all()
    return render(request, 'seatlisttable.html', {
        'seats': seats,
        'buses': buses,
        'operators': operators,
    })



# @csrf_exempt
# def create_seat_ajax(request):
#     if request.method == 'POST':
#         seat_number = request.POST.get('seat_number')
#         bus_number = request.POST.get('bus_number')
#         bus_operator_name = request.POST.get('bus_operator')

#         if not (seat_number and bus_number and bus_operator_name):
#             return JsonResponse({'error': 'Missing data'}, status=400)

#         bus_operator = BusOperator.objects.filter(Bus_name=bus_operator_name).first()
#         if not bus_operator:
#             return JsonResponse({'error': 'Bus operator not found'}, status=404)

#         bus = Bus.objects.filter(bus_number=bus_number, operator=bus_operator).first()
#         if not bus:
#             return JsonResponse({'error': 'Bus not found'})

#         Seat.objects.create(seat_number=seat_number, bus=bus, is_available=True)
#         return JsonResponse({'success': True})

#     return JsonResponse({'error': 'Invalid request method'})

# @csrf_exempt
# def delete_seat_ajax(request, seat_id):
#     if request.method == 'POST':
#         try:
#             seat = Seat.objects.get(id=seat_id)
#             seat.delete()
#             return JsonResponse({'success': True})
#         except Seat.DoesNotExist:
#             return JsonResponse({'error': 'Seat not found'}, status=404)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def routeview(request):
    carno = Bus.objects.filter(user=request.user)
    sdate = request.GET.get('date')
   
    if request.method == 'POST':
        from_location = request.POST.get('from_location')
        to_location = request.POST.get('to_location')
        date = request.POST.get('date')
        time_str = request.POST.get('time')  # e.g. "08:30"
        car_number = request.POST.get('car_number')
        price = request.POST.get('price')
        path = request.POST.get('path')

        if time_str:
            time = datetime.strptime(time_str, "%H:%M").time()
        else:
            time = None  # or set a default time if you want

        bus = Bus.objects.filter(bus_number=car_number).first()
        busobj = Bus.objects.get(bus_number=car_number)

        route_obj, created = Route.objects.get_or_create(
            from_location=from_location,
            to_location=to_location,
        )

        if bus:
            routename = BusRoute.objects.create(
                from_location=from_location,
                to_location=to_location,
                date=date,
                time=time,
                price=price,
                bus=bus,
                route=route_obj,
                path = path,
            )

            seat_number = Seat.objects.filter(bus=bus)

            for i in seat_number:
                seatobj = Seat.objects.get(id=i.id)
                seatname = SeatBook.objects.create(
                route = routename,
                bus_number = busobj,
                seat_number=seatobj
                )
                print('success')
            
            return redirect('routeview')
    today=datetime.today().date()   
    
    if sdate == None:
        routes = BusRoute.objects.filter(  bus__operator__user=request.user, date=today) #if i click route then today date show 
    else:
       routes = BusRoute.objects.filter(  bus__operator__user=request.user, date=sdate) #if i click search date 
    return render(request, 'route.html', {
        'carno': carno,
        'routes': routes,
    })

def get_seats(request):  #seat function write in home.html have ajax and url and now this is functions
    bus_id = request.GET.get('bus_id')
    route_id = request.GET.get('sid')
    bus_obj = Bus.objects.get(id=int(bus_id))
    route_obj = BusRoute.objects.get(id=int(route_id))
    if not bus_id:
        return JsonResponse({'error': 'bus_id is required'}, status=400)

    # seats = Seat.objects.filter(bus_id=bus_id)
    seats = SeatBook.objects.filter(route=route_obj)
    bustype =  bus_obj.bus_type
    seat_data = []

    for seat in seats:
        seatobj = seat.seat_number.seat_number
        seat_data.append({
            'id': seat.id,
            'seat_number': seatobj,
            'is_available':seat.is_available,
            'seat_status': seat.seat_status
        })

    return JsonResponse({'status': 'success', 'seats': seat_data,'bus_type':bustype})

def get_selected_seats(request): #select seat 
    sid = request.GET.get('sid')
    seat_obj = Seat.objects.filter(id= int(sid))
    seats = []
    for i in seat_obj:
        seats.append({'id':i.id, 'sno':i.seat_number})
 


    return JsonResponse({'status': 'success', 'seats': seats[0]})

# def delete_route(request, id):
#     route = BusRoute.objects.get(id=id)
#     if request.method == 'POST':
#         route.delete()
#         return redirect('routeview') 

def edit_route(request, route_id):
    if request.method == 'POST':
        try:
            print(request.POST.get('path'))
            route = BusRoute.objects.get(id=route_id)
            route.save() 
            route.from_location = request.POST.get('from_location')
            route.to_location = request.POST.get('to_location')
            route.date = request.POST.get('date')
            route.time = request.POST.get('time')
            route.price = request.POST.get('price')
            route.path = request.POST.get('path')
            route.save()
            

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def delete_route(request, id):
    if request.method == 'POST':
        try:
            route = BusRoute.objects.get(id=id)
            route.delete()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                return redirect('routeview')
        except BusRoute.DoesNotExist:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Route not found.'})
            else:
                return redirect('routeview')
    return redirect('routeview')


def tablelistview(request):
    return render(request, 'tablelist.html')

#in model using SeatBook
def booking_confirmation(request, pk): 
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # print("Received data:", data)
            

            cprint = []  # move this outside loop

            for i in data:
                print(i['routeid'])
                broute = BusRoute.objects.get(id=int(i['routeid']))
                sbook = SeatBook.objects.get(route=broute, id=int(i['seat_number']))
                price = sbook.route.price
                print(price)

                sbook.name = i['pname']
                sbook.nrc = i['pnrc']
                sbook.phone = i['Pphone']
                sbook.gender = i['pgender']
                sbook.traveller_type = i['ptravellertype']
                sbook.special_request = i['prequest']
                
                busobj = sbook.bus_number
                bustype = busobj.bus_type
                opobj = busobj.operator
                opname = opobj.Bus_name
                routeobj = sbook.route
                fromloc = routeobj.from_location
                toloc = routeobj.to_location
                dateobj = routeobj.date
                timeobj = routeobj.time
                priceobj = routeobj.price
                sobj = sbook.seat_number
                seatno = sobj.seat_number
                n = sbook.name
                Nrc = sbook.nrc
                pno = sbook.phone
                gen = sbook.gender
                travel = sbook.traveller_type
                req = sbook.special_request


                cprint.append({
                    'Operator': opname,
                    'Bus_type': bustype,
                    'from_location': fromloc,
                    'to_location': toloc,
                    'Date': dateobj,
                    'Time': timeobj,
                    'Seat': seatno,
                    'Name': n,
                    'Nrc': Nrc,
                    'Phone': pno
                })

                sbook.seat_status = 2
                sbook.save()

            print('this is ticket')
            print(cprint)

            return JsonResponse({'success': True, 'message': "Booking confirmed", 'cprint': cprint})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': "Invalid or empty JSON body"}, status=400)

    else:
        return JsonResponse({'success': False, 'message': "Only POST requests are allowed"}, status=405)
    
def paymentcomplete(request, pk):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received data:", data)

            ticket = []  # Move this OUTSIDE the loop to collect all tickets

            for i in data:
                print(i['routeid'])
                broute = BusRoute.objects.get(id=int(i['routeid']))
                sbook = SeatBook.objects.get(route=broute, id=int(i['seat_number']))
                price = sbook.route.price

                sbook.name = i['pname']
                sbook.nrc = i['pnrc']
                sbook.phone = i['Pphone']
                sbook.gender = i['pgender']
                sbook.traveller_type = i['ptravellertype']
                sbook.special_request = i['prequest']
                sbook.seat_status = 3
                sbook.amount = price
                sbook.save()

                # Ticket info per seat
                busobj = sbook.bus_number
                bustype = busobj.bus_type
                opname = busobj.operator.Bus_name
                routeobj = sbook.route
                fromloc = routeobj.from_location
                toloc = routeobj.to_location
                dateobj = routeobj.date
                timeobj = routeobj.time
                priceobj = routeobj.price
                seatno = sbook.seat_number.seat_number
                n = sbook.name
                Nrc = sbook.nrc
                pno = sbook.phone
                gen = sbook.gender
                travel = sbook.traveller_type
                req = sbook.special_request

                ticket.append({
                    'Operator': opname,
                    'Bus_type': bustype,
                    'from_location': fromloc,
                    'to_location': toloc,
                    'Date': dateobj,
                    'Time': timeobj,
                    'Price': priceobj,
                    'Seat': seatno,
                    'Name': n,
                    'Nrc': Nrc,
                    'Phone': pno
                })

            print('this is ticket list:')
            print(ticket)
            return JsonResponse({'success': True, 'message': "Booking confirmed", 'ticket': ticket})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': "Invalid or empty JSON body"}, status=400)
    else:
        return JsonResponse({'success': False, 'message': "Only POST requests are allowed"}, status=405)
    
def paynowconfirm(request, pk):
    sbook = SeatBook.objects.get(id=int(pk))
    price  = sbook.route.price
    print(price)
    busobj = sbook.bus_number
    bustype = busobj.bus_type
    opobj = busobj.operator #opname
    opname= opobj.Bus_name
    routeobj = sbook.route
    fromloc = routeobj.from_location
    toloc = routeobj.to_location
    dateobj = routeobj.date
    timeobj = routeobj.time
    priceobj = routeobj.price
    sobj = sbook.seat_number
    seatno = sobj.seat_number
    n = sbook.name
    Nrc = sbook.nrc
    pno = sbook.phone

    ticket= []
    ticket.append({'Operator':opname, 'Bus_type':bustype, 'from_location':fromloc, 'to_location':toloc, 'Date':dateobj, 'Time':timeobj, 'Price':priceobj, 'Seat':seatno, 'Name':n, 'Nrc':Nrc, 'Phone':pno})
    print('this is ticket')
    print(ticket)
    sbook.seat_status=3  #change color 3
    sbook.amount = price
    sbook.save()
    return JsonResponse({'success': True, 'message': "paynow confirm",'ticket': ticket})



def cancelbooking(request, pk):
    sbook = SeatBook.objects.get(id=int(pk))
    sbook.seat_status=1 
    sbook.name = ""
    sbook.nrc = ""
    sbook.phone = ""
    sbook.save()
    return JsonResponse({'success': True, 'message': "Booking cancelled successfully."})

@login_required
def carnumberlistview(request):
    buses = Bus.objects.filter(user=request.user)
    operators = BusOperator.objects.all()
    return render(request, 'carnumberlist.html', {'buses': buses, 'operators': operators})

def create_bus(request):
    if request.method == 'POST':
        bus_number = request.POST.get('bus_number')
        driver_name = request.POST.get('driver_name')
        driver_phone = request.POST.get('driver_phone')
        bus_type = request.POST.get('bus_type')
        operator = BusOperator.objects.get(user=request.user)
       

        bus = Bus.objects.create(
            bus_number=bus_number,
            driver_name=driver_name,
            driver_phone=driver_phone,
            operator=operator,
            bus_type=bus_type, 
            user=request.user,

        )


        return JsonResponse({
            'message': 'Bus created successfully!',
            'bus': {
                'id': bus.id,
                'bus_number': bus.bus_number,
                'driver_name': bus.driver_name,
                'driver_phone': bus.driver_phone,
                'operator_name': bus.operator.Bus_name,
                'bus_type': bus.bus_type, 
            }
        })

    return JsonResponse({'message': 'Invalid request'}, status=400)

from django.views.decorators.http import require_POST

@require_POST
def delete_bus(request, bus_id):
    bus = Bus.objects.get(id=bus_id)
    bus.delete()
    return JsonResponse({'message': 'Bus deleted successfully'})

@csrf_exempt
def edit_bus(request, id):
    if request.method == 'POST':
        try:
            bus = Bus.objects.get(pk=id)
            bus.bus_number = request.POST.get('bus_number')
            bus.driver_name = request.POST.get('driver_name')
            bus.driver_phone = request.POST.get('driver_phone')
            bus.bus_type = request.POST.get('bus_type')
            bus.save()

            return JsonResponse({
                'message': 'Bus updated successfully!',
                'bus': {
                    'id': bus.id,
                    'bus_number': bus.bus_number,
                    'driver_name': bus.driver_name,
                    'driver_phone': bus.driver_phone,
                    'bus_type': bus.bus_type,
                }
            })
        except Bus.DoesNotExist:
            return JsonResponse({'message': 'Bus not found'})

        
@login_required
def busoperator(request):
    return render (request, 'operatorbusbooking.html')

def operatortodaybusroute(request):  #search bus original
    today=datetime.today().date()


    busroute = BusRoute.objects.filter(
        date=today,
        bus__operator__user=request.user
    )
    bus_list = []
    for route in busroute:
        
        bid = route.bus.id

        bus_list.append({
            'bus_name': route.bus.operator.Bus_name,
            'bus_type': route.bus.bus_type,
            'bus_number': route.bus.bus_number,
            'from_location': route.from_location,
            'to_location': route.to_location,
            'price':route.price,
            'time':route.time,
            'busid': bid,
            'sid': route.id,
        })

    return JsonResponse({'status': 'success', 'busroute': bus_list})

def opsearchroutedateview (request):
    fromname = request.GET.get('fromname')
    toname = request.GET.get('toname')
    departure_date_str = request.GET.get('departure_date')

    try:
        departure_date = datetime.strptime(departure_date_str, '%Y-%m-%d').date()
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'Invalid date format'})

    today = date.today()
    if departure_date < today:
        return JsonResponse({'status': 'error', 'message': 'Cannot search past dates'})

    busroute = BusRoute.objects.filter(
        from_location__iexact=fromname,
        date=departure_date,
        path__icontains=toname
    )

    bus_list = []
    for route in busroute:
        bid = route.bus.id
        bus_list.append({
            'bus_name': route.bus.operator.Bus_name,
            'bus_type': route.bus.bus_type,
            'bus_number': route.bus.bus_number,
            'from_location': route.from_location,
            'to_location': route.to_location,
            'price': route.price,
            'time': route.time,
            'busid': bid,
            'sid': route.id,
        })

    return JsonResponse({'status': 'success', 'busroute': bus_list})



# modal pop up seat create
def create_seat(request):
    if request.method =='POST':
        seat_number = request.POST.get('seat_number')
        bus_id = request.POST.get('bus_id')
        bus = Bus.objects.get(id=bus_id)
        Seat.objects.create(seat_number=seat_number, bus=bus)
        return redirect('/car/')
    
def get_seat_by_bus(request, bus_id):
    seats = Seat.objects.filter(bus_id=bus_id)
    seat_list = [{'id':seat.id, 'seat_number': seat.seat_number}for seat in seats]
    print(seat_list)
    return JsonResponse({'seatlist':seat_list})

def passengerinfo(request, pk):
    getroute = BusRoute.objects.get(id=int(pk))
    sbook = SeatBook.objects.filter(route=getroute)
    context = {'sbook': sbook, 'getroute': getroute}
    return render(request, 'passengerlist.html', context)

def passengers_print(request, pk):
    try:
        route = BusRoute.objects.get(id=int(pk))
        sbook = SeatBook.objects.filter(route=route)

        data = []
        for s in sbook:
            data.append({
                'name': s.name,
                'nrc': s.nrc,
                'phone': s.phone,
                'seat': str(s.seat_number),
                'gender': s.gender,  # ✅ Added Gender
                'traveller_type': s.traveller_type,  # ✅ Added Traveller Type
                'special_request': s.special_request,  # ✅ Added Special Request
                'operator': str(s.bus_number.operator.Bus_name),
                'from': str(s.route.from_location),
                'to': str(s.route.to_location),
                'bus_number': str(s.bus_number)
            })

        return JsonResponse({'success': True, 'data': data})

    except BusRoute.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Route not found'})

def reportView(request, pk):
    getroute = BusRoute.objects.get (id=pk)
    sbook = SeatBook.objects.filter(route=getroute)
    total_amount = sbook.aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'getroute': getroute,
        'sbook': sbook,
        'total_amount': total_amount,
    }
    
    return render(request, 'report.html', context)

def Report_print(request, pk):
    try:
        route = BusRoute.objects.get(id=int(pk))
        sbook = SeatBook.objects.filter(route=route)

        data = []
        for s in sbook:
            data.append({
                'name': s.name,
                'nrc': s.nrc,
                'phone': s.phone,
                'seat': str(s.seat_number),
                'amount': s.amount or 0,  # ✅ Now shows amount instead of operator
            })

        total_amount = sbook.aggregate(total=Sum('amount'))['total'] or 0

        # Route info (for header row)
        route_info = {
            'date': route.date.strftime("%Y-%m-%d"),
            'from': str(route.from_location),
            'to': str(route.to_location),
            'operator': route.bus.operator.Bus_name,
            'bus_number': str(route.bus),
        }

        return JsonResponse({
            'success': True,
            'data': data,
            'total_amount': total_amount,
            'route_info': route_info  # ✅ pass for header row
        })

    except BusRoute.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Route not found'})


# def Report_print(request, pk): old version
#     try:
#         route = BusRoute.objects.get(id=int(pk))
#         sbook = SeatBook.objects.filter(route=route)

#         data = []
#         for s in sbook:
#             data.append({
#                 'name': s.name,
#                 'nrc': s.nrc,
#                 'phone': s.phone,
#                 'seat': str(s.seat_number),
#                 'operator': route.bus.operator.Bus_name if route.bus.operator else '',
#                 # No bus_number, no from-to here
#             })

#         total_amount = sbook.aggregate(total=Sum('amount'))['total'] or 0

#         return JsonResponse({'success': True, 'data': data, 'total_amount': total_amount})

#     except BusRoute.DoesNotExist:
#         return JsonResponse({'success': False, 'error': 'Route not found'})

@login_required  
def DateByDateReport(request):
    today = datetime.today().date()
    first_date = today.replace(day=1)
    first_day_of_year = today.replace(month=1, day=1)

    base_qs = SeatBook.objects.select_related('route__bus').filter(route__bus__user=request.user)

    monthly_data = (
        base_qs.filter(route__date__range=(first_date, today))
        .values('route__from_location', 'route__to_location')
        .annotate(amount_total=Sum('amount'))
        .order_by('route__from_location')
    )

    daily_data = (
        base_qs.filter(route__date=today)
        .values('route__from_location', 'route__to_location')
        .annotate(amount_total=Sum('amount'))
    )

    yearly_data = (
        base_qs.filter(route__date__range=(first_day_of_year, today))
        .values('route__from_location', 'route__to_location')
        .annotate(amount_total=Sum('amount'))  
        .distinct()
        .order_by('route__from_location')
    )

    labels = [f"{item['route__from_location']} → {item['route__to_location']}" for item in monthly_data]
    monthly_amounts = [item['amount_total'] for item in monthly_data]

    dailylabels = [f"{item['route__from_location']} → {item['route__to_location']}" for item in daily_data]
    daily_amounts = [item['amount_total'] for item in daily_data]

    yearly_labels = [f"{item['route__from_location']} → {item['route__to_location']}" for item in yearly_data]
    yearly_amounts = [item['amount_total'] for item in yearly_data]

    context = {
        'monthly_labels': labels,
        'monthly_amounts': monthly_amounts,
        'daily_labels': dailylabels,
        'daily_amounts': daily_amounts,
        'yearly_labels': yearly_labels,
        'yearly_amounts': yearly_amounts,
    }

    return render(request, 'datebydatereport.html', context)

# @login_required  
# def DateByDateReport(request):
#     today = datetime.today().date()
    
#     # 1st day of current month
#     first_date = today.replace(day=1)
    
#     # last day of current month
#     last_day = monthrange(today.year, today.month)[1]
#     last_date_of_month = today.replace(day=last_day)
    
#     # 1st day of current year
#     first_day_of_year = today.replace(month=1, day=1)

#     base_qs = SeatBook.objects.select_related('route__bus').filter(route__bus__user=request.user)

#     # Monthly: whole current month
#     monthly_data = (
#         base_qs.filter(route__date__range=(first_date, last_date_of_month))
#         .values('route__from_location', 'route__to_location')
#         .annotate(amount_total=Sum('amount'))
#         .order_by('route__from_location')
#     )

#     # Daily: exactly today
#     daily_data = (
#         base_qs.filter(route__date=today)
#         .values('route__from_location', 'route__to_location')
#         .annotate(amount_total=Sum('amount'))
#     )

#     # Yearly: from Jan 1 to today
#     yearly_data = (
#         base_qs.filter(route__date__range=(first_day_of_year, today))
#         .values('route__from_location', 'route__to_location')
#         .annotate(amount_total=Sum('amount'))  
#         .order_by('route__from_location')
#     )

#     monthly_labels = [f"{item['route__from_location']} → {item['route__to_location']}" for item in monthly_data]
#     monthly_amounts = [item['amount_total'] for item in monthly_data]

#     daily_labels = [f"{item['route__from_location']} → {item['route__to_location']}" for item in daily_data]
#     daily_amounts = [item['amount_total'] for item in daily_data]

#     yearly_labels = [f"{item['route__from_location']} → {item['route__to_location']}" for item in yearly_data]
#     yearly_amounts = [item['amount_total'] for item in yearly_data]

#     context = {
#         'monthly_labels': monthly_labels,
#         'monthly_amounts': monthly_amounts,
#         'daily_labels': daily_labels,
#         'daily_amounts': daily_amounts,
#         'yearly_labels': yearly_labels,
#         'yearly_amounts': yearly_amounts,
#     }

#     return render(request, 'datebydatereport.html', context)



def get_total_amount(request):
    today = datetime.today().date()
    first_date = today.replace(day=1)

    routemonth = BusRoute.objects.filter(
        bus__user=request.user,
        date__range=(first_date, today)
    ).values(
        'id',
        'from_location',
        'to_location',
        'date',
        'time',
    ).annotate(
        total_amount=Sum('seatbook__amount')
    ).order_by('-total_amount')

    amount = 0
    getroute = BusRoute.objects.filter(bus__user=request.user, date=today)
    for i in getroute:
        total_amount = SeatBook.objects.filter(route=i).aggregate(total=Sum('amount'))['total'] or 0
        amount += total_amount

    max_amount = routemonth[0]['total_amount'] if routemonth else 1

    top_route_data = []
    for route in routemonth[:3]:
        top_route_data.append({
            'route_id': route['id'],
            'from': route['from_location'],
            'to': route['to_location'],
            'date': route['date'].strftime('%Y-%m-%d'),
            'time': route['time'].strftime('%I:%M %p'),
            'total_amount': route['total_amount'],
            'progress': int((route['total_amount'] / max_amount) * 100),
        })

    return JsonResponse({'total_amount': amount, 'top_route_data': top_route_data})

def aboutview(request):
    return render(request, 'about.html')

def galleryview(request):
    return render(request, 'gallery.html')