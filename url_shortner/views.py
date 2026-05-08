from django.shortcuts import render, redirect
from .forms import UrlForm
import uuid
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .models import URLModel, Click
import random 
import string
import datetime
from datetime import timedelta
from django.core.paginator import Paginator
from .models import DayData
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure




chars=string.ascii_letters + string.digits
chars= list(chars)


def go_to_link(request, pk):
    '''Clients IP address'''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # first IP = client
    else:
        ip = request.META.get('REMOTE_ADDR')

    # Find the URLModel object
    url_details = URLModel.objects.get(uuid=pk)

    # Increment total clicks
    url_to_edit = URLModel.objects.filter(uuid=pk).first()
    url_to_edit.number_of_times_clicked += 1
    url_to_edit.save()
    
    date_clicked= datetime.date.today()
    clicks_per_day=url_to_edit.number_of_times_clicked
    
    new_data1= DayData(url_relation=url_details, day_date= date_clicked, day_value=clicks_per_day)
    new_data1.save()

    # Save new click entry
    new_data2 = Click(url_relation=url_details, time_clicked=date_clicked, ip_address=ip)
    new_data2.save()
    return redirect(url_details.long_link)



def generate_graph(request, pk):
    url_details= URLModel.objects.filter(uuid=pk).first()

    queryset=DayData.objects.filter(url_relation=url_details,
                                    day_date__gte=datetime.datetime.now().date()-timedelta(days=7))
    
    date_data=[]
    clicks_data= []
    
    for record in queryset:
        date_data.append(record.day_date.strftime("%d"))
        clicks_data.append(record.day_value)
    
    '''Graph Plotting'''
    fig=Figure(figsize=(10,6))
    ax= fig.add_subplot(1,1,1)
    ax.plot(date_data, clicks_data)
    
    ax.set_xlabel('Dates')
    ax.set_ylabel('No. Of Clicks')
    ax.set_title("Weekly Click Analysis")
    
    canvas= FigureCanvas(fig)
    response= HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response



#Core function to handle the shorting of links
def shorten_url(request):
    submitted= False
    if request.method == 'POST':
        #submittng/staging our form for saving
        form=UrlForm(request.POST)
        
        #Filtering and checking if the link we want to shorten is already in our db to prevent duplicate links
        short_link_filter= URLModel.objects.values_list('short_link', flat=True)
        long_link_filter= URLModel.objects.values_list('long_link', flat=True)
        
        #getting the long link we passed in our form
        long_link = request.POST.get('long_link')
        
        if long_link in long_link_filter:
            messages.success(request, 'Link Already exists input another one')
            
        else:
            if form.is_valid():
                #generating a uuid 6 characters long
                uid=str(uuid.uuid4())[:6]
                keys= chars.copy()
                random.shuffle(keys)
                short_link=""
                
                
                for link in keys:
                    short_link += link
                short_link=short_link[:10]
                
                while short_link in short_link_filter:
                    # If the link is a duplicate, generate a new one
                    random.shuffle(keys)
                    short_link = ""
                    
                    for short in keys:
                        short_link += short
                    short_link = short_link[:10]
                    
                try:
                    #we dont save it yet cos we want to add more fields
                    url_instance= form.save(commit=False)
                    
                    url_instance.uuid=uid #attaches the generated id  to the model instance
                    url_instance.short_link= short_link #ataches our short link
                    
                    url_instance.save()
                    messages.success(request, "Link Saved")
                    return HttpResponseRedirect('/?submitted=True')
                except Exception as e:
                    print(f'Error: {e}')
            else:
                print('form wasnt submitted')
    else:
        form=UrlForm()
        if 'submitted' in request.GET:
            submitted=True
    saved_links=URLModel.objects.all().order_by('-id')
    return render(request, 'shorten_url.html', {'form': form,
                                                'links':saved_links})


#Delete Link
def delete_link(request, id):
    particular_link= URLModel.objects.get(pk=id)
    try:
        particular_link.delete()
        messages.success(request, 'Link deleted Successfully')
        return redirect('/')
    except:
        messages.success(request, 'Error deleting link')


def analytics(request):
    click_data= Click.objects.all().order_by('-time_clicked')
    p=Paginator(click_data, 10)
    
    page= request.GET.get('page')
    clicked_data= p.get_page(page)
    nums="a" * clicked_data.paginator.num_pages
    return render(request, 'analytics.html', {'click_data': click_data,
                                              'data':clicked_data,
                                              "nums":nums})
    
